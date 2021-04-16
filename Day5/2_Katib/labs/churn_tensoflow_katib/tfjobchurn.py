import argparse
import logging
import json
import os
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
  data = pd.read_csv("https://raw.githubusercontent.com/AdeloreSimiloluwa/Artificial-Neural-Network/master/data/Churn_Modelling.csv")

  #preprocessing
  X = data.iloc[:, 3:-1]
  y = data.iloc[:,-1:]

  # encoding country
  encoder_X_1= LabelEncoder()
  X.iloc[:,1] = encoder_X_1.fit_transform(X.iloc[:,1])

  # encoding gender
  encoder_X_2= LabelEncoder()
  X.iloc[:,2] = encoder_X_2.fit_transform(X.iloc[:,2])

  # we would also use the dummy variable because they are norminal variables
  dummy = pd.get_dummies(X["Geography"], prefix = ['Geography'],drop_first=True)
  X=pd.concat([X,dummy], axis = 1)
  X=X.drop(columns = ['Geography'], axis = 1)
    
  # split the data
  X_train,X_test,y_train,y_test = train_test_split( X,y, test_size=0.2, random_state = 10)
  train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
  test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))
  train = train_dataset.cache().shuffle(2000).repeat()
  return train, test_dataset


def model(args):
  model = models.Sequential()
  model.add(Dense(units =9, activation='relu', input_dim=11))
  model.add(Dense(units =9, activation='relu'))
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
                         epochs=50,
                         steps_per_epoch=30)
  
  eval_loss, eval_acc = multi_worker_model.evaluate(test_dataset_sharded, 
                                                    verbose=0, steps=10)

  # Log metrics for Katib
  logging.info("loss={:.4f}".format(eval_loss))
  logging.info("accuracy={:.4f}".format(eval_acc))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--batch_size",
                      type=int,
                      default=32,
                      metavar="N",
                      help="Batch size for training (default: 128)")
  parser.add_argument("--learning_rate", 
                      type=float,  
                      default=0.1,
                      metavar="N",
                      help='Initial learning rate')
  parser.add_argument("--optimizer", 
                      type=str, 
                      default='adam',
                      metavar="N",
                      help='optimizer')

  parsed_args, _ = parser.parse_known_args()
  main(parsed_args)
