FROM gcr.io/arrikto-public/tensorflow-1.14.0-notebook-cpu:v0.7.0.arr2.kale.pyodbc

USER root

RUN echo 'alias grep="grep --color=auto' >> /etc/bash.bashrc && \
   echo 'alias ls="ls --color=auto' >> /etc/bash.bashrc

# Install latest KFP SDK & Kale & JupyterLab Extension
RUN pip3 install --upgrade pip && \
   # XXX: Install enum34==1.1.8 because other versions lead to errors during
   #  KFP installation
   pip3 install tensorflow && \
   pip3 install pandas && \
   pip3 install numpy && \
   pip3 install scikit-learn && \
   pip3 install scipy && \
   pip3 install matplotlib && \
   pip3 install seaborn && \
   pip3 install --upgrade "enum34==1.1.8" && \
   pip3 install --upgrade "jupyterlab>=2.0.0,<3.0.0" && \
   pip3 install --upgrade kubeflow-kale && \
   jupyter labextension install kubeflow-kale-labextension
  

RUN echo "jovyan ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/jovyan
WORKDIR /home/jovyan
USER jovyan

CMD ["sh", "-c", \
    "jupyter lab --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser \
     --allow-root --port=8888 --LabApp.token='' --LabApp.password='' \
     --LabApp.allow_origin='*' --LabApp.base_url=${NB_PREFIX}"]