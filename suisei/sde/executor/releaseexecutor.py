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
Contains the implementation of the SDE release executor.
"""

# SDE Imports
from suisei.sde.executor.executor import Executor

class ReleaseExecutor(Executor):

    """
    Contains the implementation of the release script executor.

    Authors:
        Attila Kovacs
    """

    def __init__(self, component: str, application: 'SDE') -> None:

        """
        Creates a new ReleaseExecutor instance.

        Args:
            component:          The component which will be released.
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

        return
