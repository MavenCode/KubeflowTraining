FROM tensorflow/tensorflow:2.3.0
RUN pip install tensorflow_datasets
RUN pip install keras
COPY tfjob.py /
ENTRYPOINT ["python", "/tfjob.py", "--saved_model_dir", "/train/saved_model/", "--learning_rate", "0.001", "--optimizer", "adam"]