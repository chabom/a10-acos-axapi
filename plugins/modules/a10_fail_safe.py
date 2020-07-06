#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = r'''
module: a10_fail_safe
description:
    - Fail Safe Global Commands
short_description: Configures A10 fail-safe
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
          - noop
          - present
          - absent
        required: True
    ansible_host:
        description:
        - Host for AXAPI authentication
        required: True
    ansible_username:
        description:
        - Username for AXAPI authentication
        required: True
    ansible_password:
        description:
        - Password for AXAPI authentication
        required: True
    ansible_port:
        description:
        - Port for AXAPI authentication
        required: True
    a10_device_context_id:
        description:
        - Device ID for aVCS configuration
        choices: [1-8]
        required: False
    a10_partition:
        description:
        - Destination/target partition for object/command
        required: False
    oper:
        description:
        - "Field oper"
        required: False
        suboptions:
            total_system_memory:
                description:
                - "Field total_system_memory"
            fpga_stats_iochan:
                description:
                - "Field fpga_stats_iochan"
            total_free_fpga_buff:
                description:
                - "Field total_free_fpga_buff"
            total_fpga_buffers:
                description:
                - "Field total_fpga_buffers"
            free_fpga_buffers:
                description:
                - "Field free_fpga_buffers"
            config:
                description:
                - "Field config"
            fpga_stats_num_cntrs:
                description:
                - "Field fpga_stats_num_cntrs"
            free_session_memory:
                description:
                - "Field free_session_memory"
            avail_fpga_buff_domain1:
                description:
                - "Field avail_fpga_buff_domain1"
            avail_fpga_buff_domain2:
                description:
                - "Field avail_fpga_buff_domain2"
            total_session_memory:
                description:
                - "Field total_session_memory"
            fpga_buff_recovery_threshold:
                description:
                - "Field fpga_buff_recovery_threshold"
            sess_mem_recovery_threshold:
                description:
                - "Field sess_mem_recovery_threshold"
    session_mem_recovery_threshold:
        description:
        - "Session memory recovery threshold (percentage) (Percentage of available session memory (default 30%))"
        required: False
    log:
        description:
        - "Log the event"
        required: False
    fpga_buff_recovery_threshold:
        description:
        - "FPGA buffers recovery threshold (Units of 256 buffers (default 2))"
        required: False
    hw_error_monitor:
        description:
        - "'hw-error-monitor-disable'= Disable fail-safe hardware error monitor; 'hw-error-monitor-enable'= Enable fail-safe hardware error monitor; "
        required: False
    hw_error_recovery_timeout:
        description:
        - "Hardware error recovery timeout (minutes) (waiting time of recovery from hardware errors (default 0))"
        required: False
    sw_error_monitor_enable:
        description:
        - "Enable fail-safe software error monitor"
        required: False
    fpga_monitor_enable:
        description:
        - "FPGA monitor feature enable"
        required: False
    fpga_monitor_threshold:
        description:
        - "FPGA monitor packet missed for error condition (Numbers of missed monitor packets before setting error condition (default 3))"
        required: False
    fpga_monitor_forced_reboot:
        description:
        - "FPGA monitor forced reboot in error condition"
        required: False
    kill:
        description:
        - "Stop the traffic and log the event"
        required: False
    disable_failsafe:
        description:
        - "Field disable_failsafe"
        required: False
        suboptions:
            action:
                description:
                - "'all'= Disable All; 'io-buffer'= Disable I/O Buffer; 'session-memory'= Disable Session Memory; 'system-memory'= Disable System Memory; "
            uuid:
                description:
                - "uuid of the object"
    total_memory_size_check:
        description:
        - "Check total memory size of current system (Size of memory (GB))"
        required: False
    fpga_monitor_interval:
        description:
        - "FPGA monitor packet interval (seconds) (Numbers of seconds between sending packets (default 1))"
        required: False
    config:
        description:
        - "Field config"
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
    sw_error_recovery_timeout:
        description:
        - "Software error recovery timeout (minutes) (waiting time of recovery from software errors (default 3))"
        required: False
    uuid:
        description:
        - "uuid of the object"
        required: False


