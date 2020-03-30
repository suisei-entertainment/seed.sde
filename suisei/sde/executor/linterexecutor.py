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
Contains the implementation of the SDE linter executor.
"""

# Platform Imports
import logging

# Dependency Imports
import pylint.lint

# SDE Imports
from suisei.sde.executor.executor import Executor

class LinterExecutor(Executor):

    """
    Utility class to execute the linter tool and generate reports.

    Authors:
        Attila Kovacs
    """

    def __init__(self, component: str, application: 'SDE') -> None:

        """
        Creates a new LinterExecutor instance.

        Args:
            component:          The component which will be tested.
            application:        The SDE application instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(application)

        self._component = component
        """
        The component to test.
        """

    def execute(self) -> None:

        """
        Executes the linter.

        Authors:
            Attila Kovacs
        """

        result = 0
        logger = logging.getLogger('suisei.sde')

        logger.debug('Executing linter...')

        components = []

        if self._component != 'all':
            components.append(self._application.Components[self._component])
        else:
            components = self._application.Components.values()

        for component in components:
            logger.info('Executing linter for component %s', component.ID)
            lint_dir = component

            print(component.LinterDirectory)

            pylint_opts = \
            [
                '-j 0',
                '--reports=yes',
                '--rcfile=./.pylintrc',
                component.LinterDirectory
            ]

            result = pylint.lint.Run(pylint_opts)

            if result >= 32:
                logger.error('Failed to execute linter.')
            else:
                logger.debug('Linter executed successfully.')
