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
Contains the implementation of the PipBuilder class.
"""

# Platform Imports
import os
import logging

# SDE Imports
from .builder import Builder

class PipBuilderConfig:

    """
    Utility class that contains the builder configuration of a pip
    builder.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new PipBuilderConfig instance.

        Authors:
            Attila Kovacs
        """

        return

class PipBuilder(Builder):

    """
    Builder implementation that executes a pip installation.

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
