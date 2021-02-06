FROM python:3.7.1
WORKDIR /data_visuals
RUN pip install --upgrade pip \
&& pip install -U numpy pandas joblib
COPY visuals.py /data_visuals
ENTRYPOINT ["python", "visuals.py"]