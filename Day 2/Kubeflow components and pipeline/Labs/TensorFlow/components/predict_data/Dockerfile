FROM tensorflow/tensorflow:latest
WORKDIR /predict_data
RUN pip install --upgrade pip \
&& pip install -U scikit-learn numpy pandas 
COPY predict.py /predict_data
ENTRYPOINT ["python", "predict.py"]