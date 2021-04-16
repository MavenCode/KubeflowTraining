FROM tensorflow/tensorflow:2.4.0
RUN pip install tensorflow_datasets
COPY tfjob.py /
ENTRYPOINT ["python", "/tfjob.py", "--batch_size", "100", "--learning_rate", "0.001", "--optimizer", "adam"]