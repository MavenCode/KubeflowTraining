FROM python:3.6
WORKDIR /obtain_data
RUN pip install -U joblib pandas
COPY obtain_data.py /obtain_data
ENTRYPOINT ["python", "obtain_data.py"]