### Simple katib mnist example with persistent volume

The example also mounts a persistent volume for output, making it suitable
for integrating with components like Katib.

To build and push this image for usage:
```shell
docker image build -t katib:2.0 .
docker tag katib:2.0 mavencodev/katib:2.0
docker push mavencodev/katib:2.0
```

Usage:
1. Add the persistent volume and claim: `kubectl apply -f tfevent-volume/.`
2. Deploy the TFJob: `kubectl apply -f katib-tfjob.yaml`
OR
3. https://raw.githubusercontent.com/<github-repository>/katib-tfjob.yaml
4. To get Katib experiment status `kubectl -n <user-namespace=kubeflow-josepholaide10> get experiment <YAML_file_config_name=mavencode> -o yaml`
5. To get  Katib experiment trial status `kubectl -n <user-namespace=kubeflow-josepholaide10> get trials>`

To delete Job:
1. `kubectl -n <user-namespace=josephadmin> delete experiment <YAML_file_config_name=mavencode>`
