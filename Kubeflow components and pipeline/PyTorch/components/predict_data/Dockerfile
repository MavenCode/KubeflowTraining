FROM pytorch/pytorch:latest
WORKDIR /predict_pytorch
RUN pip install -U torch numpy
COPY predict.py /predict_pytorch
ENTRYPOINT ["python", "predict.py"]