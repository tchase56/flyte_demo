# Instructions

## create conda environment 

* conda create -n flyte_env python=3.9
* conda activate flyte_env
* conda install pandas
* pip install -U flytekit

## run hello world example 

* pyflyte run example.py hello_world_wf
* pyflyte run example.py hello_world_wf --name Ada

## flyte project

* create flyte-ready projects (from flyte github templates)
    * pyflyte init --template basic_template-dockerfile basic_template
    * pyflyte init --template wine-classification wine-classification

## basic_template example

* install requirements in conda environment
    * cd basic_template
    * pip install -r requirements.txt
* run workflow in a local python environment
    * cd workflows
    * pyflyte run example.py wf

## wine-classification example

* install requirments in conda environment
    * cd wine-classification
    * pip install -r requirements.txt
* run workflow in a local python environment
    * cd workflows
    * pyflyte run wine_classification_example.py training_workflow

## run on local cluster

* update x-code if necessary
* install flytectl
    * brew install flyteorg/homebrew-tap/flytectl
* export FLYTECTL_CONFIG environment variable in your shell
    *  export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml
* start the docker daemon
    * open rancher desktop
* start the demo cluster
    * flytectl demo start
    * if you are running rancher desktop and you get an error about not finding docker daemon
        * sudo ln -s ~$USER/.rd/docker.sock /var/run/docker.sock

![screenshot](images/daemon_error.png)

* if you get the error "Error starting userland proxy: listen tcp4 0.0.0.0:6443: bind: address already in use"
    * sudo lsof -i -P -n | grep <port number>  # List who's using the port
    * https://github.com/flyteorg/flyte/issues/3792
    * https://discuss.flyte.org/c/ask-the-community/52
    * go into rancher desktop and disable kubernetes (and maybe traefik as well)

![screenshot](images/port_error.png)

![screenshot](images/solution_to_port_error.png)

* create a project on the demo cluster to correspond to your local Flyte project
    * flytectl create project \
    --id "my-project" \
    --labels "my-label=my-project" \
    --description "My Flyte project" \
    --name "My project"
* Run the workflow on the Flyte cluster with pyflyte run using the --remote flag and additional parameters for the project name and domain. In this example, you can also optionally pass a name parameter to the workflow:
    * pyflyte run --remote -p my-project -d development example.py wf --name Ada
    * You should see a URL to the workflow execution on your demo Flyte cluster, where <execution_name> is a unique identifier for the workflow execution:


## inspecting the workflow run in the FlyteConsole web interface
* execution view
    * The default execution view shows the list of tasks executing in sequential order.

![screenshot](images/execution_view_flyte.png)

* task panel
    * Clicking on a single task will open a panel that shows task logs, inputs, outputs, and metadata.

![screenshot](images/task_panel_flyte.png)

* graph view
    * The Graph view shows the execution graph of the workflow, providing visual information about the topology of the graph and the state of each node as the workflow progresses.

![screenshot](images/graph_view_flyte.png)

* timeline view

![Screenshot](images/timeline_view_flyte)





references
* cookiecutter python project
    * https://cookiecutter.readthedocs.io/en/1.7.2/first_steps.html
* flyte
    * https://docs.flyte.org/en/latest/introduction.html
