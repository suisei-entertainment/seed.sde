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
Contains the implementation of the VersionBumperBuilder class.
"""

# Platform Imports
import os
import logging
import subprocess

# SDE Imports
from .builder import Builder

# SEED Imports
from suisei.seed.utils import JsonFile, ProductVersion

class VersionBumperBuilderConfig:

    """
    Utility class that contains the builder configuration of a version bumper
    builder.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 target: str,
                 major: str = None,
                 minor: str = None,
                 patch: str = None,
                 build: str = None,
                 release: str = None,
                 codename: str = None) -> None:

        """
        Creates a new VersionBumperBuilderConfig instance.

        Args:
            target:     Path to the version file to update
            major:      The major version to set
            minor:      The minor version to set
            patch:      The patch level to set
            build:      The build number to set
            release:    The release type
            codename:   The codemane of the release

        Authors:
            Attila Kovacs
        """

        # The target version file that will be updated
        self._target = target

        # The major product version
        self._major = major

        # The minor product version
        self._minor = minor

        # The patch level
        self._patch = patch

        # The build number
        self._build = build

        # The release type
        self._release = release

        # The codename of the release
        self._codename = codename

class VersionBumperBuilder(Builder):

    """
    Builder implementation that crates a version descriptor file.

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
        logger.info('Executing version number build for component %s (%s)',
                    self._component.ID,
                    self._component.Name)

        # Check whether the version file already exists or not
        if os.path.isfile(os.path.abspath(self._target)):

            # Load the file into a product version object to serve as base
            version_file = JsonFile(path=os.path.abspath(self._target))
            version_file.load()
            version_data = ProductVersion(version_data=version_file.Content)

            # Update major version if needed
            if self._major == '+':
                version_data.bump_major_version()
            elif self._major is not None:
                version_data.update_major_version(self._major)

            # Updated minor version if needed
            if self._minor == '+':
                version_data.bump_minor_version()
            elif self._minor is not None:
                version_data.update_minor_version(self._minor)

            # Update patch level if needed
            if self._patch == '+':
                version_data.bump_patch_level()
            elif self._patch is not None:
                version_data.update_patch_level(self._patch)

            # Update build number if needed
            if self._build == '+':
                version_data.bump_build_number()
            elif self._build is not None:
                version_data.update_build_number(self._build)

            # Update SCM
            version_data.update_scm(self._get_commit_hash())

            # Update release if needed
            if self._release is not None:
                version_data.update_release(self._release)

            # update codename if needed
            if self._codename is not None:
                version_data.update_codename(self._codename)

            # Save the version file
            version_file.overwrite_content(version_data.serialize())
            version_file.save()

        else:

            # Create a new product version object with the data provided
            # in the constructor
            raw_version_data = \
            {
                'major': self._major,
                'minor': self._minor,
                'patch': self._patch,
                'release': self._release,
                'meta':
                {
                    'codename': self._codename,
                    'scm': self._get_commit_hash(),
                    'build': self._build
                }
            }

            version_data = ProductVersion(version_data=raw_version_data)
            version_file = JsonFile(path=os.path.abspath(self._target))
            version_file.overwrite_content(version_data.serialize())
            version_file.save()

    def _get_commit_hash(self) -> str:

        """
        Retrieves the current Git commit hash to use as a Git revision in
        the product version.
        """

        try:
            git_hash = subprocess.Popen(
                'git rev-parse HEAD',
                stdout=subprocess.PIPE).communicate()[0].strip().decode('ascii')
        except OSError:
            git_hash = 'UNKNOWN'

        return git_hash
