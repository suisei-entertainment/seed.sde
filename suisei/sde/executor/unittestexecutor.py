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
Contains the implementation of the SDE unittest executor.
"""

# Platform Imports
import logging
import unittest
import os
import shutil

# Dependency Imports
from tap import TAPTestRunner

# SDE Imports
from suisei.sde.executor.executor import Executor

class UnitTestExecutor(Executor):

    """
    Executor implementation to run the unit tests of a component.

    Authors:
        Attila Kovacs
    """

    def __init__(self, component: str, application: 'SDE') -> None:

        """
        Creates a new UnitTestExecutor instance.

        Args:
            component:          The component which will be tested.
            application:        The SDE application instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(application)

        self._test_runner = None
        """
        The test runner used to execute the test.
        """

        self._component = component
        """
        The component to test.
        """

    def execute(self) -> None:

        """
        Executes the tests.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')

        # Prepare the test directory
        self._prepare_directory()

        components = []

        if self._component != 'all':
            components.append(self._component)
        else:
            components = self._application.Components

        test_success = True

        # Disable console logging for SEED loggers
        loggers = \
        [
            logging.getLogger('suisei.seed.exceptions'),
            logging.getLogger('suisei.seed.utils'),
            logging.getLogger('suisei.seed.network'),
            logging.getLogger('suisei.seed.protocol'),
            logging.getLogger('suisei.seed.node'),
            logging.getLogger('suisei.seed.configuration'),
            logging.getLogger('suisei.seed.services'),
            logging.getLogger('suisei.seed.processing'),
            logging.getLogger('suisei.seed.pal')
        ]

        for logger in loggers:
            logger.propagate = False

        # Run the tests
        for component in components:
            logger.info('Executing unit tests for component %s', component)
            self._create_test_runner(component)
            test_suite = self._build_test_suite(component)

            if test_suite:
                result = self._test_runner.run(test_suite)

                if result.errors:
                    test_success = False
                    logger.info('There were test cases finished as ERROR: \n%s',
                                result.errors)
                else:
                    logger.info('No test cases finished as ERROR.')

                if result.failures:
                    test_success = False
                    logger.info('There where test cases finished as FAILURE: '
                                '\n%s', result.failures)
                else:
                    logger.info('No test cases finished as FAILURE.')

        logger.debug('All tests executed.')

        if not test_success:
            raise SystemExit(-1)

    @staticmethod
    def _prepare_directory() -> None:

        """
        Prepare the testfiles directory. Create it if it doesn't exist and
        remove all files from it if it already exists.

        Authors:
            Attila Kovacs
        """

        test_directory = os.path.abspath(os.path.expanduser(
            '~/.sde/testfiles/'))

        if os.path.isdir(test_directory):

            # There is already a testfiles directory, clean it up
            shutil.rmtree(test_directory)

        # Create an empty .testfiles directory
        os.makedirs(test_directory)

    def _create_test_runner(self, component: str) -> None:

        """
        Creates the test runner to use for test execution.

        Args:
            component:      Name of the component to test.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')
        logger.debug('Creating test runner for component %s...', component)

        try:
            descriptor = self._application.Components[component]
        except KeyError:
            logger.error('Component %s was not found', component)
            return

        try:
            self._test_runner = TAPTestRunner(
                verbosity=descriptor.UnitTestVerbosity)
            self._test_runner.set_outdir(descriptor.UnitTestOutDir)
            self._test_runner.set_format(descriptor.UnitTestLogFormat)
            logger.debug('Saving test output to %s',
                         self._application.get_ut_outdir(component))
        except ImportError:
            logger.warning('The TAP test runner is not installed on the host '
                           'system, falling back to the default unit test '
                           'runner.')
            self._test_runner = unittest.TextTestRunner(
                verbosity=descriptor.UnitTestVerbosity)

        logger.debug('Test runner created successfully.')

    def _build_test_suite(self, component: str) -> unittest.TestSuite:

        """
        Builds the test suite for the given component.

        If test coverage is not measured, then we can just use Python's
        built-in test discovery tool to gather the tests to run.

        When test coverage is measured all tests need to be imported manually
        here to avoid coverage missing imports and function definitions.

        Args:
            component:          Name of the component to test.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')
        logger.debug('Building test suite for component %s to execute...',
                     component)

        try:
            descriptor = self._application.Components[component]
        except KeyError:
            logger.error('Component %s was not found', component)
            return

        test_loader = unittest.TestLoader()
        unit_test_path = descriptor.UnitTestLocation

        if unit_test_path is None:
            logger.debug('Component %s has no unit tests.', component)
            return None

        logger.debug('Path to search for test files: %s', unit_test_path)

        logger.debug('Using Python\'s internal test discovery...')
        test_suite = test_loader.discover(
            start_dir=unit_test_path,
            pattern='test_*.py')

        return test_suite
