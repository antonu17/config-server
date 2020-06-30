#!/usr/bin/env python

# Copyright: (c) 2020, Anton Ustyuzhanin <antonu17@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: kind

short_description: A module to manage `kind` kubernetes cluster

version_added: "2.9"

description:
    - "This is a module that handles creating amd deleting `kind` kubernetes clusters"

options:
    name:
        description:
            - Cluster name
        type: str
        required: true
    config:
        description:
            - Config file for the `kind` cluster
        type: str
        required: false
    action:
        description:
            - C(create) ensure the cluster is created
            - C(delete) ensure the cluster is deleted
            - C(status) return current cluster status
            - C(load) upload docker image into kind cluster
        type: str
        choices: [ create, delete, status ]
        required: false
    binary:
        description:
            - Path to the `kind` cli binary
        type: str
        required: false
    image:
        description:
            - Node docker image to use for booting the cluster
        type: str
        required: false
    kubeconfig:
        description:
            - Sets kubeconfig path instead of `$KUBECONFIG` or `$HOME/.kube/config`
        type: str
        required: false

author:
    - Anton Ustyuzhanin (@antonu17)
'''

EXAMPLES = '''
# Start test-cluster
- name: Create kind cluster
  kind:
    name: test-cluster

# Stop test-cluster
- name: Stop kind cluster
  kind:
    name: test-cluster
    state: deleted
'''

RETURN = '''
status:
    description: Kind cluster status. Possible values are 'created', 'deleted'
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os

kind_binary = 'kind'
kind_kubeconfig_args = []


def kind_cluster_exists(module):
    name = module.params['name']
    args = [kind_binary, "get", "clusters"]
    rc, out, err = module.run_command(args, use_unsafe_shell=True)

    for line in out.splitlines():
        if line == name:
            return True

    return False


def kind_create_cluster(module):
    name = module.params['name']
    config = module.params['config']
    image = module.params['image']

    args = [kind_binary, "create", "cluster", "--name", name]
    args.extend(kind_kubeconfig_args)

    if image:
        args.extend(["--image", image])

    if config:
        args.extend(["--config", config])

    return module.run_command(args, use_unsafe_shell=True)


def kind_delete_cluster(module):
    name = module.params['name']
    args = [kind_binary, "delete", "cluster", "--name", name]
    args.extend(kind_kubeconfig_args)

    return module.run_command(args, use_unsafe_shell=True)


def kind_load_image(module):
    name = module.params['name']
    image = module.params['image']
    args = [kind_binary, "load", "docker-image", "--name", name, image]

    return module.run_command(args, use_unsafe_shell=True)


def run_module():
    global kind_binary, kind_kubeconfig_args

    module_args = dict(
        name=dict(type='str', required=True),
        config=dict(type='str', required=False),
        action=dict(type='str', choices=['create', 'delete', 'status', 'load'], default='create'),
        binary=dict(type='str', required=False, default='kind'),
        image=dict(type='str', required=False),
        kubeconfig=dict(type='str', required=False)
    )

    result = dict(
        changed=False,
        status=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.params['binary']:
        kind_binary = module.params['binary']

    if module.params['kubeconfig']:
        kind_kubeconfig_args = ["--kubeconfig", module.params['kubeconfig']]

    if module.params['action'] == 'create':
        if not kind_cluster_exists(module):
            rc, out, err = kind_create_cluster(module)
            if rc != 0:
                module.fail_json(msg='error running kind', rc=rc, out=out, err=err)
            result['changed'] = True
            result['status'] = 'created'

    if module.params['action'] == 'delete':
        if kind_cluster_exists(module):
            rc, out, err = kind_delete_cluster(module)
            if rc != 0:
                module.fail_json(msg='error running kind', rc=rc, out=out, err=err)
            result['changed'] = True
            result['status'] = 'deleted'

    if module.params['action'] == 'load':
        if kind_cluster_exists(module):
            rc, out, err = kind_load_image(module)
            if rc != 0:
                module.fail_json(msg='error running kind', rc=rc, out=out, err=err)
            if err:
                result['changed'] = True
            result['status'] = out
        else:
            module.fail_json(msg='kind cluster is not created', rc=rc, out=out, err=err)


    if module.params['action'] == 'status':
        result['status'] = 'created' if kind_cluster_exists(module) else 'deleted'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
