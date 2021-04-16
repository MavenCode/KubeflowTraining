import argparse
import logging
import json
import os
import re
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np
import pandas as pd
# splitting the data
from sklearn.model_selection import train_test_split
# Standardization - feature scaling
from sklearn.preprocessing import StandardScaler
# data encoding
from sklearn.preprocessing import LabelEncoder

import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.layers import Dense, Flatten 
from tensorflow.keras.optimizers import SGD, Adam, RMSprop

logging.getLogger().setLevel(logging.INFO)




def make_datasets_unbatched():
  data = pd.read_csv("https://raw.githubusercontent.com/MavenCode/KubeflowTraining/master/Day2/KubeflowComponentsAndPipeline/Labs/6_minio/titanic/datasets/train.csv")

  #preprocessing
  data['relatives'] = data['SibSp'] + data['Parch']
  data.loc[data['relatives'] > 0, 'not_alone'] = 0
  data.loc[data['relatives'] == 0, 'not_alone'] = 1
  data['not_alone'] = data['not_alone'].astype(int)

  # drop columns with high cardinality
  data = data.drop(['PassengerId', 'Name', 'Ticket'], axis=1)

  #dealing with missing data in cabin feature
  deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}

  data['Cabin'] = data['Cabin'].fillna("U0")
  data['Deck'] = data['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
  data['Deck'] = data['Deck'].map(deck)
  data['Deck'] = data['Deck'].fillna(0)
  data['Deck'] = data['Deck'].astype(int)
  # we can now drop the cabin feature
  data = data.drop(['Cabin'], axis=1)

  #dealing with missing data in age feature
  data["Age"] = data["Age"].fillna(data["Age"].mean())

  #dealing with missing data in emabrk feature
  # fill with most common value
  common_value = 'S'
  data['Embarked'] = data['Embarked'].fillna(common_value)

  # encode categorical variables
  data = pd.get_dummies(data)

  X=data.drop("Survived",axis=1)
  y=data.Survived

    
  # split the data
  X_train,X_test,y_train,y_test = train_test_split( X,y, test_size=0.2, random_state = 10)
  train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
  test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))
  train = train_dataset.cache().shuffle(100).repeat()
  return train, test_dataset


def model(args):
  model = models.Sequential()
  model.add(Dense(units =20, activation='relu', input_dim=13))
  model.add(Dense(units =1, activation='sigmoid'))

  model.summary()
  opt = args.optimizer
  model.compile(optimizer=opt,
                loss='binary_crossentropy',
                metrics=['accuracy'])
  tf.keras.backend.set_value(model.optimizer.learning_rate, args.learning_rate)
  return model


def main(args):
  # MultiWorkerMirroredStrategy creates copies of all variables in the model's
  # layers on each device across all workers
  strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(
      communication=tf.distribute.experimental.CollectiveCommunication.AUTO)
  logging.debug(f"num_replicas_in_sync: {strategy.num_replicas_in_sync}")
  BATCH_SIZE_PER_REPLICA = args.batch_size
  BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync

  # Datasets need to be created after instantiation of `MultiWorkerMirroredStrategy`
  train_dataset, test_dataset = make_datasets_unbatched()
  train_dataset = train_dataset.batch(batch_size=BATCH_SIZE)
  test_dataset = test_dataset.batch(batch_size=BATCH_SIZE)

  # See: https://www.tensorflow.org/api_docs/python/tf/data/experimental/DistributeOptions
  options = tf.data.Options()
  options.experimental_distribute.auto_shard_policy = \
        tf.data.experimental.AutoShardPolicy.DATA

  train_datasets_sharded  = train_dataset.with_options(options)
  test_dataset_sharded = test_dataset.with_options(options)

  with strategy.scope():
    # Model building/compiling need to be within `strategy.scope()`.
    multi_worker_model = model(args)

  # Keras' `model.fit()` trains the model with specified number of epochs and
  # number of steps per epoch. 
  multi_worker_model.fit(train_datasets_sharded,
                         epochs=12,
                         steps_per_epoch=5)
  
  eval_loss, eval_acc = multi_worker_model.evaluate(test_dataset_sharded, 
                                                    verbose=0, steps=10)

  # Log metrics for Katib
  logging.info("loss={:.4f}".format(eval_loss))
  logging.info("accuracy={:.4f}".format(eval_acc))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--batch_size",
                      type=int,
                      default=12,
                      metavar="N",
                      help="Batch size for training (default: 128)")
  parser.add_argument("--learning_rate", 
                      type=float,  
                      default=0.001,
                      metavar="N",
                      help='Initial learning rate')
  parser.add_argument("--optimizer", 
                      type=str, 
                      default='adam',
                      metavar="N",
                      help='optimizer')

  parsed_args, _ = parser.parse_known_args()
  main(parsed_args)