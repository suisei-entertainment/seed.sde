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
Contains the implementation of the SphinxBuilder class.
"""

# Platform Imports
import os
import logging

# SDE Imports
from .builder import Builder

class SphinxBuilderConfig:

    """
    Utility class that stores the configuration of a Sphinx builder.

    Authors:
        Attila Kovacs
    """

    @property
    def Target(self) -> str:

        """
        The build target to call in Sphinx.

        Authors:
            Attila Kovacs
        """

        return self._target

    @property
    def SourcePath(self) -> str:

        """
        The path where the documentation sources are located.

        Authors:
            Attila Kovacs
        """

        return self._source_path

    @property
    def TargetPath(self) -> str:

        """
        The path where the generated documentation will be stored.

        Authors:
            Attila Kovacs
        """

        return self._target_path

    def __init__(self,
                 target: str,
                 sourcepath: str,
                 targetpath: str) -> None:

        """
        Creates a new SphinxBuilderConfig instance.

        Args:
            target:     The build target to call in Sphinx
            sourcepath: The path where the documentation sources are located
            targetpath: The path where the generated documentation will be
                        stored.

        Authors:
            Attila Kovacs
        """

        # The build target to call in Sphinx
        self._target = target

        # The path where the documentation sources are located
        self._source_path = os.path.abspath(sourcepath)

        # The path where the generated documentation will be stored
        self._target_path = os.path.abspath(targetpath)

class SphinxBuilder(Builder):

    """
    Builder implementation that executes the Sphinx builder in the given source
    directory.

    Authors:
        Attila Kovacs
    """

    def build(self) -> None:

        """
        Executes the actual component build based on the component descriptor.

        Authors:
            Attila Kovacs
        """

        logger = logging.getLogger('suisei.sde')
        logger.info('Executing documentation build for component %s (%s)',
                    self._component.ID,
                    self._component.Name)

        source_path = os.path.abspath(
            os.path.expanduser(self._component.BuilderConfig.SourcePath))

        target_path = os.path.abspath(
            os.path.expanduser(self._component.BuilderConfig.TargetPath))

        # Go to the source directory
        current_dir = os.getcwd()
        os.chdir(source_path)
        logger.debug('Entering source directory %s',
                     source_path)

        # Create build command
        build_command = 'sphinx-build -b {} \"{}\" \"{}\"'.format(
            self._component.BuilderConfig.Target,
            source_path,
            target_path)
        logger.debug('Executing build command %s', build_command)

        self._subprocess_call(build_command, invoke_shell=True)

        os.chdir(current_dir)
