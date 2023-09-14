# coding: utf-8
# OceanBase Deploy.
# Copyright (C) 2021 OceanBase
#
# This file is part of OceanBase Deploy.
#
# OceanBase Deploy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OceanBase Deploy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OceanBase Deploy.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import absolute_import, division, print_function

from enum import Enum


class LockError(Exception):
    pass


class OBDErrorCode(object):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return  self.msg


class OBDErrorCodeTemplate(object):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        self._str_ = ('OBD-%04d: ' % code) + msg

    def format(self, *args, **kwargs):
        return OBDErrorCode(
            self.code,
            self._str_.format(*args, **kwargs),
        )

    def __str__(self):
        return self.msg


class FixEval(object):

    DEL = 0
    SET = 1

    def __init__(self, operation, key, value=None, is_global=False):
        self.operation = operation
        self.key = key
        self.value = value
        self.is_global = is_global

class OBDErrorSuggestion(object):

    def __init__(self, msg, auto_fix=False, fix_eval=[]):
        self.msg = msg
        self.auto_fix = auto_fix
        self.fix_eval = fix_eval


class OBDErrorSuggestionTemplate(object):

    def __init__(self, msg, auto_fix=False, fix_eval=[]):
        self._msg = msg
        self.auto_fix = auto_fix
        self.fix_eval = fix_eval if isinstance(fix_eval, list) else [fix_eval]

    def format(self, *args, **kwargs):
        return OBDErrorSuggestion(
            self._msg.format(*args, **kwargs),
            auto_fix=kwargs.get('auto_fix', self.auto_fix),
            fix_eval=kwargs.get('fix_eval', self.fix_eval)
        )


class CheckStatus(object):

    FAIL = "FAIL"
    PASS = "PASS"
    WAIT = "WAIT"

    def __init__(self, status=WAIT, error=None, suggests=[]):
        self.status = status
        self.error = error
        self.suggests = suggests



class InitDirFailedErrorMessage(object):

    PATH_ONLY = ': {path}.'
    NOT_EMPTY = ': {path} is not empty.'
    CREATE_FAILED = ': create {path} failed.'
    NOT_DIR = ': {path} is not a directory .'
    PERMISSION_DENIED = ': {path} permission denied .'


DOC_LINK = '<DOC_LINK>'
DOC_LINK_MSG = 'See {}'.format(DOC_LINK if DOC_LINK else "https://www.oceanbase.com/product/ob-deployer/error-codes .")

EC_CONFIG_CONFLICT_PORT = OBDErrorCodeTemplate(1000, 'Configuration conflict {server1}:{port} port is used for {server2}\'s {key}')
EC_CONFLICT_PORT = OBDErrorCodeTemplate(1001, '{server}:{port} port is already used')
EC_FAIL_TO_INIT_PATH = OBDErrorCodeTemplate(1002, 'Fail to init {server} {key}{msg}')
EC_CLEAN_PATH_FAILED = OBDErrorCodeTemplate(1003, 'Fail to clean {server}:{path}')
EC_CONFIG_CONFLICT_DIR = OBDErrorCodeTemplate(1004, 'Configuration conflict {server1}: {path} is used for {server2}\'s {key}')
EC_SOME_SERVER_STOPED = OBDErrorCodeTemplate(1005, 'Some of the servers in the cluster have been stopped')
EC_FAIL_TO_CONNECT = OBDErrorCodeTemplate(1006, 'Failed to connect to {component}')
EC_ULIMIT_CHECK = OBDErrorCodeTemplate(1007, '({server}) {key} must not be less than {need} (Current value: {now})')
EC_FAILED_TO_GET_AIO_NR = OBDErrorCodeTemplate(1008, '({ip}) failed to get fs.aio-max-nr and fs.aio-nr')
EC_NEED_CONFIG = OBDErrorCodeTemplate(1009, '{server} {component} need config: {miss_keys}')
EC_NO_SUCH_NET_DEVICE = OBDErrorCodeTemplate(1010, '{server} No such net interface: {devname}')
EC_AIO_NOT_ENOUGH = OBDErrorCodeTemplate(1011, '({ip}) Insufficient AIO remaining (Avail: {avail}, Need: {need}), The recommended value of fs.aio-max-nr is 1048576')
EC_PARAM_CHECK = OBDErrorCodeTemplate(1012, '{errors}')
EC_SSH_CONNECT = OBDErrorCodeTemplate(1013, '{user}@{ip} connect failed: {message}')
EC_CHECK_STANDBY = OBDErrorCodeTemplate(1015, 'Unable to confirm the primary-standby relationship, rerun with "--ignore-standby" option if you want to proceed despite the risks.')

