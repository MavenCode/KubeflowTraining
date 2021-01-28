For this scenario we will deploy a pretrained saved model from Tensorflow/models. We will use a toy model called **Half plus two** which generates  **`0.5*x+2`** for the values of **`x`** we provide for prediction:

To get this model, first clone the TensorFlow Serving repo.

`git clone https://github.com/tensorflow/serving`{{execute}}

Set path to the model.

`model_dir=/root/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_cpu`{{execute}}
