If the service type is LoadBalancer, it will have its own accessible external ip. Get the external ip by:
`microk8s kubectl get svc mnist-service`{{execute}}

And then send the request

`curl -X POST -d @input.json http://localhost:8500/v1/models/mnist:predict`{{execute}}
