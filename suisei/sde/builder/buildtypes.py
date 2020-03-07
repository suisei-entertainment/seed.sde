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
Contains the list of supported builder types.
"""

# Platfrom Imports
from enum import IntEnum

class BuildTypes(IntEnum):

    """
    List of supported build types.

    Authors:
        Attila Kovacs
    """

    UNKNOWN = 0     # Unknown build type

    CMAKE = 1           # CMake build system
    MAKE = 2            # Make build system
    PROTOBUF = 3        # Protobuf compiler
    SPHINX = 4          # Sphinx
    ARTIFACTORY = 5     # Artifactory (retrieve the dependency from
                        # Artifactory)
    PYTHON = 6          # Python build based on PyInstaller
    DEB = 7             # Debian package builder
    DOCKER = 8          # Dockerfile based docker builder
    MULTISTAGE = 9      # Builder with multiple build stages
    CONTENT = 10        # Builder that moves files between locations
    VERSIONBUMPER = 11  # Builder that increases the version number in a given
                        # product version descriptor.
    BASH = 12           # Builder that executes a bash script.
    WHEEL = 13          # Builder that creates Python wheels
    PIP = 14            # Builder that install a Python package through pip.
