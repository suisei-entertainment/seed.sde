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
Entry point of the SEED Development Environment tool.
"""

# Platform Imports
import sys
import argparse
import traceback

# SDE Imports
from suisei.sde.application import SDE

if __name__ == '__main__':

    # Setup command line parser
    PARSER = argparse.ArgumentParser(
        description=\
        'SDE command line utility to automate common development tasks.',
        epilog=\
        'For more information please read the development documentation.',
        usage='sde [options]')

    BUILD_SYSTEM = PARSER.add_argument_group(
        title='Build System',
        description='Contains commands related to the build system.')

    BUILD_SYSTEM.add_argument(
        '--build',
        dest='build',
        action='store',
        help='Executes the build script of the given component.',
        metavar='component')

    TEST_EXECUTOR = PARSER.add_argument_group(
        title='Test Executor',
        description='Contains commands related to the test executor.')

    TEST_EXECUTOR.add_argument(
        '--unit-test',
        dest='unittest',
        action='store',
        help='Executes the unit tests of the given component.',
        metavar='component')

    TEST_EXECUTOR.add_argument(
        '--feature-test',
        dest='featuretest',
        action='store',
        help='Executes the feature tests of the given component.',
        metavar='component')

    TEST_EXECUTOR.add_argument(
        '--system-test',
        dest='systemtest',
        action='store',
        help='Executes the system tests of the given component.',
        metavar='component')

    TEST_EXECUTOR.add_argument(
        '--performance-test',
        dest='performancetest',
        action='store',
        help='Executes the performacne tests of the given component.',
        metavar='component')

    TEST_EXECUTOR.add_argument(
        '--linter',
        dest='linter',
        action='store_true',
        help='Executes the linter.')

    TEST_EXECUTOR.add_argument(
        '--coverage',
        dest='coverage',
        action='store_true',
        help='Executes the coverage test.')

    INSTALLER = PARSER.add_argument_group(
        title='Installer',
        description='Contains commands related to the environment installer')

    INSTALLER.add_argument(
        '--install',
        dest='install',
        action='store_true',
        help='Installs a local development environment.')

    MISC = PARSER.add_argument_group(
        title='Misc',
        description='Additional supported commands')

    MISC.add_argument(
        '-v', '--version',
        dest='version',
        action='store_true',
        help='Displays the current SDE version.',
        default=False)

    MISC.add_argument(
        '-d', '--debug',
        dest='debug',
        action='store_true',
        help='Runs the tool in debug mode for additional '
             'debug logging.',
        default=False)

    MISC.add_argument(
        '--opendocs',
        dest='opendocs',
        action='store_true',
        help='Open the generated documentation in the default browser if '
             'called in a GUI environment.',
        default=False)

    # Parse command line
    ARGS = PARSER.parse_args(sys.argv[1:])

    # Start SDE
    try:
        APP = SDE(debug=ARGS.debug)

        if ARGS.version:
            APP.execute(mode='version')

        if ARGS.build is not None:
            APP.execute(mode='build', component=ARGS.build)

        if ARGS.unittest is not None:
            APP.execute(mode='unittest', component=ARGS.unittest)

        if ARGS.featuretest is not None:
            APP.execute(mode='featuretest', component=ARGS.featuretest)

        if ARGS.systemtest is not None:
            APP.execute(mode='systemtest', component=ARGS.systemtest)

        if ARGS.performancetest is not None:
            APP.execute(mode='performancetest',
                        component=ARGS.performancetest)

        if ARGS.linter:
            APP.execute(mode='linter')

        if ARGS.coverage:
            APP.execute(mode='coverage')

        if ARGS.install:
            APP.execute(mode='install')

        if ARGS.opendocs:
            try:
                APP.execute(mode='opendocs')
            except FileNotFoundError as exception:
                raise SystemExit(exception)

    #pylint: disable=broad-except
    except Exception:
        print('>>>>> UNHANDLED EXCEPTION <<<<<')
        print(traceback.print_exc())
        print('>>>>> :UNHANDLED EXCEPTION: <<<<<')
