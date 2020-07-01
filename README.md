# Config Server

This is a demo project. The main 4 scopes of the demo are Programming, Automation, CI/CD, and Observability.

Programming part is a REST API server written on Python

- Code organization
- Unit testing
- 12 Factor compliance (to some extent)
- API Documentation (RAML, Console)
- Data access layer
- Containerization
- Packaging via [Helm][4]
- Building automation via GNU Make

Automation part for provisioning demo Kubernetes cluster is written on Ansible.

- Use of various Ansible features: Galaxy Dependencies, Collections, Custom Modules, Roles, Playbooks, Variables, etc.
- Use [Kind][1] to create demo Kubernetes cluster
- Use [Helm][4] to deploy core components: Nginx Ingress, Concourse CI, Prometheus, Grafana, etc.
- Use local artifact repositories: [registry][2] for docker images, [chartmuseum][5] for helm charts

CI/CD part is a Concourse pipeline with 2 workflows: Testing Pull requests, and Building+Deployment a new version when PR is merged.

- Use of YAML anchors to simplify pipeline code
- Use of various Concourse features: Pipelines, Resources, Jobs, Tasks, Input/Output volumes, Parallel execution

Observability part provides logging, metrics, traces collection and visualization.

- Prometheus
- Grafana Loki
- Open telemetry
- Grafana
- Jaeger UI

## Purpose

The `config-server` is an API server for storing and querying arbitrary JSON object via REST interface. Possible areas of application:

* Key-value storage
* Feature toggle storage
* Shared session data storage

I have chosen python for this project, mainly because I have never written REST API on python before and wanted to check it out.

## API reference

The REST API has the following methods implemented

| Action  | HTTP Method | URL
| ------- | ----------- | -----------------
| List    | `GET`       | `/configs`
| Create  | `POST`      | `/configs`
| Get     | `GET`       | `/configs/{name}`
| Replace | `PUT`       | `/configs/{name}`
| Update  | `PATCH`     | `/configs/{name}`
| Delete  | `DELETE`    | `/configs/{name}`

## Development process

New features are added via pull requests. Before pushing changes to the upstream make sure all tests are passed.
In order to simplify local development and testing there's a `Makefile` with the following goals defined:

* `setup`: configure local `virtualenv` environment in `.venv` directory and installs required libraries
* `clean`: remove `.venv` directory
* `lint`: check code style with `flake8`
* `test`: run unit tests with `python -m unittest`
* `run`: spin up the server locally via `docker-compose`
* `build`: create `build` directory and copy all required runtime files into it
* `artifact`: build a versioned docker image from `build` directory

## Release, deployment, CI/CD Demo

To check out the demo you need to spin up the fully-fledged demo environment with Kubernetes, Docker registry, CI/CD platform.

### Pre-requisites

Developer system should have the following components

* Git
* Python 3.8 (including pip and -m venv)
* Ansible
* GNU Make
* Docker
* Kubectl cli
* Kind cli
* Helm v3 cli

### Install kind cli manually

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.8.1/kind-$(uname)-amd64
chmod +x ./kind
mv ./kind /some-dir-in-your-PATH/kind
```

### Install helm v3 cli manually

Follow instructions from the official documentation https://helm.sh/docs/intro/install/

### Provision demo environment

The entire demo environment is running on Kubernetes in Docker, using [`kind`][1] project. All the components are running inside the demo Kubernetes cluster:

* Docker registry is not actually required when running `kind`, because images can be uploaded via kind cli. For local demonstration purposes I'd go with official [registry][2]
* CI/CD platform. I've chosen [Concourse CI][3]
* Observability stack

```bash
git clone antonu17/config-server
cd config-server/automation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml -p ./collections/
ansible-playbook -i local.ini demo-environment.yml
```

To deploy `kind` cluster with ansible I didn't find Ansible module I also didn't want to use `shell`
or `command` module to run `kind` cli, so I decided to write a simple module that can create, delete,
and check status of the `kind` cluster.

After kind cluster is operational, the following components are installed using Helm v3:

* nginx-ingress controller
* concourse

[1]: https://kind.sigs.k8s.io/
[2]: https://hub.docker.com/_/registry
[3]: https://concourse-ci.org/
[4]: https://helm.sh/
[5]: https://github.com/helm/chartmuseum
