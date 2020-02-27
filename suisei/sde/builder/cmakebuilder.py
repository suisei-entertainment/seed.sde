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
Contains the implementation of the CMakeBuilder class.
"""

# Platform Imports
import os
import logging

# SDE Imports
from .builder import Builder

class CMakeBuilderConfig:

    """
    Utility class that contains the builder configuration of a CMake
    builder.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new CMakeBuilderConfig instance.

        Authors:
            Attila Kovacs
        """

        return

class CMakeBuilder(Builder):

    """
    Builder implementation that executes CMake in the given source directory.

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
        logger.info('Executing CMake build for component %s (%s)',
                    self._component.ID,
                    self._component.Name)

        # Go to the source directory
        current_dir = os.getcwd()
        os.chdir(self._component.SourePath)
        logger.debug('Entering source directory %s',
                     self._component.SourcePath)

        # Create build command
        build_command = 'cmake -G \"Unix Makefiles\" .'
        logger.debug('Executing build command %s', build_command)

        # Execute the build
        self._subprocess_call(build_command, invoke_shell=True)

        # Move back to the original directory
        os.chdir(current_dir)
