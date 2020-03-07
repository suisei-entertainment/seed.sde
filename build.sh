#!/bin/bash

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

# Remove previously installed version
pip uninstall -y suisei-sde

# Create binary package
pyinstaller --noconfirm --onefile --clean --hidden-import='pkg_resources.py2_warn' --name sde ./suisei/sde/__main__.py

# Create local install and install it inside the virtual environment
python setup.py sdist bdist_wheel
pip install ./dist/suisei_sde-0.1.0-py3-none-any.whl