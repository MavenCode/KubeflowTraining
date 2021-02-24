Learn how to build a kubeflow component in 2 different ways

1. Lightweight method

2. Resuable method, which involves the use of :

   a. a python script

   b. a docker image 
   
   Ensure you have docker installed in your environment.
   
   `sudo snap install docker --classic`

   Run the following code in your cli before you run the notebook
   
      `docker pull python:3.7.1`
      
      Clone this repository `git clone https://github.com/MavenCode/KubeflowTraining.git`
      
      Change your working directory to `KubeflowTraining/Day 2/KubeflowComponentsAndPipeline/Labs/1_creatingPipelineComponents` and run the following to build the 
      docker image:

      `docker build --tag=preprocess-component:v.0.2 .`

      `docker login`

      `docker tag preprocess-component:v.0.2 mavencodev/preprocess-component:v.0.2`

      `docker push mavencodev/preprocess-component:v.0.2`

Details on how each are created are in the the [jupyter notebook](https://github.com/MavenCode/KubeflowTraining/blob/master/Day%202/KubeflowComponentsAndPipeline/Labs/1_creatingPipelineComponents/Different%20ways%20to%20build%20a%20Kubeflow%20component%20.ipynb) and you can also following through with this [video illustration](https://drive.google.com/file/d/19t9AV82VjFGus1z9bpcl6d6gwoz-Cs5R/view?usp=sharing).
