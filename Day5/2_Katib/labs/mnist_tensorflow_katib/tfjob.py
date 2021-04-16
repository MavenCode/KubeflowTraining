import argparse
import logging
import json
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import SGD, Adam, RMSprop

logging.getLogger().setLevel(logging.INFO)




def make_datasets_unbatched():
  BUFFER_SIZE = 10000

  datasets, ds_info = tfds.load(name="mnist", download=True, with_info=True, as_supervised=True)
  mnist_train, mnist_test = datasets["train"], datasets["test"]

  def scale(image, label):
      image = tf.cast(image, tf.float32) / 255
      return image, label

  train_dataset = mnist_train.map(scale).cache().shuffle(BUFFER_SIZE).repeat()
  test_dataset = mnist_test.map(scale)

  return train_dataset, test_dataset


def model(args):
  model = models.Sequential()
  model.add(
      layers.Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1)))
  model.add(layers.MaxPooling2D((2, 2)))
  model.add(layers.Conv2D(128, (3, 3), activation='relu'))
  model.add(layers.Flatten())
  model.add(layers.Dense(256, activation='relu'))
  model.add(layers.Dense(10, activation='softmax'))

  model.summary()
  opt = args.optimizer
  model.compile(optimizer=opt,
                loss='sparse_categorical_crossentropy',
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
                         epochs=10,
                         steps_per_epoch=10)
  
  eval_loss, eval_acc = multi_worker_model.evaluate(test_dataset_sharded, 
                                                    verbose=0, steps=10)

  # Log metrics for Katib
  logging.info("loss={:.4f}".format(eval_loss))
  logging.info("accuracy={:.4f}".format(eval_acc))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--batch_size",
                      type=int,
                      default=128,
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
