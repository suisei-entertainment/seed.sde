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
Contains the implementation of the ContentBuilder class.
"""

# Platform Imports
import os
import logging

# SDE Imports
from .builder import Builder

class ContentBuilderConfig:

    """
    Utility class that contains the builder configuration of a content
    builder.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new ContentBuilderConfig instance.

        Authors:
            Attila Kovacs
        """

        return

class ContentBuilder(Builder):

    """
    Builder implementation that moves files from one location to another.

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
