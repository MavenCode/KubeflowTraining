### Simple fashion mnist example with persistent volume

The example also mounts a persistent volume for output, making it suitable
for integrating with components like Katib.

To build and push this image for usage:
```shell
docker image build -t tfjob:6.0 .
docker tag tfjob:6.0 josephcruisedocker8624/tfjob:6.0
docker push josephcruisedocker8624/tfjob:6.0
```

Usage:
1. Add the persistent volume and claim: `kubectl apply -f tfevent-volume/.`
2. Deploy the TFJob: `kubectl apply -f tfjob.yaml`
3. To get TFJob status `kubectl -n <user-namespace=josephadmin> get tfjob <YAML_file_config_name=fmnist> -o yaml`
4. To get Tensorflow Logs `kubectl -n <user-namespace=josephadmin> logs <{JOBNAME}-{REPLICA-TYPE}-{INDEX}=fmnist-worker-1>`

To delete Job:
1. `kubectl -n <user-namespace=josephadmin> delete tfjob <YAML_file_config_name=fmnist>`
