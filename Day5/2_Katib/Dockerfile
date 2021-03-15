FROM tensorflow/tensorflow:2.3.0
RUN pip install tensorflow_datasets
ADD mnist.py /
 
ENTRYPOINT ["python", "-u", "/mnist.py"]