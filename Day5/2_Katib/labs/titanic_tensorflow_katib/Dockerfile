FROM tensorflow/tensorflow:2.3.0
RUN pip install tensorflow_datasets pandas scikit-learn keras
COPY tfjobtitan.py /
ENTRYPOINT ["python", "/tfjobtitan.py", "--batch_size", "10", "--learning_rate", "0.001", "--optimizer", "sgd"]