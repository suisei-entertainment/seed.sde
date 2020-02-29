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
Contains the implementation of the SDE coverage test executor.
"""

# Platform Imports
import logging

# SDE Imports
from suisei.sde.executor.executor import Executor

class CoverageExecutor(Executor):

    """
    Utility class to execute the test coverage tool and generate reports.

    Authors:
        Attila Kovacs
    """

    def execute(self) -> None:

        """
        Executes the coverage test.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')

        # Running coverage test
        logger.debug('Running unit tests with coverage enabled...')
        if self._subprocess_call(
                'coverage run -m suisei.sde --unit-test all',
                invoke_shell=True):
            logger.debug('All unit tests has been executed.')
        else:
            logger.error('Failed to execute unit tests.')

        # Display report
        logger.debug('Generating report...')
        if self._subprocess_call('coverage report', invoke_shell=True):
            logger.debug('Report generated.')
        else:
            logger.error('Failed to generate unit test report.')

        # Write HTML report
        logger.debug('Generating HTML report...')
        if self._subprocess_call('coverage html', invoke_shell=True):
            logger.debug('HTML report was generated.')
        else:
            logger.error('Failed to generate HTML report.')
