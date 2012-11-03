#
# LSST Data Management System
# Copyright 2012 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

import re
from lsst.pipe.tasks.ingest import ParseTask

class MegacamParseTask(ParseTask):
    def translate_ccd(self, md):
        if not md.exists("EXTNAME"):
            raise RuntimeError("No EXTNAME in header")
        extname = md.get("EXTNAME").strip()
        if extname[0:3] != "ccd":
            raise RuntimeError("Unrecognised EXTNAME: %s" % extname)
        ccd = int(extname[4:])
        return ccd

    def translate_taiObs(self, md):
        # Field name is "taiObs" but we're giving it UTC; shouldn't matter so long as we're consistent
        return "%sT%s" % (md.get("DATE-OBS").strip(), md.get("UTC-OBS").strip())

    def getInfo(self, filename):
        phuInfo, infoList = super(MegacamParseTask, self).getInfo(filename)
        match = re.search(r"\d+(?P<state>o|p)\.fits.*", filename)
        if not match:
            raise RuntimeError("Unable to parse filename: %s" % filename)
        phuInfo['state'] = match.group('state')
        for info in infoList:
            info['state'] = match.group('state')
        return phuInfo, infoList
