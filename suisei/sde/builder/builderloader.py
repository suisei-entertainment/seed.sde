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
Contains the implementation of the BuilderLoader class.
"""

# Platform Imports
import os
import logging

# SEED Imports
from suisei.seed.exceptions import InvalidInputError

# SDE Imports
from .buildtypes import BuildTypes
from .artifactorybuilder import ArtifactoryBuilderConfig
from .cmakebuilder import CMakeBuilderConfig
from .contentbuilder import ContentBuilderConfig
from .debbuilder import DebBuilderConfig
from .dockerbuilder import DockerBuilderConfig
from .makebuilder import MakeBuilderConfig
from .multistagebuilder import MultiStageBuilderConfig
from .protobufbuilder import ProtobufBuilderConfig
from .pythonbuilder import PythonBuilderConfig
from .sphinxbuilder import SphinxBuilderConfig
from .versionbumperbuilder import VersionBumperBuilderConfig

class BuilderLoader:

    """
    Utility class that loads the loader configuration of a given component
    descriptor.

    Authors:
        Attila Kovacs
    """

    def __init__(self, component: 'ComponentDescriptor'):

        """
        Creates a new BuilderLoader instance.

        Args:
            component:  The component that is using this class to load
                        builders.

        Authors:
            Attila Kovacs
        """

        # The component the descriptor belongs to.
        self._component = component

    def load(self, descriptor: dict):

        """
        Loads the builder configuration from the given descriptor.

        Args:
            descriptor:     The builder descriptor to load.

        Authors:
            Attila Kovacs
        """

        try:

            build_type = descriptor['build']['type'].lower()

            # Identify and load the builder configuration for the component
            if build_type == 'cmake':
                self._load_cmake_builder(descriptor)
            elif build_type == 'make':
                self._load_make_builder(descriptor)
            elif build_type == 'protobuf':
                self._load_protobuf_builder(descriptor)
            elif build_type == 'sphinx':
                self._load_sphinx_builder(descriptor)
            elif build_type == 'artifactory':
                self._load_artifactory_builder(descriptor)
            elif build_type == 'python':
                self._load_python_builder(descriptor)
            elif build_type == 'deb':
                self._load_deb_builder(descriptor)
            elif build_type == 'docker':
                self._load_docker_builder(descriptor)
            elif build_type == 'multistage':
                self._load_multistage_builder(descriptor)
            elif build_type == 'content':
                self._load_content_builder(descriptor)
            elif build_type == 'versionbumper':
                self._load_versionbumper_builder(descriptor)
            else:
                raise InvalidInputError(
                    'Invalid build type {} was specified in the configuration '
                    'file.'.format(build_type))
        except KeyError:
            logger = logging.getLogger('suisei.sde')
            logger.debug('Build configuration was not found for component '
                         '%s', self._component._id)
            self._component._build_type = BuildTypes.UNKNOWN
            self._component._build_target = ''

    def _load_cmake_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a CMake builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.CMAKE

        builder_config = CMakeBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_make_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a Make builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.MAKE

        builder_config = MakeBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_protobuf_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a Protocol Buffers builder from the
        component descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.PROTOBUF

        builder_config = ProtobufBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_sphinx_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a Sphinx builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.SPHINX

        builder_config = SphinxBuilderConfig(
            target=descriptor['build']['target'],
            sourcepath=descriptor['build']['sourcepath'],
            targetpath=descriptor['build']['targetpath'])

        self._component.set_builder_config(builder_config)

    def _load_artifactory_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of an Artifactory builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.ARTIFACTORY

        builder_config = ArtifactoryBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_python_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a Python builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.PYTHON

        builder_config = PythonBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_deb_builder(self, escriptor: dict) -> None:

        """
        Loads the configuration of a deb builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.DEB

        builder_config = DebBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_docker_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a Docker builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.DOCKER

        builder_config = DockerBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_multistage_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a multistage builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.MULTISTAGE

        builder_config = MultiStageBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_content_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a content builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.CONTENT

        builder_config = ContentBuilderConfig()

        self._component.set_builder_config(builder_config)

    def _load_versionbumper_builder(self, descriptor: dict) -> None:

        """
        Loads the configuration of a version bumper builder from the component
        descriptor.

        Args:
            descriptor:     The component descriptor from the configuration
                            file.

        Authors:
            Attila Kovacs
        """

        self._component._build_type = BuildTypes.VERSIONBUMPER

        builder_config = VersionBumperBuilderConfig()

        self._component.set_builder_config(builder_config)