# error code for observer
EC_OBSERVER_NOT_ENOUGH_MEMORY = OBDErrorCodeTemplate(2000, '({ip}) not enough memory. (Free: {free}, Need: {need})')
EC_OBSERVER_NOT_ENOUGH_MEMORY_ALAILABLE = OBDErrorCodeTemplate(2000, '({ip}) not enough memory. (Available: {available}, Need: {need})')
EC_OBSERVER_NOT_ENOUGH_MEMORY_CACHED = OBDErrorCodeTemplate(2000, '({ip}) not enough memory. (Free: {free}, Buff/Cache: {cached}, Need: {need})')
EC_OBSERVER_CAN_NOT_MIGRATE_IN = OBDErrorCodeTemplate(2001, 'server can not migrate in')
EC_OBSERVER_FAIL_TO_START = OBDErrorCodeTemplate(2002, 'Failed to start {server} observer')
EC_OBSERVER_FAIL_TO_START_WITH_ERR = OBDErrorCodeTemplate(2002, 'Failed to start {server} observer: {stderr}')
EC_OBSERVER_NOT_ENOUGH_DISK = OBDErrorCodeTemplate(2003, '({ip}) {disk} not enough disk space. (Avail: {avail}, Need: {need})')
EC_OBSERVER_NOT_ENOUGH_DISK_4_CLOG = OBDErrorCodeTemplate(2003, '({ip}) {path} not enough disk space for clog. Use redo_dir to set other disk for clog, or reduce the value of datafile_size')
EC_OBSERVER_INVALID_MODFILY_GLOBAL_KEY = OBDErrorCodeTemplate(2004, 'Invalid: {key} is not a single server configuration item')
EC_OBSERVER_FAILED_TO_REGISTER = OBDErrorCodeTemplate(2005, 'Failed to register cluster.')
EC_OBSERVER_FAILED_TO_REGISTER_WITH_DETAILS = OBDErrorCodeTemplate(2005, 'Failed to register cluster. {appname} may have been registered in {obconfig_url}.')
EC_OBSERVER_MULTI_NET_DEVICE = OBDErrorCodeTemplate(2006, '{ip} has more than one network interface. Please set `devname` for ({server})')
EC_OBSERVER_PING_FAILED = OBDErrorCodeTemplate(2007, '{ip1} {devname} fail to ping {ip2}. Please check configuration `devname`')
EC_OBSERVER_TIME_OUT_OF_SYNC = OBDErrorCodeTemplate(2008, 'Cluster clocks are out of sync')
EC_OBSERVER_PRODUCTION_MODE_LIMIT = OBDErrorCodeTemplate(2009, '({server}): when production_mode is True, {key} can not be less then {limit}')
EC_OBSERVER_SYS_MEM_TOO_LARGE = OBDErrorCodeTemplate(2010, '({server}): system_memory too large. system_memory must be less than memory_limit/memory_limit_percentage.')
EC_OBSERVER_GET_MEMINFO_FAIL = OBDErrorCodeTemplate(2011, "{server}: fail to get memory info.\nPlease configure 'memory_limit' manually in configuration file")

# error code for test commands
EC_MYSQLTEST_PARSE_CMD_FAILED = OBDErrorCodeTemplate(3000, 'parse cmd failed: {path}')
EC_MYSQLTEST_FAILE_NOT_FOUND = OBDErrorCodeTemplate(3001, '{file} not found in {path}')
EC_TPCC_LOAD_DATA_FAILED = OBDErrorCodeTemplate(3002, 'Failed to load data.')
EC_TPCC_RUN_TEST_FAILED = OBDErrorCodeTemplate(3003, 'Failed to run TPC-C benchmark.')

