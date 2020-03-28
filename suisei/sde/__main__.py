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

def main():

    # Setup command line parser
    parser = argparse.ArgumentParser(
        description=\
        'SDE command line utility to automate common development tasks.',
        epilog=\
        'For more information please read the development documentation.',
        usage='sde [options]')

    build_system = parser.add_argument_group(
        title='Build System',
        description='Contains commands related to the build system.')

    build_system.add_argument(
        '--build',
        dest='build',
        action='store',
        help='Executes the build script of the given component.',
        metavar='component')

    test_executor = parser.add_argument_group(
        title='Test Executor',
        description='Contains commands related to the test executor.')

    test_executor.add_argument(
        '--unit-test',
        dest='unittest',
        action='store',
        help='Executes the unit tests of the given component.',
        metavar='component')

    test_executor.add_argument(
        '--feature-test',
        dest='featuretest',
        action='store',
        help='Executes the feature tests of the given component.',
        metavar='component')

    test_executor.add_argument(
        '--system-test',
        dest='systemtest',
        action='store',
        help='Executes the system tests of the given component.',
        metavar='component')

    test_executor.add_argument(
        '--performance-test',
        dest='performancetest',
        action='store',
        help='Executes the performacne tests of the given component.',
        metavar='component')

    test_executor.add_argument(
        '--linter',
        dest='linter',
        action='store_true',
        help='Executes the linter.')

    test_executor.add_argument(
        '--coverage',
        dest='coverage',
        action='store',
        help='Executes the coverage test.')

    installer = parser.add_argument_group(
        title='Installer',
        description='Contains commands related to the environment installer')

    installer.add_argument(
        '--install',
        dest='install',
        action='store_true',
        help='Installs a local development environment.')

    releaser = parser.add_argument_group(
        title='Release Management',
        description='Contains commands related to the release management '
                    'utilities.')

    releaser.add_argument(
        '--release',
        dest='release',
        action='store',
        help='Creates a new release version with the given version number.')

    misc = parser.add_argument_group(
        title='Misc',
        description='Additional supported commands')

    misc.add_argument(
        '-v', '--version',
        dest='version',
        action='store_true',
        help='Displays the current SDE version.',
        default=False)

    misc.add_argument(
        '-d', '--debug',
        dest='debug',
        action='store_true',
        help='Runs the tool in debug mode for additional '
             'debug logging.',
        default=False)

    misc.add_argument(
        '--opendocs',
        dest='opendocs',
        action='store_true',
        help='Open the generated documentation in the default browser if '
             'called in a GUI environment.',
        default=False)

    # Parse command line
    args = parser.parse_args(sys.argv[1:])

    # Start SDE
    try:
        app = SDE(debug=args.debug)

        if args.version:
            app.execute(mode='version')

        if args.build is not None:
            app.execute(mode='build', component=args.build)

        if args.unittest is not None:
            app.execute(mode='unittest', component=args.unittest)

        if args.featuretest is not None:
            app.execute(mode='featuretest', component=args.featuretest)

        if args.systemtest is not None:
            app.execute(mode='systemtest', component=args.systemtest)

        if args.performancetest is not None:
            app.execute(mode='performancetest',
                        component=args.performancetest)

        if args.linter:
            app.execute(mode='linter')

        if args.coverage:
            app.execute(mode='coverage')

        if args.install:
            app.execute(mode='install')

        if args.release is not None:
            app.execute(mode='release', component=args.release)

        if args.opendocs:
            try:
                app.execute(mode='opendocs')
            except FileNotFoundError as exception:
                raise SystemExit(exception)

    #pylint: disable=broad-except
    except Exception:
        print('>>>>> UNHANDLED EXCEPTION <<<<<')
        print(traceback.print_exc())
        print('>>>>> :UNHANDLED EXCEPTION: <<<<<')

if __name__ == '__main__':
    main()
