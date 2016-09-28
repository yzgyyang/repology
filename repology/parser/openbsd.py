# Copyright (C) 2016 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import csv

from ..util import SplitPackageNameVersion
from ..package import Package

def SanitizeVersion(version):
    match = re.match("(.*)v[0-9]+$", version)
    if match is not None:
        version = match.group(1)

    match = re.match("(.*)p[0-9]+$", version)
    if match is not None:
        version = match.group(1)

    #pos = version.rfind(',')
    #if pos != -1:
        #version = version[0:pos]

    #pos = version.rfind('_')

    #if pos != -1:
        #version = version[0:pos]

    return version

class OpenBSDIndexParser():
    def __init__(self):
        pass

    def Parse(self, path):
        result = []

        with open(path, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter='|')
            for row in reader:
                pkg = Package()

                pkgname = row[0]

                # cut away string suffixws which come after version
                match = re.match("(.*?)(-[a-z_]+[0-9]*)+$", pkgname)
                if match is not None:
                    pkgname = match.group(1)

                pkg.name, pkg.fullversion = SplitPackageNameVersion(pkgname)
                pkg.version = SanitizeVersion(pkg.fullversion)
                pkg.comment = row[3]
                pkg.maintainers.append(row[5])
                pkg.category = row[6].split(' ')[0]

                result.append(pkg)

        return result
