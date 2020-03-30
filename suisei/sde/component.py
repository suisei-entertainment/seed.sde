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
Contains the implementation of the component descriptor.
"""

# Platform Imports
import os
import logging
from enum import IntEnum

# SEED Imports
from suisei.seed.exceptions import InvalidInputError

# SEED Imports
from suisei.sde.builder import BuilderLoader, BuildTypes

class ComponentDescriptor:

    """
    Utility class that represents the configuration of a single component.

    Authors:
        Attila Kovacs
    """

    @property
    def ID(self) -> str:

        """
        The unique ID of the component.

        Authors:
            Attila Kovacs
        """

        return self._id

    @property
    def Name(self) -> str:

        """
        The name of the component.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def UnitTestOutDir(self) -> str:

        """
        Path to the directory where unittest logs will be saved.

        Authors:
            Attila Kovacs
        """

        return self._ut_out_dir

    @property
    def UnitTestLogFormat(self) -> str:

        """
        The log format to use in the output file.

        Authors:
            Attila Kovacs
        """

        return self._ut_log_format

    @property
    def UnitTestLocation(self) -> str:

        """
        Path to the directory where the unit tests of the component are
        located.

        Authors:
            Attila Kovacs
        """

        return self._ut_path

    @property
    def UnitTestVerbosity(self) -> int:

        """
        Verbosity of the unit test executor.

        Authors:
            Attila Kovacs
        """

        return self._ut_verbosity

    @property
    def BuildType(self) -> 'BuildTypes':

        """
        The build type of the component.

        Authors:
            Attila Kovacs
        """

        return self._build_type

    @property
    def Dependencies(self) -> list:

        """
        Provides access to the list of build dependencies of the component.

        Authors:
            Attila Kovacs
        """

        return self._dependencies

    @property
    def BuilderConfig(self) -> object:

        """
        Provides access to the builder configuration of the component.

        Authors:
            Attila Kovacs
        """

        return self._builder_config

    @property
    def LinterDirectory(self) -> str:

        """
        The directory where the linter for the component should be executed.

        Authors:
            Attila Kovacs
        """

        return self._linter_directory

    def __init__(self, descriptor: dict, application: 'SDE') -> None:

        """
        Creates a new ComponentDescriptor instance.

        Args:
            descriptor:     The serialized format of the component descriptor.

        Authors:
            Attila Kovacs
        """

        # The application the component is attached to.
        self._application = application

        # Unique component ID
        self._id = None

        # Name of the component
        self._name = None

        # Path to the directory where the unit test logs will be stored.
        self._ut_out_dir = None

        # The log format to use in the unit test logs
        self._ut_log_format = None

        # Path to the directory where the unit tests of the component are
        # located.
        self._ut_path = None

        # Verbosity of the unit test executor.
        self._ut_verbosity = None

        # The build type to use when building the component
        self._build_type = BuildTypes.UNKNOWN

        # List of dependencies that are required to build the component.
        self._dependencies = []

        # The builder configuration to use when building the component.
        self._builder_config = None

        # The diretory where the linter for the component should be executed.
        self._linter_directory = None

        try:
            self._load_from_descriptor(descriptor)
        except InvalidInputError:
            logger = logging.getLogger('suisei.sde')
            logger.error('Failed to parse the component descriptor '
                         'from the configuration.')
            logger.debug('Descriptor: %s', descriptor)
            raise

    def has_dependencies(self) -> bool:

        """
        Returns whether or not the component has any build dependencies.

        Returns:
            'True' if the component has build dependencies, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if self._dependencies:
            return True

        return False

    def get_all_dependencies(self) -> list:

        """
        Returns all direct or indirect dependencies of the component.

        Authors:
            Attila Kovacs
        """

        dep_list = []

        if not self._dependencies:
            return dep_list

        for dependency in self._dependencies:
            component = self._application.Components[dependency]
            dep_list.append(component.ID)
            dep_list.append(component.get_all_dependencies())

        return dep_list

    def set_builder_config(self, builder_config: object) -> None:

        """
        Sets the builder configuration of the component.

        Args:
            builder_config:     The builder configuration to set.

        Authors:
            Attila Kovacs
        """

        self._builder_config = builder_config

    def _load_from_descriptor(self, descriptor: dict) -> None:

        """
        Parses the configuration from the passed in JSON representation.

        Args:
            coniguration:       The configuration as a JSON object.

        Raises:
            InvalidInputError:  Raised when a required element is not found
                                in the configuration.
            InvalidInputError:  Raised when an unsupported build type is
                                specified in the configuration.

        Authors:
            Attila Kovacs
        """

        try:
            self._id = descriptor['id']
        except KeyError:
            logger = logging.getLogger('suisei.sde')
            logger.error('Component ID was not found in descriptor: %s',
                         descriptor)
            raise InvalidInputError(
                'Component ID was not found in descriptor: {}'.format(
                    descriptor))

        try:
            self._name = descriptor['name']
        except KeyError:
            logger = logging.getLogger('suisei.sde')
            logger.warning('Component name was not found for component %s',
                           self._id)
            self._name = 'UNKNOWN'

        try:
            self._ut_out_dir = os.path.expanduser(
                descriptor['unittest']['outdir'])
            self._ut_log_format = descriptor['unittest']['logformat']
            self._ut_path = os.path.abspath(
                descriptor['unittest']['testdir'])
        except KeyError:
            logger = logging.getLogger('suisei.sde')
            logger.debug('Unittest configuration was not found for component '
                         '%s', self._id)

        try:
            self._ut_verbosity = int(descriptor['unittest']['verbosity'])
        except KeyError:
            # Default to verbosity level 1 if the configuration is not present
            # in the configuration file.
            self._ut_verbosity = 1

        try:
            self._linter_directory = os.path.abspath(
                os.path.expanduser(descriptor['linter']['linterdir']))
        except KeyError:
            logger = logging.getLogger('suisei.sde')
            logger.debug('Linter configuration was not found for component '
                         '%s', self._id)
            self._linter_directory = './'

        # Load builder configuration
        loader = BuilderLoader(self)
        loader.load(descriptor)
