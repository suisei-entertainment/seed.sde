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
Contains the implementation of the top level SDE application class.
"""

# Platform Imports
import os
import json
import logging
import sys
import webbrowser
import glob
import subprocess
from logging.handlers import RotatingFileHandler

# Dependency Imports
import coloredlogs
from termcolor import colored

# SEED Imports
from suisei.seed.utils import ProductVersion, JsonFile
from suisei.seed.exceptions import InvalidInputError

# SDE Imports
from suisei.sde.component import ComponentDescriptor
from suisei.sde.executor.linterexecutor import LinterExecutor
from suisei.sde.executor.coverageexecutor import CoverageExecutor
from suisei.sde.executor.buildexecutor import BuildExecutor
from suisei.sde.executor.unittestexecutor import UnitTestExecutor

class SDE:

    """
    Top level class of the SDE command line utility. Responsible for loading
    the application configuration and starting the requested sub-tool.

    Authors:
        Attila Kovacs
    """

    @property
    def IsDebugMode(self) -> bool:

        """
        Returns whether or not the tool was started in debug mode.

        Authors:
            Attila Kovacs
        """

        return self._debug

    @property
    def Version(self) -> ProductVersion:

        """
        Provides access to the product version of the tool.

        Authors:
            Attila Kovacs
        """

        return self._version

    @property
    def LogDirectory(self) -> str:

        """
        Provides access to the log directory.

        Authors:
            Attila Kovacs
        """

        return self._log_directory

    @property
    def LogFile(self) -> str:

        """
        Provides access to the name of the log file.

        Authors:
            Attila Kovacs
        """

        return self._log_file

    @property
    def LogLevel(self) -> str:

        """
        Provides access to the minimum log level.

        Authors:
            Attila Kovacs
        """

        return self._log_level

    @property
    def Components(self) -> dict:

        """
        Provides access to the components known by SDE.

        Authors:
            Attila Kovacs
        """

        return self._components

    @property
    def DocumentationPath(self) -> str:

        """
        The path to the development documentation.

        Authors:
            Attila Kovacs
        """

        return self._doc_path

    def __init__(self, debug: bool = False) -> None:

        """
        Creates a new SDE instance.

        Args:
            debug:      Whether or not the tool was started in debug mode.

        Authors:
            Attila Kovacs
        """

        self._debug = debug             # Debug mode
        self._version = None            # Product version
        self._log_directory = None      # Path to the logging directory
        self._log_file = None           # Name of the log file
        self._log_level = None          # Minimum log level
        self._components = {}           # List of components
        self._doc_path = None           # Path to the development documentation

        # Load the configuration
        config_path = self._get_config_path()
        self._load_configuration(config_path)

        # Configure logging
        self._configure_logging()

    def execute(self,
                mode: str,
                component: str = None) -> None:

        """
        Executes the requested sub-tool based on command line input.

        Args:
            mode:       The mode in which the tool is launched based on the
                        command line arguments. Possible values:
                            - version:          Displays the tool version.
                            - build:            Executes a build.
                            - unittest:         Executes a unit test.
                            - featuretest:      Executes a feature test.
                            - systemtest:       Executes a system test.
                            - performancetest:  Executes a performance test.
                            - linter:           Executes the linter.
                            - coverage:         Executes the coverage test.
                            - install:          Executes the installer.
                            - opendocs:         Opens the development
                                                documentation.
                            - release:          Executes the release script.
            component:  The name of the component to perform the operation on.

        Authors:
            Attila Kovacs
        """

        # Call the specific handler function based on the mode parameter.
        handler = getattr(self, '_on_execute_' + mode)
        handler(component)

    def get_ut_outdir(self, component: str) -> str:

        """
        Returns the output directory to use for the unit test test report for
        the given component.

        Args:
            component:      Name of the component.

        Returns:
            Absolute path of the directory where the unit test report will be
            saved, or None if the given component was not found.

        Authors:
            Attila Kovacs
        """

        if self.has_component(component):
            return self._components[component].UnitTestOutDir

        return None

    def get_ut_log_format(self, component: str) -> str:

        """
        Returns the format string that will be used in the unit test report for
        the given component.

        Args:
            component:      Name of the component.

        Returns:
            The format string of the component, or None if the given component
            was not found.

        Authors:
            Attila Kovacs
        """

        if self.has_component(component):
            return self._components[component].UnitTestLogFormat

        return None

    def get_ut_verbosity(self, component: str) -> int:

        """
        Returns the verbosity of the unit test executor that will be used in
        the unit test for the given component.

        Args:
            component:      Name of the component.

        Returns:
            The format string of the component, or None if the given component
            was not found.

        Authors:
            Attila Kovacs
        """

        if self.has_component(component):
            return self._components[component].UnitTestVerbosity

        return None

    def has_component(self, component: str) -> bool:

        """
        Returns whether or not the given component is configured in the
        application.

        Args:
            component:      ID of the component to check.

        Returns:
            'True' if the given component exists, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if component in self._components:
            return True

        return False

    def get_test_file_path(self, component: str) -> str:

        """
        Returns the path to the directory where the unit tests of a given
        component are located.

        Args:
            component:      Name of the component.

        Returns:
            A list of absolte paths to the files that contain the unit tests
            of the given component, or None if the given component was not
            found.

        Authors:
            Attila Kovacs
        """

        if self.has_component(component):
            return self._components[component].UnitTestLocation

        return None

    @staticmethod
    def is_virtual_env() -> bool:

        """
        Returns whether or not the application was started inside virtualenv.

        Returns:
            'True' if the application is running inside virtualenv, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        if (hasattr(sys, 'real_prefix')) \
           or (hasattr(sys, 'base_prefix')) \
           and sys.base_prefix != sys.prefix:
            return True

        return False

    def _on_execute_version(self, component: str) -> None:

        """
        Handler function to print the application version when requested
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        del component

        self._print_version()

    def _on_execute_build(self, component: str) -> None:

        """
        Handler function that is called when the build command is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        executor = BuildExecutor(component=component,
                                 application=self)
        executor.execute()

    def _on_execute_unittest(self, component: str) -> None:

        """
        Handler function that is called when the unit test command is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        executor = UnitTestExecutor(component=component,
                                    application=self)
        executor.execute()

    def _on_execute_featuretest(self, component: str) -> None:

        """
        Handler function that is called when the feature test is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        del component

    def _on_execute_systemtest(self, component: str) -> None:

        """
        Handler function that is called when the system test is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        del component

    def _on_execute_performancetest(self, component: str) -> None:

        """
        Handler function that is called when the performance test is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        del component

    def _on_execute_linter(self, component: str) -> None:

        """
        Handler function that is called when the linter option is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        executor = LinterExecutor(application=self)
        executor.execute()

    def _on_execute_coverage(self, component: str) -> None:

        """
        Handler function that is called when the coverage command is selected
        through command line.

        Args:
            component:      The component to perform the command on.

        Authors:
            Attila Kovacs
        """

        executor = CoverageExecutor(application=self)
        executor.execute()

    def _on_execute_install(self, component: str) -> None:

        """
        Handler function that is called when the install command is selected
        through command line.

        Authors:
            Attila Kovacs
        """

        del component

    def _on_execute_release(self, component: str) -> None:

        """
        Handler function that is called when the release command is selected
        through command line.

        Authors:
            Attila Kovacs
        """

        del component

    def _on_execute_opendocs(self, component: str) -> None:

        """
        Handler function that is called when the the opendocs command is
        selected through command line.

        Authors:
            Attila Kovacs
        """

        if not os.path.isfile(self.DocumentationPath):
            raise FileNotFoundError(
                'Documentation was not found on the local system, it was '
                'probably not built yet. Execute sde --build documentation '
                'first.')

        webbrowser.open_new_tab(self.DocumentationPath)

    def _get_config_path(self) -> str:

        """
        Retrieves the configuration path to the config file of the tool.

        By default it will look for the configuration file in the current
        user's home directory. If no configuration file is found there it will
        try the current working directory. If no file is found there either
        then it will create a default configuration file in the user's home
        directory and return the path to it.

        Returns:
            The path to the configuration file as a string.

        Authors:
            Attila Kovacs
        """

        config_path = os.path.abspath(
            os.path.expanduser('~/.sde/sde.conf'))

        if not os.path.isfile(config_path):

            alternate_path = '{}/sde.conf'.format(os.getcwd())
            if os.path.isfile(alternate_path):
                config_path = alternate_path
            else:
                # Create the directory if it doesn't exist
                if not os.path.isdir(os.path.abspath(
                    os.path.expanduser('~/.sde'))):
                    os.makedirs(os.path.abspath(os.path.expanduser(
                        '~/.sde')))
                    os.makedirs(os.path.abspath(os.path.expanduser(
                        '~/.sde/components')))

                # Create the configuration file
                self._create_default_config(config_path)

        return config_path

    @staticmethod
    def _create_default_config(config_path: str) -> None:

        """
        Creates the default configuration for the SDE tool if no configuration
        file was found.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')

        # Default SDE configuation descriptor
        default_config = \
        {
            "version":
            {
                "major": 0,
                "minor": 1,
                "patch": 0,
                "release": "internal",
                "meta":
                {
                    "codename": "Fujin"
                }
            },
            "logging":
            {
                "logfile": "sde.log",
                "logdir": "~/.sde/logs",
                "loglevel": "INFO"
            },
            "documentationpath": "~/.sde/build/doc/development/html/index.html",
            "componentpath": "~/.sde/components/components/"
        }

        # Save config file
        try:
            with open(config_path, 'w') as file:
                json.dump(default_config, file)
        except OSError:
            print('ERROR >>>>> Failed to write the '
                  'default configuration. <<<<< ERROR')

        # Get component configuration
        target_path = os.path.abspath(os.path.expanduser('~/.sde/'))
        current_dir = os.getcwd()
        os.chdir(target_path)

        try:
            command = \
                'git clone '
                'https://github.com/suisei-entertainment/seed.components.git '
                './components'
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as error:
            logger.error('Failed to clone the components repository. '
                'Error: %s', error.returncode)

        os.chdir(os.path.abspath('{}/components'.format(target_path)))

        try:
            command = 'git checkout development'
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as error:
            logger.error('Failed to switch to the development branch. '
                'Error: %s', error.returncode)

        os.chdir(current_dir)

    def _load_configuration(self, config_path: str) -> None:

        """
        Loads the configuration of the tool from disk.

        Args:
            config_path:        Path to the configuration file to load

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')

        content = {}

        with open(config_path, 'r') as config_file:
            content = json.load(config_file)

        # Try to load the product version
        version_data = None
        try:
            version_data = content['version']
        except KeyError:
            raise SystemExit(
                'No version information was found in the configuration file.')

        self._version = ProductVersion(version_data)

        # Load logging configuration
        try:
            self._log_directory = os.path.expanduser(
                content['logging']['logdir'])
            self._log_file = content['logging']['logfile']
            self._log_level = content['logging']['loglevel'].upper()
        except KeyError:
            raise SystemExit(
                'Logging configuration is missing from the configuration file.')

        # Load components
        component_path = ''

        try:
            component_path = content['componentpath']
        except KeyError:
            # Component path not found in the configuration, use the default
            # path
            component_path = '~/.sde/components/components/'

        component_path = os.path.abspath(os.path.expanduser(component_path))
        logger.debug('Loading components from %s...', component_path)

        if not os.path.isdir(component_path):
            raise SystemExit(
                'No component configuration was found under {}'.format(
                    component_path))

        # Load all component descriptors from the component directory
        file_list = glob.glob('{}/*.component'.format(component_path))

        for file in file_list:
            logger.debug('Loading component descriptor %s', file)
            try:
                component_file = JsonFile(path=file)
                component_file.load()
                desc = ComponentDescriptor(descriptor=component_file.Content,
                                           application=self)
                self._components[desc.ID] = desc
                logger.debug('Component %s was added successfully.', desc.ID)
            except InvalidInputError:
                del desc

        # Load documentation path
        try:
            self._doc_path = os.path.expanduser(content['documentationpath'])
        except KeyError:
            raise SystemExit('Documentation path was not found in the '
                             'configuration file.')

    def _configure_logging(self) -> None:

        """
        Configures the logging to be used by SDE.

        Authors:
            Attila Kovacs
        """

        log_mapping = \
        {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'FATAL': logging.FATAL
        }

        # Create the logging directory if it doesn't exist
        if not os.path.isdir(self.LogDirectory):
            os.makedirs(self.LogDirectory)

        # Create the log file
        log_path = os.path.abspath('{}/{}'.format(
            self.LogDirectory, self.LogFile))
        log_file = RotatingFileHandler(
            log_path,
            maxBytes=1024*1024*10,
            backupCount=1)
        log_file.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))

        if self.IsDebugMode:
            log_file.setLevel(logging.DEBUG)
        else:
            log_file.setLevel(log_mapping[self.LogLevel])

        # Configure main logger
        loggers = \
        [
            logging.getLogger('suisei.sde'),
            logging.getLogger('suisei.seed.exception'),
            logging.getLogger('suisei.seed.util'),
            logging.getLogger('suisei.seed.network'),
            logging.getLogger('suisei.seed.protocol'),
            logging.getLogger('suisei.seed.node'),
            logging.getLogger('suisei.seed.configuration'),
            logging.getLogger('suisei.seed.services'),
            logging.getLogger('suisei.seed.processing'),
            logging.getLogger('suisei.seed.pal')
        ]

        for logger in loggers:
            if self.IsDebugMode:
                logger.setLevel(logging.DEBUG)
            else:
                logger.setLevel(log_mapping[self.LogLevel])
            logger.addHandler(log_file)

        # Activate colored logs
        try:
            if self.IsDebugMode:
                coloredlogs.install(level='DEBUG')
            else:
                coloredlogs.install(level=self.LogLevel)
        except ImportError:
            pass # Just silently ignore the missing library

    def _print_version(self) -> None:

        """
        Displays the application version.

        Authors:
            Attila Kovacs
        """

        print('SDE version: {}'.format(
            colored(self._version.VersionString, 'cyan')))