# error code for other components.
# obagent
EC_OBAGENT_RELOAD_FAILED = OBDErrorCodeTemplate(4000, 'Fail to reload {server}')
EC_OBAGENT_SEND_CONFIG_FAILED = OBDErrorCodeTemplate(4001, 'Fail to send config file to {server}')
# obproxy
EC_OBPROXY_NEED_CONFIG = OBDErrorCodeTemplate(4100, '{server} need config "rs_list" or "obproxy_config_server_url"')
EC_OBPROXY_START_FAILED = OBDErrorCodeTemplate(4101, 'failed to start {server} obproxy: {stderr}')
# grafana
EC_GRAFANA_DEFAULT_PWD = OBDErrorCodeTemplate(4200, "{server} grafana admin password should not be 'admin'")
EC_GRAFANA_PWD_LESS_5 = OBDErrorCodeTemplate(4201, "{server} grafana admin password length should not be less than 5")
# ocp express
EC_OCP_EXPRESS_JAVA_NOT_FOUND = OBDErrorCodeTemplate(4300, "{server}: failed to query java version, you may not have java installed")
EC_OCP_EXPRESS_JAVA_VERSION_ERROR = OBDErrorCodeTemplate(4301, "{server}: ocp-express need java with version {version}")
EC_OCP_EXPRESS_NOT_ENOUGH_MEMORY = OBDErrorCodeTemplate(4302, '({ip}) not enough memory. (Free: {free}, Need: {need})')
EC_OCP_EXPRESS_NOT_ENOUGH_MEMORY_AVAILABLE = OBDErrorCodeTemplate(4302, '({ip}) not enough memory. (Available: {available}, Need: {need})')
EC_OCP_EXPRESS_NOT_ENOUGH_MEMORY_CACHED = OBDErrorCodeTemplate(4302, '({ip}) not enough memory. (Free: {free}, Buff/Cache: {cached}, Need: {need})')
EC_OCP_EXPRESS_NOT_ENOUGH_DISK = OBDErrorCodeTemplate(4303, '({ip}) {disk} not enough disk space. (Avail: {avail}, Need: {need})')
EC_OCP_EXPRESS_DEPENDS_COMP_VERSION = OBDErrorCodeTemplate(4304, 'OCP express {ocp_express_version} needs to use {comp} with version {comp_version} or above')
EC_OCP_EXPRESS_META_DB_NOT_ENOUGH_LOG_DISK_AVAILABLE = OBDErrorCodeTemplate(4305, 'There is not enough log disk for ocp meta tenant. (Avail: {avail}, Need: {need})')
EC_OCP_EXPRESS_META_DB_NOT_ENOUGH_LOG_DISK = OBDErrorCodeTemplate(4305, 'There is not enough log disk for ocp meta tenant.')
EC_OCP_EXPRESS_META_DB_NOT_ENOUGH_MEM = OBDErrorCodeTemplate(4305, 'There is not enough memory for ocp meta tenant')
EC_OCP_EXPRESS_ADMIN_PASSWD_ERROR = OBDErrorCodeTemplate(4306, '({ip}) ocp-express admin_passwd invalid.(Current :{current})')
# 4350-4399 had been used by ocp

#ob-configserver
EC_OBC_PROGRAM_START_ERROR = OBDErrorCodeTemplate(4401, 'Failed to start {server} ob-configserver.')
EC_OBC_VIP_SET_ERROR = OBDErrorCodeTemplate(4402, '{server} ob-configserver config error: vip_address and vip_port must be set together')
EC_OBC_CONNECTION_URL_EMPTY = OBDErrorCodeTemplate(4402, '{server} ob-configserver config error: connection_url is empty')
EC_OBC_CONNECTION_URL_ERROR = OBDErrorCodeTemplate(4402, '{server} ob-configserver config error: connection_url must be an absolute path')
EC_OBC_DATABASE_TYPE_ERROR = OBDErrorCodeTemplate(4402, '{server} ob-configserver config error: database_type can only be set to `mysql` or `sqlite3`, and must be in lowercase. ')
EC_OBC_SQLITE_PERMISSION_DENIED = OBDErrorCodeTemplate(4403, '{ip}: {path}: permission denied.')
EC_OBC_DATABASE_CONNECT_ERROR = OBDErrorCodeTemplate(4404, '{server}: failed to connect to database: {url}')



# sql
EC_SQL_EXECUTE_FAILED = OBDErrorCodeTemplate(5000, "{sql} execute failed")

# obdiag
EC_OBDIAG_NOT_FOUND = OBDErrorCodeTemplate(6000, 'Failed to executable obdiag command, you may not have obdiag installed')
EC_OBDIAG_NOT_CONTAIN_DEPEND_COMPONENT = OBDErrorCodeTemplate(6001, 'obdiag must contain depend components {components}')
EC_OBDIAG_OPTIONS_FORMAT_ERROR = OBDErrorCodeTemplate(6002, 'obdiag options {option} format error, please check the value : {value}')

