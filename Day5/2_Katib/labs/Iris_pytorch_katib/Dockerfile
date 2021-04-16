FROM pytorch/pytorch:1.0-cuda10.0-cudnn7-runtime
RUN pip install pandas scikit-learn
ADD iris.py /opt
WORKDIR /opt

# Add folder for the logs.
RUN mkdir /katib

RUN chgrp -R 0 /opt \
  && chmod -R g+rwX /opt \
  && chgrp -R 0 /katib \
  && chmod -R g+rwX /katib

ENTRYPOINT ["python3", "/opt/iris.py"]