Learn how to build a kubeflow component in 2 different ways

1. Lightweight method

2. Resuable method, which involves the use of :

   a. a python script

   b. a docker image 
   
   Run the following code in you jupyter notebook terminal before you run the notebook
   
      `docker pull python:3.7.1`
      
      cd into the notebook directory `KubeflowTraining/Day 2/KubeflowComponentsAndPipeline/Labs/1_creatingPipelineComponents` and run the following to build the 
      docker image:

      `docker build --tag=preprocess-component:v.0.2`

      `docker login`

      `docker tag preprocess-component:v.0.2 mavencodev/preprocess-component:v.0.2`

      `docker push mavencodev/preprocess-component:v.0.2`

Details on how each are created are in the the [jupyter notebook](https://github.com/MavenCode/KubeflowTraining/blob/master/Day%202/KubeflowComponentsAndPipeline/Labs/1_creatingPipelineComponents/Different%20ways%20to%20build%20a%20Kubeflow%20component%20.ipynb) and you can also following through with this video illutration.
