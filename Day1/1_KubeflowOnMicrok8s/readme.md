# Deploy Kubeflow on Microk8s

  1. Install Microk8s
  
     `sudo snap install microk8s --classic`


  2. Join  Microk8s group
  
     `sudo usermod -a -G microk8s "$NEWUSER"`
      
     `sudo chown -f -R "$NEWUSER" /.kube`

  3. Logout of the VM
  
     `exit`

  4. ssh into the vm 
  
     `ssh -i “key.pem” ubuntu@......amazonaws.com`

  5. Enable Microk8s addons
  
     `microk8s.enable dns dashboard storage metrics-server`
     
  6. Check microk8s status
  
	   `microk8s status`
     
      `microk8s.kubectl get pods --all namespaces`

  
  7. Enable kubeflow
  
	   `microk8s.enable kubeflow`
     
     
     
  8. Once kubeflow is sucessfully enabled, log out of your vm and configure SOCK Proxy on your browser
  
     `exit`
     
     `ssh -i “key.pem” -D9999 ubuntu@......amazonaws.com`
     
     Watch this [video](https://drive.google.com/file/d/1z9FGpzmnZgYNLAgi_GlIHPU1HOhTbLYI/view?usp=sharing) for more details on how SOCK Proxy is configured.
     
  9. Now copy the Kubeflow GUI address from your terminal (e.g. http://10.64.140.43.xip.io) and paste it into Firefox URL bar.
  
  
 
  
  
