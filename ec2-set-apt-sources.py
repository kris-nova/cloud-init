#!/usr/bin/python
#
#    Fetch the availabity zone and create the sources.list
#    Copyright (C) 2009 Canonical Ltd.
#
#    Author: Chuck Short <chuck.short@canonical.com>
#            Soren Hansen <soren@canonical.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import subprocess
from Cheetah.Template import Template

import ec2init

SOURCES_LIST = '/etc/apt/sources.list'
GENERATED_SOURCES_LIST = '/var/run/ec2/sources.list'
OUT_OF_THE_WAY_SOURCES_LIST = '/etc/apt/sources.list.moved-by-ec2-init'

def main():
    ec2 = ec2init.EC2Init()

	mirror = ec2.get_mirror_for_availability_zone()

	if not os.path.exists(GENERATED_SOURCES_LIST):
		t = os.popen("lsb_release -cs").read()
		codename = t.strip()

		mp = { 'mirror' : mirror, 'codename' : codename }
		t = Template(file='/etc/ec2-init/templates/sources.list.tmpl', searchList=[mp])
		f = open(GENERATED_SOURCES_LIST, 'w')
		f.write(t.respond())
		f.close()

	if not os.path.exists(OUT_OF_THE_WAY_SOURCES_LIST):
		os.rename(SOURCES_LIST, OUT_OF_THE_WAY_SOURCES_LIST)
		os.symlink(GENERATED_SOURCES_LIST, SOURCES_LIST)
        aptget = subprocess.Popen(['apt-get', 'update'])
        aptget.communicate()

if __name__ == '__main__':
    main()