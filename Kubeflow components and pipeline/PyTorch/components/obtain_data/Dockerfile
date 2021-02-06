FROM python:3.7.1
WORKDIR /obtain_data
RUN pip install -U pandas
COPY obtain_data.py /obtain_data
ENTRYPOINT ["python", "obtain_data.py"]