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
Contains the implementation of the BuildExecutor class.
"""

# SDE Imports
from suisei.sde.component import ComponentDescriptor

from suisei.sde.builder import (
    BuildTypes,
    ArtifactoryBuilder,
    CMakeBuilder,
    MakeBuilder,
    ProtobufBuilder,
    SphinxBuilder,
    PythonBuilder,
    DebBuilder,
    DockerBuilder,
    MultiStageBuilder,
    ContentBuilder)

from .executor import Executor

class BuildExecutor(Executor):

    """
    Contains common executor implementation for build executors.

    Authors:
        Attila Kovacs
    """

    def __init__(self, component: str, application: 'SDE') -> None:

        """
        Creates a new BuildExecutor instance.

        Args:
            component:          The component which will be tested.
            application:        The SDE application instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(application)

        # Name of the component to build
        if not self._application.has_component(component):
            raise RuntimeError('Component {} does not exist.'.format(component))

        self._component = self._application.Components[component]

    def execute(self) -> None:

        """
        Contains the main execution logic.

        Authors:
            Attila Kovacs
        """

        if self._component.has_dependencies():
            self.build_dependencies()

        self.execute_build(self._component)

    @staticmethod
    def execute_build(component: ComponentDescriptor) -> None:

        """
        Executes the actual build.

        Args:
            component:      The component descriptor to build.

        Authors:
            Attila Kovacs
        """

        builder = None

        if component.BuildType == BuildTypes.CMAKE:
            builder = CMakeBuilder(component)
        elif component.BuildType == BuildTypes.MAKE:
            builder = MakeBuilder(component)
        elif component.BuildType == BuildTypes.PROTOBUF:
            builder = ProtobufBuilder(component)
        elif component.BuildType == BuildTypes.SPHINX:
            builder = SphinxBuilder(component)
        elif component.BuildType == BuildTypes.ARTIFACTORY:
            builder = ArtifactoryBuilder(component)
        elif component.BuildType == BuildTypes.PYTHON:
            builder = PythonBuilder(component)
        elif component.BuildType == BuildTypes.DEB:
            builder = DebBuilder(component)
        elif component.BuildType == BuildTypes.DOCKER:
            builder = DockerBuilder(component)
        elif component.BuildType == BuildTypes.MULTISTAGE:
            builder = MultiStageBuilder
        elif component.BuildType == BuildTypes.CONTENT:
            builder = ContentBuilder

        builder.build()

    def build_dependencies(self) -> None:

        """
        Builds any dependencies associated with the project.

        Authors:
            Attila Kovacs
        """

        # Get a list with all dependencies
        dep_list = list(dict.fromkeys(self._component.get_all_dependencies()))

        for dependency in dep_list:
            component = self._application.Components[dependency]
            self.execute_build(component)