# Unexpected exceptions code
EC_UNEXPECTED_EXCEPTION = OBDErrorCodeTemplate(9999, 'Unexpected exception: need to be posted on "https://ask.oceanbase.com", and we will help you resolve them.')

# WARN CODE 
WC_ULIMIT_CHECK = OBDErrorCodeTemplate(1007, '({server}) The recommended number of {key} is {need} (Current value: {now})')
WC_AIO_NOT_ENOUGH = OBDErrorCodeTemplate(1011, '({ip}) The recommended value of fs.aio-max-nr is 1048576 (Current value: {current})')
WC_OBSERVER_SAME_DISK = OBDErrorCodeTemplate(1012, '({ip}) clog and data use the same disk ({disk})')
WC_OBSERVER_SYS_MEM_TOO_LARGE = OBDErrorCodeTemplate(2010, '({server}): system_memory too large. system_memory should be less than {factor} * memory_limit/memory_limit_percentage.')
WC_OCP_EXPRESS_FAILED_TO_GET_DISK_INFO = OBDErrorCodeTemplate(4303, '({ip}) failed to get disk information, skip disk space check')

# SUGGESTION for ERROR
SUG_SET_CONFIG = OBDErrorSuggestionTemplate('Please set config {key} correctly')
SUG_INCREASE_CONFIG = OBDErrorSuggestionTemplate('Please increase the {key} in configuration')
SUG_DECREASE_CONFIG = OBDErrorSuggestionTemplate('Please decrease the {key} in configuration')
SUG_PORT_CONFLICTS = OBDErrorSuggestionTemplate('Please adjust the configuration to avoid port conflicts')
SUG_USE_OTHER_PORT = OBDErrorSuggestionTemplate('Please choose another unoccupied port or terminate the process occupying the port')
SUG_NO_SUCH_NET_DEVIC = OBDErrorSuggestionTemplate('Please set the network interface corresponding to {ip} to `devname`', fix_eval=[FixEval(FixEval.DEL, 'devname')])
SUG_CONFIG_CONFLICT_DIR = OBDErrorSuggestionTemplate('Please specify a new `{key}` for the {server}')
SUG_CONFIRM_OS = OBDErrorSuggestionTemplate('Please confirm whether the deployment node is a compatible operating system')
SUG_SPECIFY_PATH = OBDErrorSuggestionTemplate('Please specify the path again')
SUG_SET_DEVICE = OBDErrorSuggestionTemplate('Please set the correct network device name to devname')
SUG_USE_SEPARATE_DISKS = OBDErrorSuggestionTemplate('Please use separate disks for redo_dir and data_dir')
SUG_USE_ANOTHER_DEVICE = OBDErrorSuggestionTemplate('Please specify {dir} to another disk with enough space')
SUB_SET_NO_PRODUCTION_MODE = OBDErrorSuggestionTemplate('Please set production_mode to false', True, [FixEval(FixEval.SET, 'production_mode', False)])
SUG_CONFIRM_CONFIG_SERVER = OBDErrorSuggestionTemplate('Please confirm that the ob config service is running normally and that obproxy_config_server_url can be connected correctly'),
SUG_USE_RS_LIST = OBDErrorSuggestionTemplate('Instead of using ob config service, please use rs_list configuration in obproxy to proxy observer')
SUG_GRAFANA_PWD = OBDErrorSuggestionTemplate('Grafana password length must be greater than 4 and not "admin"', True, [FixEval(FixEval.DEL, 'login_password', is_global=True)])
SUG_PARAM_CHECK = OBDErrorSuggestionTemplate('Please check your config')
SUG_SSH_FAILED = OBDErrorSuggestionTemplate('Please check user config and network')
SUG_SYSCTL = OBDErrorSuggestionTemplate('Please execute `echo ‘{var}={value}’ >> /etc/sysctl.conf; sysctl -p` as root in {ip}.')
SUG_ULIMIT = OBDErrorSuggestionTemplate('Please execute `echo -e "* soft {name} {value}\\n* hard {name} {value}" >> /etc/security/limits.d/{name}.conf` as root in {ip}. if it dosen\'t work, please check whether UsePAM is yes in /etc/ssh/sshd_config.')
SUG_CONNECT_EXCEPT = OBDErrorSuggestionTemplate('Connection exception or unsupported OS. Please retry or contact us.')
SUG_UNSUPPORT_OS = OBDErrorSuggestionTemplate('It may be an unsupported OS, please contact us for assistance')
SUG_OBSERVER_SYS_MEM_TOO_LARGE = OBDErrorSuggestionTemplate('`system_memory` should be less than {factor} * memory_limit/memory_limit_percentage.', fix_eval=[FixEval(FixEval.DEL, 'system_memory')])
SUG_OBSERVER_NOT_ENOUGH_MEMORY_ALAILABLE = OBDErrorSuggestionTemplate('Please execute `echo 1 > /proc/sys/vm/drop_caches` as root in {ip} to rlease cached.')
SUG_OBSERVER_REDUCE_MEM = OBDErrorSuggestionTemplate('Please reduce the `memory_limit` or `memory_limit_percentage`', fix_eval=[FixEval(FixEval.DEL, 'memory_limit'), FixEval(FixEval.DEL, 'system_memory'), FixEval(FixEval.DEL, 'memory_limit_percentage')])
SUG_OBSERVER_SAME_DISK = OBDErrorSuggestionTemplate('Configure `redo_dir` and `data_dir` to different disks')
SUG_OBSERVER_NOT_ENOUGH_DISK = OBDErrorSuggestionTemplate('Please reduce the `datafile_size` or `datafile_disk_percentage`', fix_eval=[FixEval(FixEval.DEL, 'datafile_size'), FixEval(FixEval.DEL, 'datafile_disk_percentage')])
SUG_OBSERVER_REDUCE_REDO = OBDErrorSuggestionTemplate('Please reduce the `log_disk_size` or `log_disk_percentage`', fix_eval=[FixEval(FixEval.DEL, 'log_disk_size'), FixEval(FixEval.DEL, 'log_disk_percentage')])
SUG_OBSERVER_NOT_ENOUGH_DISK_4_CLOG = OBDErrorSuggestionTemplate('Please increase the `clog_disk_utilization_threshold` and `clog_disk_usage_limit_percentage`', fix_eval=[FixEval(FixEval.DEL, 'clog_disk_utilization_threshold'), FixEval(FixEval.DEL, 'clog_disk_usage_limit_percentage')])
SUG_OBSERVER_TIME_OUT_OF_SYNC = OBDErrorSuggestionTemplate('Please enable clock synchronization service')
SUG_OCP_EXPRESS_INSTALL_JAVA_WITH_VERSION = OBDErrorSuggestionTemplate('Please install java with version {version}. If java is already installed, please set `java_bin` to the expected java binary path')
SUG_OCP_EXPRESS_NOT_ENOUGH_MEMORY_AVALIABLE = OBDErrorSuggestionTemplate('Please execute `echo 1 > /proc/sys/vm/drop_caches` as root in {ip} to rlease cached.')
SUG_OCP_EXPRESS_REDUCE_MEM = OBDErrorSuggestionTemplate('Please reduce the `memory_size`', fix_eval=[FixEval(FixEval.DEL, 'memory_size')])
SUG_OCP_EXPRESS_REDUCE_DISK = OBDErrorSuggestionTemplate('Please reduce the `logging_file_total_size_cap`', fix_eval=[FixEval(FixEval.DEL, 'logging_file_total_size_cap')])
SUG_OCP_EXPRESS_COMP_VERSION = OBDErrorSuggestionTemplate('Please use {comp} with version {version} or above')
SUG_OCP_EXPRESS_REDUCE_META_DB_MEM = OBDErrorSuggestionTemplate('Please reduce the `ocp_meta_tenant_memory_size`', fix_eval=[FixEval(FixEval.DEL, 'ocp_meta_tenant_memory_size')])
SUG_OCP_EXPRESS_REDUCE_META_DB_LOG_DISK = OBDErrorSuggestionTemplate('Please reduce the `ocp_meta_tenant_log_disk_size`', fix_eval=[FixEval(FixEval.DEL, 'ocp_meta_tenant_log_disk_size')])
SUG_OCP_EXPRESS_EDIT_ADMIN_PASSWD_ERROR = OBDErrorSuggestionTemplate('Please edit the `admin_passwd`, must be 8 to 32 characters in length, and must contain at least two digits, two uppercase letters, two lowercase letters, and two of the following special characters:~!@#%^&*_-+=|(){{}}[]:;,.?/)', fix_eval=[FixEval(FixEval.DEL, 'admin_passwd')], auto_fix=True)