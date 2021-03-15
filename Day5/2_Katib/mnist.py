import argparse
import logging

import tensorflow as tf
import tensorflow_datasets as tfds

logging.getLogger().setLevel(logging.INFO)


def make_datasets(buffer_size):
    datasets, ds_info = tfds.load(name="mnist", with_info=True, as_supervised=True)
    mnist_train, mnist_test = datasets["train"], datasets["test"]

    def scale(image, label):
        image = tf.cast(image, tf.float32) / 255
        return image, label

    train_dataset = mnist_train.map(scale).cache().shuffle(buffer_size).repeat()
    test_dataset = mnist_test.map(scale)

    return train_dataset, test_dataset


def compile_model(args):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Conv2D(64, 3, activation="relu", input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(10),
        ]
    )
    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.SGD(
            learning_rate=args.learning_rate, momentum=args.momentum
        ),
        metrics=["accuracy"],
    )
    return model


def main():
    parser = argparse.ArgumentParser(description="TensorFlow MNIST Training Job")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        metavar="N",
        help="Batch size for training (default: 64)",
    )
    parser.add_argument(
        "--buffer-size",
        type=int,
        default=10000,
        metavar="N",
        help="Number of training examples to buffer before shuffling" "default: 10000)",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.5,
        metavar="N",
        help="Learning rate (default: 0.5)",
    )
    parser.add_argument(
        "--momentum",
        type=float,
        default=0.1,
        metavar="N",
        help="Accelerates SGD in the relevant direction and dampens oscillations (default: 0.1)",
    )

    args, _ = parser.parse_known_args()

    strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
    logging.debug(f"num_replicas_in_sync: {strategy.num_replicas_in_sync}")
    global_batch_size = args.batch_size * strategy.num_replicas_in_sync

    # Datasets need to be created after instantiation of `MultiWorkerMirroredStrategy`
    train_dataset, test_dataset = make_datasets(buffer_size=args.buffer_size)
    train_dataset = train_dataset.batch(batch_size=global_batch_size)
    test_dataset = test_dataset.batch(batch_size=global_batch_size)

    # See: https://www.tensorflow.org/api_docs/python/tf/data/experimental/DistributeOptions
    dataset_options = tf.data.Options()
    dataset_options.experimental_distribute.auto_shard_policy = (
        tf.data.experimental.AutoShardPolicy.DATA
    )
    train_datasets_sharded = train_dataset.with_options(dataset_options)
    test_dataset_sharded = test_dataset.with_options(dataset_options)

    # Model compilation must be within `strategy.scope()`
    with strategy.scope():
        model = compile_model(args=args)

    # We cannot set `steps_per_epoch = None` with MirroredStrategy
    # See: https://github.com/tensorflow/tensorflow/issues/25254
    model.fit(train_datasets_sharded, epochs=10, steps_per_epoch=10)
    eval_loss, eval_acc = model.evaluate(test_dataset_sharded, verbose=0, steps=10)

    # Log metrics for Katib
    logging.info("loss={:.4f}".format(eval_loss))
    logging.info("accuracy={:.4f}".format(eval_acc))


if __name__ == "__main__":
    main()
