The operator-sdk and ansible prerequisites should be installed before following along with the steps. 


Create a folder and move into it. 
```
mkdir example-operator
cd example-operator 
```

Initialize the folder

`operator-sdk init --plugins=ansible --domain demo.com`

Generate the role files

`operator-sdk create api --group cache --version v1 --kind demo --generate-role`

Edit the role/demo/tasks/main.yml file and ensure it is exactly the same with the text below 
```
name:  Hello World Task
debug:
   msg: “Hello World! This is an operator.”
when: toggle_message
```

Open the config/samples/cache_v1_demo.yml file and replace the `foo:bar` under the spec column with `toggle_message: true`.

Build and push the operator container to any registry of choice.

`make docker-build docker-push IMG=<some-registry>/<project-name>:tag`
