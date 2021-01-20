## Installing Microk8s
Microks is a lightweight Kubernetes distribution that can be installed on a virtual machine, your local environment(Linux, Windows and Mac) or on the cloud in seconds.
It is small, simple secure, current comprehensive and is also said to deliver the fastest and most efficient multi-node kubernetes.

Microk8s is deployed via Snaps, they are containerised software packages that are simple to create and install. 
The microk8s snap is frequently updated to match each release of Kubernetes. It can be installed using the command below:

`snap install microk8s --classic --beta`{{execute}}

You could also spercify the version you want. For example to install Microk8s in the v1.18 series:

`sudo snap install microk8s --classic --channel=1.18/stable`

To see the versions available try 

`snap info microk8s`{{execute}}

Now that you have installed microk8s you can view the node you just deployed.  

`microk8s.kubectl get node`{{execute}}

This might take a few second, so wait a couple of moments. If you receive an error it means that microk8s is still starting in the background. 
Wait alittle longer and try again.



**PS: We are deploying Microk8s on Ubuntu for this scenario.**
