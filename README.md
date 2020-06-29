# Config Server

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
* Python (including pip and virtualenv)
* Ansible
* GNU Make
* Docker
* Kubectl cli
* [Kind](#install-kind) cli

The entire demo environment is running on Kubernetes in Docker, using [`kind`][1] project. All the components are running inside the demo Kubernetes cluster:

* Docker registry is not actually required when running `kind`, because images can be uploaded via kind cli. For local demonstration purposes I'd go with official [registry][2]
* CI/CD platform. I've chosen [Concourse CI][3]
* Observability stack


### Install kind cli

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.8.1/kind-$(uname)-amd64
chmod +x ./kind
mv ./kind /some-dir-in-your-PATH/kind
```

### Deploy demo environment

```bash
git clone antonu17/config-server
cd config-server/automation
ansible-playbook -i local.ini kind-cluster.yml
```

[1]: https://kind.sigs.k8s.io/
[2]: https://hub.docker.com/_/registry
[3]: https://concourse-ci.org/
