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

from tool import OrderedDict


def create_takeover_base_config(plugin_context, *args, **kwargs):
    options = plugin_context.options
    host = getattr(options, 'host')
    mysql_port = getattr(options, 'mysql_port')
    root_password = getattr(options, 'root_password')

    config = OrderedDict()
    component_name = 'oceanbase-ce'
    global_config = {
        'mysql_port': mysql_port,
        'root_password': root_password
    }
    config[component_name] = {
        'servers': [host],
        'global': global_config
    }

    user_config = {}
    ssh_key_map = {
        'username': 'ssh_user',
        'ssh_password': 'password',
        'key_file': 'ssh_key_file',
        'port': 'ssh_port'
    }
    for key in ssh_key_map:
        opt = ssh_key_map[key]
        val = getattr(options, opt)
        if val is not None:
            user_config[key] = val
    if user_config:
        config['user'] = user_config
    
    return plugin_context.return_true('takeover_config', config)