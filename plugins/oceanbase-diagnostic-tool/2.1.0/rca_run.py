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
from ssh import LocalClient
import _errno as err
import os


def rca_run(plugin_context, *args, **kwargs):
    def get_option(key, default=''):
        value = getattr(options, key)
        if value is None:
            value = default
        stdio.verbose('get option: %s value %s' % (key, value))
        return value

    def local_execute_command(command, env=None, timeout=None):
        command = r"{install_dir}/obdiag".format(install_dir=obdiag_install_dir)
        return LocalClient.execute_command(command, env, timeout, stdio)

    def get_obdiag_cmd():
        base_commond=r"{install_dir}/obdiag rca run --scene={scene}".format(install_dir=obdiag_install_dir, scene=scene_option)
        cmd = r"{base}".format(
            base=base_commond,
        )
        if store_dir_option:
            cmd = cmd + r" --store_dir {store_dir}".format(store_dir=store_dir_option)
        if parameters_option:
            cmd = cmd + r" --input_parameters '{input_parameters}'".format(input_parameters=parameters_option)
        return cmd

    def run():
        obdiag_cmd = get_obdiag_cmd()
        stdio.verbose('execute cmd: {}'.format(obdiag_cmd))
        return LocalClient.run_command(obdiag_cmd, env=None, stdio=stdio)

    options = plugin_context.options
    obdiag_bin = "obdiag"
    stdio = plugin_context.stdio
    obdiag_install_dir = get_option('obdiag_dir')
    scene_option = get_option('scene')
    if not scene_option:
        stdio.error("failed get --scene option, example: obd obdiag rca run {0} --scene <scene_name> ".format(plugin_context.deploy_name))
        return plugin_context.return_false() 
    parameters_option = get_option('input_parameters')
    store_dir_option = os.path.abspath(get_option('store_dir'))

    ret = local_execute_command('%s --help' % obdiag_bin)
    if not ret:
        stdio.error(err.EC_OBDIAG_NOT_FOUND.format())
        return plugin_context.return_false()
    try:
        if run():
            plugin_context.return_true()
    except KeyboardInterrupt:
        stdio.exception("obdiag rca run failed")
        return plugin_context.return_false()