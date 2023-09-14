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

from _errno import EC_CLEAN_PATH_FAILED


def destroy(plugin_context, *args, **kwargs):
    cluster_config = plugin_context.cluster_config
    clients = plugin_context.clients
    stdio = plugin_context.stdio
    global_ret = True
    stdio.start_loading('ob-configserver work dir cleaning')

    for server in cluster_config.servers:
        server_config = cluster_config.get_server_conf(server)
        stdio.verbose('%s work path cleaning' % server)
        client = clients[server]
        home_path = server_config['home_path']
        ret = client.execute_command('rm -fr %s/' % (home_path), timeout=-1)
        if not ret:
            stdio.warn(EC_CLEAN_PATH_FAILED.format(server=server, path=home_path))
            global_ret = False
        else:
            stdio.verbose('%s:%s cleaned' % (server, home_path))
    if not global_ret:
        stdio.stop_loading('fail')
    else:
        stdio.stop_loading('succeed')
        plugin_context.return_true()
