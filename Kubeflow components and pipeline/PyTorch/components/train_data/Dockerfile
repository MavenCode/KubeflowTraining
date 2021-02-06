FROM pytorch/pytorch:latest
WORKDIR /train_pytorch
RUN pip install --upgrade pip==19.3 \
&& pip install -U torch numpy joblib
COPY train.py /train_pytorch
ENTRYPOINT ["python", "train.py"]