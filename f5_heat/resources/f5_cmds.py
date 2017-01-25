# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import logging

from heat.common import exception
from heat.common.i18n import _
from heat.engine import properties
from heat.engine import resource

from common.mixins import f5_bigip
from common.mixins import F5BigIPMixin


class F5SysCmds(resource.Resource, F5BigIPMixin):
    '''Sync the device configuration to the device group.'''

    PROPERTIES = (
        BIGIP_SERVER,
        CREATE_COMMANDS,
        UPDATE_COMMANDS,
        DELETE_COMMANDS
    ) = (
        'bigip_server',
        'create_commands',
        'update_commands',
        'delete_commands'
    )

    properties_schema = {
        BIGIP_SERVER: properties.Schema(
            properties.Schema.STRING,
            _('Reference to the BigIP Server resource.'),
            required=True,
            immutable=True
        ),
        CREATE_COMMANDS: properties.Schema(
            properties.Schema.LIST,
            _('List of commands to run when resource created.'),
            required=False,
            immutable=True,
            default=[]
        ),
        UPDATE_COMMANDS: properties.Schema(
            properties.Schema.LIST,
            _('List of commands to run when resource updated.'),
            required=False,
            immutable=True,
            default=[]
        ),
        DELETE_COMMANDS: properties.Schema(
            properties.Schema.LIST,
            _('List of commands to run when resource deleted.'),
            required=False,
            immutable=True,
            default=[]
        )
    }

    @f5_bigip
    def handle_create(self):
        '''Run commands on the BIG-IP® device when resource created.

        :raises: ResourceFailure exception
        '''
        try:
            create_commands = self.properties[self.CREATE_COMMANDS]
            for cmd in create_commands:
                bash_cmd = "-c '%s'" % cmd
                logging.debug("Issuing Command: %s" % bash_cmd)
                response = self.bigip.tm.util.bash.exec_cmd(
                    'run', utilCmdArgs=bash_cmd)
                if hasattr(response, 'CommandResult'):
                    logging.debug(
                        "Command: %s Response: %s" % (bash_cmd,
                                                      response.commandResult)
                    )
        except Exception:
            rtex = Exception(
                "Following command: %s failed." % cmd
            )
            raise exception.ResourceFailure(rtex, None, action='CREATE')
        return True

    @f5_bigip
    def handle_update(self):
        '''Run commands on the BIG-IP® device when resource updated.

        :raises: ResourceFailure exception
        '''

        try:
            update_commands = self.properties[self.UPDATE_COMMANDS]
            for cmd in update_commands:
                bash_cmd = "-c '%s'" % cmd
                logging.debug("Issuing Command: %s" % bash_cmd)
                response = self.bigip.tm.util.bash.exec_cmd(
                    'run', utilCmdArgs=bash_cmd)
                if hasattr(response, 'CommandResult'):
                    logging.debug(
                        "Command: %s Response: %s" % (bash_cmd,
                                                      response.commandResult)
                    )
        except Exception:
            rtex = Exception(
                "Following command: %s failed." % cmd
            )
            raise exception.ResourceFailure(rtex, None, action='UPDATE')
        return True

    @f5_bigip
    def handle_delete(self):
        '''Run commands on the BIG-IP® device when resource deleted.

        :raises: ResourceFailure exception
        '''
        if not hasattr(self, 'bigip'):
            return True

        try:
            delete_commands = self.properties[self.DELETE_COMMANDS]
            for cmd in delete_commands:
                bash_cmd = "-c '%s'" % cmd
                logging.debug("Issuing Command: %s" % bash_cmd)
                response = self.bigip.tm.util.bash.exec_cmd(
                    'run', utilCmdArgs=bash_cmd)
                if hasattr(response, 'CommandResult'):
                    logging.debug(
                        "Command: %s Response: %s" % (bash_cmd,
                                                      response.commandResult)
                    )
        except Exception:
            rtex = Exception(
                "Following command: %s failed." % cmd
            )
            raise exception.ResourceFailure(rtex, None, action='DELETE')
        return True


def resource_mapping():
    return {'F5::Sys::Cmds': F5SysCmds}
