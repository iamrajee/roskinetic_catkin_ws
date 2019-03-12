# Software License Agreement (BSD License)
#
# Copyright (c) 2014, JSK Robotics Laboratory.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of JSK Robotics Laboratory. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import print_function

from optparse import OptionParser

import os
import sys
import traceback
import genmsg
import genmsg.command_line
from catkin import terminal_color

from catkin_pkg import package, packages, workspaces, topological_order

from genmsg import MsgGenerationException
from . generate import generate_msg, generate_srv

def usage(progname):
    print("%(progname)s file(s)"%vars())

def get_pkg_map():
    pkg_map = {}
    for ws in workspaces.get_spaces():
        pkgs = packages.find_packages(ws)
        for pkg in pkgs.values():
            # packages.find_packages(workspaces.get_spaces()) returns package in high-priority-first-order, so we should not overwirte package map which is already found
            # https://github.com/ros-infrastructure/catkin_pkg/blob/fa4b136b16e2d2886ab97257684f6bff243edefb/src/catkin_pkg/workspaces.py#L43
            # https://github.com/ros-infrastructure/catkin_pkg/blob/fa4b136b16e2d2886ab97257684f6bff243edefb/src/catkin_pkg/packages.py#L71
            if pkg.name not in pkg_map:
                pkg_map[pkg.name] = pkg
    return pkg_map

pkg_map = None
def get_depends(pkg):
    """Get dependencies written as run_depend in package.xml"""
    global pkg_map
    if pkg_map is None:
        pkg_map = get_pkg_map()
    pkg_obj = pkg_map[pkg]
    pkg_xml_path = pkg_obj.filename
    depends = map(lambda x: x.name,
                  package.parse_package(pkg_xml_path).exec_depends)
    depends = list(set(depends))  # for duplicate
    return depends

def package_depends(pkg):  # pkg is string
    global pkg_map
    if pkg_map is None:
        pkg_map = get_pkg_map()
    depends = {}
    depends_impl = package_depends_impl(pkg)
    for d in depends_impl:
        try:
            pkg_obj = pkg_map[d]
            p_path = os.path.dirname(pkg_obj.filename)
            if (os.path.exists(os.path.join(p_path, "msg")) or
                    os.path.exists(os.path.join(p_path, "srv"))):
                depends[d] = pkg_obj
        except Exception as e:
            print(terminal_color.fmt(
                '@{yellow}[WARNING] path to %s is not found') % (pkg))
            print(e)
    return [p.name for n,p in topological_order.topological_order_packages(depends)]

def package_depends_impl(pkg, depends=None): # takes and returns Package object
    if depends is None:
        depends = []
    global pkg_map
    if pkg_map is None:
        pkg_map = get_pkg_map()
    if not pkg in pkg_map:
        print(terminal_color.fmt(
            '@{yellow}[WARNING] %s is not found in workspace') % (pkg))
        return depends
    ros_depends = filter(lambda x: x in pkg_map, get_depends(pkg))
    tmp_depends = filter(lambda x: x not in depends, ros_depends)
    depends.extend(tmp_depends)
    for p in tmp_depends:
        depends = package_depends_impl(p, depends)
    return depends

def genmain(argv, progname):
    parser = OptionParser("%s file"%(progname))
    parser.add_option('-p', dest='package')
    parser.add_option('-o', dest='outdir')
    parser.add_option('-I', dest='includepath', action='append')
    parser.add_option('-m', dest='manifest', action='store_true')
    options, args = parser.parse_args(argv)
    try:
        if len(args) < 2:
            parser.error("please specify args")
        if not os.path.exists(options.outdir):
            # This script can be run multiple times in parallel. We
            # don't mind if the makedirs call fails because somebody
            # else snuck in and created the directory before us.
            try:
                os.makedirs(options.outdir)
            except OSError as e:
                if not os.path.exists(options.outdir):
                    raise
        if options.manifest:
            import datetime
            global pkg_map
            if pkg_map is None:
                pkg_map = get_pkg_map()
            pkg_map = get_pkg_map()
            f = open(options.outdir+'/manifest.l', 'w+')
            f.write(";;\n")
            f.write(";; DO NOT EDIT THIS FILE\n")
            f.write(";;\n")
            pkg_filename = 'unknown'
            pkg_version = 'unknown'
            if 'geneus' in pkg_map:
                pkg_filename = pkg_map['geneus'].filename
                pkg_version  = pkg_map['geneus'].version
            pkg = args[1]               # ARG_PKG
            pkg_dependences = sorted(set(package_depends(pkg) + args[2:]))   # args[1] ARG_PKG
            # write debug information
            f.write(";; THIS FILE IS AUTOMATICALLY GENERATED\n")
            try:
                # https://github.com/jsk-ros-pkg/geneus/commit/152683d63ff23850094b472bff536946e07c76e2 depends on this comment messge
                f.write(";;  FROM %s (%s)\n"%(pkg_map[pkg].filename, pkg_map[pkg].version))
                f.write(";; USING %s %s (%s)\n"%(__file__,pkg_filename,pkg_version))
            except:
                pass
            f.write(";;\n")
            # load all dependences and then load target package
            for p in pkg_dependences:
                f.write("(ros::load-ros-package \"%s\")\n"%p)
            f.write("(ros::load-ros-package \"%s\")\n"%pkg)
            f.close()
            retcode = 0
        else:
            search_path = genmsg.command_line.includepath_to_dict(options.includepath)
            filename = args[1]
            if filename.endswith('.msg'):
                retcode = generate_msg(options.package, args[1:], options.outdir, search_path)
            else:
                retcode = generate_srv(options.package, args[1:], options.outdir, search_path)
    except genmsg.InvalidMsgSpec as e:
        print("ERROR: ", e, file=sys.stderr)
        retcode = 1
    except MsgGenerationException as e:
        print("ERROR: ", e, file=sys.stderr)
        retcode = 2
    except Exception as e:
        traceback.print_exc()
        print("ERROR: ",e)
        retcode = 3
    sys.exit(retcode or 0)
