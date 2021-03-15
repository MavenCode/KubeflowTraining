FROM python:3.7.1
WORKDIR /preprocess_data
RUN pip install --upgrade pip \
&& pip install -U scikit-learn numpy pandas
COPY reusable_preprocess.py /preprocess_data
ENTRYPOINT ["python", "reusable_preprocess.py"]