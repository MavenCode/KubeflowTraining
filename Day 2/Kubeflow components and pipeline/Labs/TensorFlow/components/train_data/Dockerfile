FROM tensorflow/tensorflow:latest
WORKDIR /tf_data
RUN pip install --upgrade pip \
&& pip install -U numpy 
COPY train.py /tf_data
ENTRYPOINT ["python", "train.py"]