'''

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["config","disable_failsafe","fpga_buff_recovery_threshold","fpga_monitor_enable","fpga_monitor_forced_reboot","fpga_monitor_interval","fpga_monitor_threshold","hw_error_monitor","hw_error_recovery_timeout","kill","log","oper","session_mem_recovery_threshold","sw_error_monitor_enable","sw_error_recovery_timeout","total_memory_size_check","uuid",]

# our imports go at the top so we fail fast.
try:
    from ansible_collections.a10.acos_axapi.plugins.module_utils import errors as a10_ex
    from ansible_collections.a10.acos_axapi.plugins.module_utils.axapi_http import client_factory, session_factory
    from ansible_collections.a10.acos_axapi.plugins.module_utils.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        ansible_host=dict(type='str', required=True),
        ansible_username=dict(type='str', required=True),
        ansible_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=['noop', 'present', 'absent']),
        ansible_port=dict(type='int', choices=[80, 443], required=True),
        a10_partition=dict(type='dict', name=dict(type='str',), shared=dict(type='str',), required=False, ),
        a10_device_context_id=dict(type='int', choices=[1, 2, 3, 4, 5, 6, 7, 8], required=False, ),
        get_type=dict(type='str', choices=["single", "list", "oper", "stats"]),
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        oper=dict(type='dict', total_system_memory=dict(type='int', ), fpga_stats_iochan=dict(type='list', fpga_stats_iochan_tx=dict(type='int', ), fpga_stats_iochan_rx=dict(type='int', ), fpga_stats_iochan_id=dict(type='int', )), total_free_fpga_buff=dict(type='int', ), total_fpga_buffers=dict(type='int', ), free_fpga_buffers=dict(type='int', ), config=dict(type='dict', oper=dict(type='dict', fpga_mon_threshold=dict(type='str', ), sw_error_mon=dict(type='str', ), sw_recovery_timeout=dict(type='str', ), hw_recovery_timeout=dict(type='str', ), fpga_mon_interval=dict(type='str', ), fpga_mon_forced_reboot=dict(type='str', ), fpga_mon_enable=dict(type='str', ), mem_mon=dict(type='str', ), hw_error_mon=dict(type='str', ))), fpga_stats_num_cntrs=dict(type='int', ), free_session_memory=dict(type='int', ), avail_fpga_buff_domain1=dict(type='int', ), avail_fpga_buff_domain2=dict(type='int', ), total_session_memory=dict(type='int', ), fpga_buff_recovery_threshold=dict(type='int', ), sess_mem_recovery_threshold=dict(type='int', )),
        session_mem_recovery_threshold=dict(type='int', ),
        log=dict(type='bool', ),
        fpga_buff_recovery_threshold=dict(type='int', ),
        hw_error_monitor=dict(type='str', choices=['hw-error-monitor-disable', 'hw-error-monitor-enable']),
        hw_error_recovery_timeout=dict(type='int', ),
        sw_error_monitor_enable=dict(type='bool', ),
        fpga_monitor_enable=dict(type='bool', ),
        fpga_monitor_threshold=dict(type='int', ),
        fpga_monitor_forced_reboot=dict(type='bool', ),
        kill=dict(type='bool', ),
        disable_failsafe=dict(type='dict', action=dict(type='str', choices=['all', 'io-buffer', 'session-memory', 'system-memory']), uuid=dict(type='str', )),
        total_memory_size_check=dict(type='int', ),
        fpga_monitor_interval=dict(type='int', ),
        config=dict(type='dict', uuid=dict(type='str', )),
        sw_error_recovery_timeout=dict(type='int', ),
        uuid=dict(type='str', )
    ))
   

    return rv

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/fail-safe"

    f_dict = {}

    return url_base.format(**f_dict)

def oper_url(module):
    """Return the URL for operational data of an existing resource"""
    partial_url = existing_url(module)
    return partial_url + "/oper"

def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]

def get(module):
    return module.client.get(existing_url(module))

def get_list(module):
    return module.client.get(list_url(module))

def get_oper(module):
    if module.params.get("oper"):
        query_params = {}
        for k,v in module.params["oper"].items():
            query_params[k.replace('_', '-')] = v 
        return module.client.get(oper_url(module),
                                 params=query_params)
    return module.client.get(oper_url(module))

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return None

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        elif isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_envelope(title, data):
    return {
        title: data
    }

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/fail-safe"

    f_dict = {}

    return url_base.format(**f_dict)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if x in params and params.get(x) is not None])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v is not None:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            elif isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def report_changes(module, result, existing_config, payload):
    if existing_config:
        for k, v in payload["fail-safe"].items():
            if isinstance(v, str):
                if v.lower() == "true":
                    v = 1
                else:
                    if v.lower() == "false":
                        v = 0
            elif k not in payload:
               break
            else:
                if existing_config["fail-safe"][k] != v:
                    if result["changed"] != True:
                        result["changed"] = True
                    existing_config["fail-safe"][k] = v
            result.update(**existing_config)
    else:
        result.update(**payload)
    return result

def create(module, result, payload):
    try:
        post_result = module.client.post(new_url(module), payload)
        if post_result:
            result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result, existing_config, payload):
    try:
        post_result = module.client.post(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result, existing_config):
    payload = build_json("fail-safe", module)
    changed_config = report_changes(module, result, existing_config, payload)
    if module.check_mode:
        return changed_config
    elif not existing_config:
        return create(module, result, payload)
    elif existing_config and not changed_config.get('changed'):
        return update(module, result, existing_config, payload)
    else:
        result["changed"] = True
        return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def absent(module, result, existing_config):
    if module.check_mode:
        if existing_config:
            result["changed"] = True
            return result
        else:
            result["changed"] = False
            return result
    else:
        return delete(module, result)

def replace(module, result, existing_config, payload):
    try:
        post_result = module.client.put(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message="",
        result={}
    )

    state = module.params["state"]
    ansible_host = module.params["ansible_host"]
    ansible_username = module.params["ansible_username"]
    ansible_password = module.params["ansible_password"]
    ansible_port = module.params["ansible_port"]
    a10_partition = module.params["a10_partition"]
    a10_device_context_id = module.params["a10_device_context_id"]

    if ansible_port == 80:
        protocol = "http"
    elif ansible_port == 443:
        protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        for ve in validation_errors:
            run_errors.append(ve)
    
    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(ansible_host, ansible_port, protocol, ansible_username, ansible_password)
    
    if a10_partition:
        module.client.activate_partition(a10_partition)

    if a10_device_context_id:
        module.client.change_context(a10_device_context_id)

    existing_config = exists(module)
    
    if state == 'present':
        result = present(module, result, existing_config)

    elif state == 'absent':
        result = absent(module, result, existing_config)
    
    elif state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
        elif module.params.get("get_type") == "oper":
            result["result"] = get_oper(module)
    module.client.session.close()
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec(), supports_check_mode=True)
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()