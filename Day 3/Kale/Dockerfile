
FROM gcr.io/arrikto-public/tensorflow-1.14.0-notebook-cpu:v0.7.0.arr2.kale.pyodbc
USER root
RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install seaborn
RUN pip install scikit-learn
RUN pip install tensorflow==2.3.0
RUN pip install requests --upgrade
RUN pip install jupyterlab
RUN pip install kfp kfp-server-api --upgrade
# Install Kale python package globally
RUN pip install kubeflow-kale
# Install Kale JupyterLab extension
RUN jupyter labextension install kubeflow-kale-labextension
ENV NB_PREFIX /
CMD ["sh", "-c", \
     "jupyter lab --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser \
      --allow-root --port=8888 --LabApp.token='' --LabApp.password='' \
      --LabApp.allow_origin='*' --LabApp.base_url=${NB_PREFIX}"]