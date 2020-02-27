## ============================================================================
##                   **** SEED Virtual Reality Platform ****
##                Copyright (C) 2019-2020, Suisei Entertainment
## ============================================================================
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## ============================================================================

"""
Contains the implementation of the Executor class.
"""

# Platform Imports
import logging
import subprocess

class Executor:

    """
    Base class for all SDE executor implementations.

    Authors:
        Attila Kovacs
    """

    @property
    def Application(self) -> 'SDE':

        """
        The application the executor is attached to.

        Authors:
            Attila Kovacs
        """

        return self._application

    def __init__(self, application: 'SDE') -> None:

        """
        Creates a new executor instance.

        Args:
            application:        The application instance the executor is
                                attached to.

        Authors:
            Attila Kovacs
        """

        self._application = application

    def execute(self) -> None:

        """
        Contains the main execution logic.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            'All implementations of the Executor has to provide an '
            'implementation for execute().')

    @staticmethod
    def _subprocess_call(command: str, invoke_shell: bool = False) -> bool:

        """
        Executes a command as a subprocess call.

        Args:
            command:        The command to execute.
            invoke_shell:   Whether or not a shell should be used.

        Returns:
            'True' if the command was executed successfully, False otherwise.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')
        logger.debug('Executing command: %s', command)

        # Execute the command
        try:
            subprocess.run(command,
                           shell=invoke_shell,
                           check=True)
            return True
        except subprocess.CalledProcessError as error:
            logger.error('Failed to execute command %s. Error: %s',
                         command,
                         error.returncode)

        return False
