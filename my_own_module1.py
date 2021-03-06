#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import os
from ansible.module_utils._text import to_bytes
# from ansible.module_utils._text import to_text


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True), #name
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)

    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
   
    if module.check_mode:
        module.exit_json(**result)
    
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'
    
    rc = os.makedirs(module.params['path'], mode=0o755, exist_ok=False)
    if (not os.access(to_bytes(module.params['path']) + to_bytes(module.params['name']), os.F_OK)):
        f = open(to_bytes(module.params['path']) + to_bytes(module.params['name']), 'wb')
        f.write(to_bytes(module.params['content']))
        f.close()
        result['changed'] = True
        result['message'] = 'File was created successfuly'
    else:
        result['changed'] = False
        result['message'] = 'File already exist'

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()