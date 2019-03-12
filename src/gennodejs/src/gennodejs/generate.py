#
#    Copyright 2016 Rethink Robotics
#
#    Copyright 2016 Chris Smith
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from __future__ import print_function

import sys
import os
import traceback
import re
from os.path import join as pjoin

#import roslib.msgs
#import roslib.srvs
#import roslib.packages
#import roslib.gentools
from genmsg import SrvSpec, MsgSpec, MsgContext
from genmsg.msg_loader import load_srv_from_file, load_msg_by_type
import genmsg.gentools
from copy import deepcopy

try:
    from cStringIO import StringIO #Python 2.x
except ImportError:
    from io import StringIO #Python 3.x

############################################################
# Built in types
############################################################

def is_fixnum(t):
    return t in ['int8', 'uint8', 'int16', 'uint16']

def is_integer(t):
    return is_fixnum(t) or t in ['byte', 'char', 'int32', 'uint32', 'int64', 'uint64'] #t2 byte, char can be fixnum

def is_signed_int(t):
    return t in ['int8', 'int16', 'int32', 'int64']

def is_unsigned_int(t):
    return t in ['uint8', 'uint16', 'uint32', 'uint64']

def is_bool(t):
    return t == 'bool'

def is_string(t):
    return t == 'string'

def is_float(t):
    return t in ['float32', 'float64']

def is_time(t):
    return t in ['time', 'duration']

def parse_msg_type(f):
    if f.base_type == 'Header':
        return ('std_msgs', 'Header')
    else:
        return f.base_type.split('/')

def get_typed_array(t):
    if t in ['int8', 'byte', 'bool']:
        return 'Int8Array'
    elif t in ['uint8', 'char']:
        return 'UInt8Array'
    elif t == 'uint16':
        return 'UInt16Array'
    elif t == 'int16':
        return 'Int16Array'
    elif t == 'uint32':
        return 'UInt32Array'
    elif t == 'int32':
        return 'Int32Array'
    elif t == 'float32':
        return 'Float32Array'
    elif t == 'float64':
        return 'Float64Array'
    # else
    return None


def has_typed_array(t):
    return is_fixnum(t) or is_float(t) or t in ['byte', 'char', 'bool', 'uint8', 'uint16','int8', 'int16', 'uint32', 'int32']

def get_type_size(t):
    """Returns the size in bytes of a builtin type if available. Else None"""
    if t in ['int8', 'uint8', 'byte', 'bool', 'char']:
        return 1
    elif t in ['int16', 'uint16']:
        return 2
    elif t in ['int32', 'uint32', 'float32']:
        return 4
    elif t in ['int64', 'uint64', 'float64', 'time', 'duration']:
        return 8
    return None

def get_default_value(field, current_message_package):
    """Return the default value for a message data field"""
    if field.is_array:
        if not field.array_len:
            return '[]'
        else:
            field_copy = deepcopy(field)
            field_copy.is_array = False;
            field_default = get_default_value(field_copy, current_message_package)
            return 'new Array({}).fill({})'.format(field.array_len, field_default)
    elif field.is_builtin:
        if is_string(field.type):
            return '\'\''
        elif is_time(field.type):
            return '{secs: 0, nsecs: 0}'
        elif is_bool(field.type):
            return 'false'
        elif is_float(field.type):
            return '0.0'
        else:
            return '0';
    # else
    (package, msg_type) = field.base_type.split('/')
    if package == current_message_package:
        return 'new {}()'.format(msg_type)
    else:
        return 'new {}.msg.{}()'.format(package, msg_type)

def is_message_fixed_size(spec, search_path):
    """Check if a particular message specification has a constant size in bytes"""
    parsed_fields = spec.parsed_fields()
    types = [f.base_type for f in parsed_fields]
    variableLengthArrays = [f.is_array and not f.array_len for f in parsed_fields]
    isBuiltin = [f.is_builtin for f in parsed_fields]
    if 'string' in types:
        return False
    elif True in variableLengthArrays:
        return False
    elif False not in isBuiltin:
        return True
    else:
        nonBuiltins = [f for f in parsed_fields if not f.is_builtin]
        # print(nonBuiltins)
        for idx, f in enumerate(nonBuiltins):
            field_msg_context = MsgContext.create_default()
            field_spec = genmsg.msg_loader.load_msg_by_type(field_msg_context, f.base_type, search_path)
            if not is_message_fixed_size(field_spec, search_path):
                return False
        return True

def get_message_fixed_size(spec, search_path):
    """
    Return the size of a message.
    If the message does not have a fixed size, returns None
    """
    if not is_message_fixed_size(spec, search_path):
        return None
    # else
    length = 0
    for f in spec.parsed_fields():
        if f.is_builtin:
            type_size = get_type_size(f.base_type)
            if type_size is None:
                raise Exception('Field {} has a non-constant size'.format(f.base_type))
            if not f.is_array:
                length += type_size
            elif not f.array_len:
                raise Exception('Array field {} has a variable length'.format(f.base_type))
            else:
                length += (f.array_len * type_size)
        else:
            field_msg_context = MsgContext.create_default()
            field_spec = genmsg.msg_loader.load_msg_by_type(field_msg_context, f.base_type, search_path)
            field_size = get_message_fixed_size(field_spec, search_path)
            if field_size is None:
                raise Exception('Field {} has a non-constant size'.format(f.base_type))
            length += field_size
    return length

############################################################
# Indented writer
############################################################

class IndentedWriter():

    def __init__(self, s):
        self.str = s
        self.indentation = 0
        self.block_indent = False

    def write(self, s, indent=True, newline=True):
        if not indent:
            newline = False
        if self.block_indent:
            self.block_indent = False
        else:
            if newline:
                self.str.write('\n')
            if indent:
                for i in range(self.indentation):
                    self.str.write(' ')
        self.str.write(s)

    def newline(self):
        self.str.write('\n')

    def inc_indent(self, inc=2):
        self.indentation += inc

    def dec_indent(self, dec=2):
        self.indentation -= dec

    def reset_indent(self):
        self.indentation = 0

    def block_next_indent(self):
        self.block_indent = True

class Indent():

    def __init__(self, w, inc=2, indent_first=True):
        self.writer = w
        self.inc = inc
        self.indent_first = indent_first

    def __enter__(self):
        self.writer.inc_indent(self.inc)
        if not self.indent_first:
            self.writer.block_next_indent()

    def __exit__(self, type, val, traceback):
        self.writer.dec_indent(self.inc)

def find_path_from_cmake_path(path):
    cmake_path = os.environ['CMAKE_PREFIX_PATH']
    paths = cmake_path.split(':')
    for search_path in paths:
        test_path = pjoin(search_path, path)
        if os.path.exists(test_path):
            return test_path
    return None

def find_path_for_package(package):
    return find_path_from_cmake_path(pjoin('share/gennodejs/ros', package))

def find_requires(spec):
    found_packages = []
    local_deps = []
    for field in spec.parsed_fields():
        if not field.is_builtin:
            (field_type_package, msg_type) = field.base_type.split('/')
            if field_type_package in found_packages:
                continue
            # else
            if field_type_package == spec.package:
                if msg_type not in local_deps:
                    local_deps.append(msg_type)
            else:
                found_packages.append(field_type_package)

    return found_packages, local_deps

def write_begin(s, spec, is_service=False):
    "Writes the beginning of the file: a comment saying it's auto-generated and the in-package form"

    s.write('// Auto-generated. Do not edit!\n\n', newline=False)
    suffix = 'srv' if is_service else 'msg'
    s.write('// (in-package %s.%s)\n\n'%(spec.package, suffix), newline=False)

def write_requires(s, spec, previous_packages=None, prev_deps=None, isSrv=False):
    "Writes out the require fields"
    if previous_packages is None:
        s.write('"use strict";')
        s.newline()
        s.write('const _serializer = _ros_msg_utils.Serialize;')
        s.write('const _arraySerializer = _serializer.Array;');
        s.write('const _deserializer = _ros_msg_utils.Deserialize;')
        s.write('const _arrayDeserializer = _deserializer.Array;');
        s.write('const _finder = _ros_msg_utils.Find;')
        s.write('const _getByteLength = _ros_msg_utils.getByteLength;');
        previous_packages = {}
    if prev_deps is None:
        prev_deps = []
    # find other message packages and other messages in this packages
    # that this message depends on
    found_packages, local_deps = find_requires(spec)
    # filter out previously found local deps
    local_deps = [dep for dep in local_deps if dep not in prev_deps]

    # require mesages from this package
    # messages from this package need to be requried separately
    # so that we don't create a circular requires dependency
    for dep in local_deps:
        if isSrv:
            s.write('let {} = require(\'../msg/{}.js\');'.format(dep, dep))
        else:
            s.write('let {} = require(\'./{}.js\');'.format(dep, dep))

    # filter out previously found packages
    found_packages = {package for package in found_packages if package not in previous_packages}
    for package in found_packages:
        # TODO: finder is only relevant to node - we should support an option to
        #   create a flat message package directory. The downside is that it requires
        #   copying files between workspaces.
        s.write('let {0} = _finder(\'{0}\');'.format(package))
    s.newline()
    s.write('//-----------------------------------------------------------')
    s.newline()
    return found_packages, local_deps

def write_msg_constructor_field(s, spec, field):
    s.write('if (initObj.hasOwnProperty(\'{}\')) {{'.format(field.name))
    with Indent(s):
        s.write('this.{} = initObj.{}'.format(field.name, field.name))
    s.write('}')
    s.write('else {')
    with Indent(s):
        s.write('this.{} = {};'.format(field.name, get_default_value(field, spec.package)))
    s.write('}')

def write_class(s, spec):
    s.write('class {} {{'.format(spec.actual_name))
    with Indent(s):
        # TODO: add optional object argument
        s.write('constructor(initObj={}) {')
        with Indent(s):
            s.write('if (initObj === null) {')
            with Indent(s):
                s.write('// initObj === null is a special case for deserialization where we don\'t initialize fields')
                for field in spec.parsed_fields():
                    s.write('this.{} = null;'.format(field.name))
            s.write('}')
            s.write('else {')
            with Indent(s):
                for field in spec.parsed_fields():
                    write_msg_constructor_field(s, spec, field)
            s.write('}')
        s.write('}')
    s.newline()

def get_message_path_from_field(field, pkg):
    (field_pkg, msg_type) = field.base_type.split('/')
    if field_pkg == pkg:
        return msg_type
    # else
    return '{}.msg.{}'.format(field_pkg, msg_type)

def write_resolve(s, spec):
    with Indent(s):
        s.write('static Resolve(msg) {')
        with Indent(s):
            s.write('// deep-construct a valid message object instance of whatever was passed in');
            s.write('if (typeof msg !== \'object\' || msg === null) {')
            with Indent(s):
                s.write('msg = {};')
            s.write('}')
            s.write('const resolved = new {}(null);'.format(spec.short_name))
            for field in spec.parsed_fields():
                if not field.is_builtin:
                    s.write('if (msg.{} !== undefined) {{'.format(field.name))
                    with Indent(s):
                        if field.is_array:
                            if field.array_len is None:
                                s.write('resolved.{} = new Array(msg.{}.length);'.format(field.name, field.name))
                                s.write('for (let i = 0; i < resolved.{}.length; ++i) {{'.format(field.name))
                                with Indent(s):
                                    s.write('resolved.{}[i] = {}.Resolve(msg.{}[i]);'.format(field.name, get_message_path_from_field(field, spec.package), field.name))
                                s.write('}')
                            else:
                                s.write('resolved.{} = new Array({})'.format(field.name, field.array_len))
                                s.write('for (let i = 0; i < resolved.{}.length; ++i) {{'.format(field.name))
                                with Indent(s):
                                    s.write('if (msg.{}.length > i) {{'.format(field.name))
                                    with Indent(s):
                                        s.write('resolved.{}[i] = {}.Resolve(msg.{}[i]);'.format(field.name, get_message_path_from_field(field, spec.package), field.name))
                                    s.write('}')
                                    s.write('else {')
                                    with Indent(s):
                                        s.write('resolved.{}[i] = new {}();'.format(field.name, get_message_path_from_field(field, spec.package)))
                                    s.write('}')
                                s.write('}')
                        else:
                            s.write('resolved.{} = {}.Resolve(msg.{})'.format(field.name, get_message_path_from_field(field, spec.package), field.name))
                    s.write('}')
                    s.write('else {')
                    with Indent(s):
                        s.write('resolved.{} = {}'.format(field.name, get_default_value(field, spec.package)))
                    s.write('}')
                else:
                    s.write('if (msg.{} !== undefined) {{'.format(field.name))
                    with Indent(s):
                        s.write('resolved.{} = msg.{};'.format(field.name, field.name))
                    s.write('}')
                    s.write('else {')
                    with Indent(s):
                        s.write('resolved.{} = {}'.format(field.name, get_default_value(field, spec.package)))
                    s.write('}')
                s.newline()
            s.write('return resolved;')
            s.write('}')

def write_end(s, spec):
    s.write('};')
    s.newline();
    write_constants(s, spec)
    s.write('module.exports = {};'.format(spec.actual_name))

def write_serialize_base(s, rest):
    s.write('bufferOffset = {};'.format(rest))

def write_serialize_length(s, name):
    #t2
    s.write('// Serialize the length for message field [{}]'.format(name))
    write_serialize_base(s, '_serializer.uint32(obj.{}.length, buffer, bufferOffset)'.format(name))

def write_serialize_length_check(s, field):
    s.write('// Check that the constant length array field [{}] has the right length'.format(field.name))
    s.write('if (obj.{}.length !== {}) {{'.format(field.name, field.array_len))
    with Indent(s):
        s.write('throw new Error(\'Unable to serialize array field {} - length must be {}\')'.format(field.name, field.array_len))
    s.write('}')

# adds function to serialize builtin types (string, uint8, ...)
def write_serialize_builtin(s, f):
    if (f.is_array):
        write_serialize_base(s, '_arraySerializer.{}(obj.{}, buffer, bufferOffset, {})'.format(f.base_type, f.name, 'null' if f.array_len is None else f.array_len))
    else:
        write_serialize_base(s, '_serializer.{}(obj.{}, buffer, bufferOffset)'.format(f.base_type, f.name))

# adds function to serlialize complex type (geometry_msgs/Pose)
def write_serialize_complex(s, f, thisPackage):
    (package, msg_type) = f.base_type.split('/')
    samePackage =  package == thisPackage
    if (f.is_array):
        if f.array_len is None:
            write_serialize_length(s, f.name)
        s.write('obj.{}.forEach((val) => {{'.format(f.name))
        with Indent(s):
            if samePackage:
                write_serialize_base(s, '{}.serialize(val, buffer, bufferOffset)'.format(msg_type))
            else:
                write_serialize_base(s, '{}.msg.{}.serialize(val, buffer, bufferOffset)'.format(package, msg_type))
        s.write('});')
    else:
        if samePackage:
            write_serialize_base(s, '{}.serialize(obj.{}, buffer, bufferOffset)'.format(msg_type, f.name))
        else:
            write_serialize_base(s, '{}.msg.{}.serialize(obj.{}, buffer, bufferOffset)'.format(package, msg_type, f.name))

# writes serialization for a single field in the message
def write_serialize_field(s, f, package):
    if f.is_array:
        if f.array_len is not None:
            write_serialize_length_check(s, f)

    s.write('// Serialize message field [{}]'.format(f.name))
    if f.is_builtin:
        write_serialize_builtin(s, f)
    else:
        write_serialize_complex(s, f, package)

def write_serialize(s, spec):
    """
    Write the serialize method
    """
    with Indent(s):
        s.write('static serialize(obj, buffer, bufferOffset) {')
        with Indent(s):
            s.write('// Serializes a message object of type {}'.format(spec.short_name))
            for f in spec.parsed_fields():
                write_serialize_field(s, f, spec.package)
            s.write('return bufferOffset;')
        s.write('}')
        s.newline()

# t2 can get rid of is_array
def write_deserialize_length(s, name):
    s.write('// Deserialize array length for message field [{}]'.format(name))
    s.write('len = _deserializer.uint32(buffer, bufferOffset);')

def write_deserialize_complex(s, f, thisPackage):
    (package, msg_type) = f.base_type.split('/')
    samePackage = package == thisPackage
    if f.is_array:
        if f.array_len is None:
            write_deserialize_length(s, f.name)
        else:
            s.write('len = {};'.format(f.array_len))

        s.write('data.{} = new Array(len);'.format(f.name))
        s.write('for (let i = 0; i < len; ++i) {')
        with Indent(s):
            if samePackage:
                s.write('data.{}[i] = {}.deserialize(buffer, bufferOffset)'.format(f.name, msg_type));
            else:
                s.write('data.{}[i] = {}.msg.{}.deserialize(buffer, bufferOffset)'.format(f.name, package, msg_type));
        s.write('}')
    else:
        if samePackage:
            s.write('data.{} = {}.deserialize(buffer, bufferOffset);'.format(f.name, msg_type))
        else:
            s.write('data.{} = {}.msg.{}.deserialize(buffer, bufferOffset);'.format(f.name, package, msg_type))

def write_deserialize_builtin(s, f):
    if f.is_array:
        s.write('data.{} = _arrayDeserializer.{}(buffer, bufferOffset, {})'.format(f.name, f.base_type, 'null' if f.array_len is None else f.array_len));
    else:
        s.write('data.{} = _deserializer.{}(buffer, bufferOffset);'.format(f.name, f.base_type))


def write_deserialize_field(s, f, package):
    s.write('// Deserialize message field [{}]'.format(f.name))
    if f.is_builtin:
        write_deserialize_builtin(s, f)
    else:
        write_deserialize_complex(s, f, package)


def write_deserialize(s, spec):
    """
    Write the deserialize method
    """
    with Indent(s):
        s.write('static deserialize(buffer, bufferOffset=[0]) {')
        with Indent(s):
            s.write('//deserializes a message object of type {}'.format(spec.short_name))
            s.write('let len;')
            s.write('let data = new {}(null);'.format(spec.short_name))
            for f in spec.parsed_fields():
                write_deserialize_field(s, f, spec.package)

            s.write('return data;')
        s.write('}')
        s.newline()

def write_get_message_size(s, spec, search_path):
    """
    Write a static method to determine the buffer size of a complete message
    """

    with Indent(s):
        s.write('static getMessageSize(object) {')
        msg_size = get_message_fixed_size(spec, search_path)
        if msg_size is not None:
            with Indent(s):
                s.write('return {};'.format(msg_size))
        else:
            def get_dynamic_field_length_line(field, query):
                if field.is_builtin:
                    if not is_string(field.base_type):
                        raise Exception('Unexpected field {} with type {} has unknown length'.format(field.name, field.base_type))
                    # it's a string array!
                    return 'length += 4 + {}.length;'.format(query)
                # else
                (package, msg_type) = field.base_type.split('/')
                samePackage = spec.package == package
                if samePackage:
                    return 'length += {}.getMessageSize({});'.format(msg_type, query)
                else:
                    return 'length += {}.msg.{}.getMessageSize({});'.format(package, msg_type, query)

            with Indent(s):
                s.write('let length = 0;')
                # certain fields will always have the same size
                # calculate that here instead of dynamically every time
                len_constant_length_fields = 0;
                for f in spec.parsed_fields():
                    field_size = None
                    if f.is_builtin:
                        field_size = get_type_size(f.base_type)
                    else:
                        field_msg_context = MsgContext.create_default()
                        field_spec = genmsg.msg_loader.load_msg_by_type(field_msg_context, f.base_type, search_path)
                        field_size = get_message_fixed_size(field_spec, search_path)

                    if f.is_array:
                        if f.array_len and field_size is not None:
                            len_constant_length_fields += (field_size * f.array_len)
                            continue
                        elif not f.array_len:
                            len_constant_length_fields += 4

                        if field_size == 1:
                            s.write('length += object.{}.length;'.format(f.name))
                        elif field_size is not None:
                            s.write('length += {} * object.{}.length;'.format(field_size, f.name))
                        else:
                            if f.is_builtin:
                                if not is_string(f.base_type):
                                    raise Exception('Unexpected field {} with type {} has unknown length'.format(f.name, f.base_type))
                                # it's a string array!
                                line_to_write = 'length += 4 + val.length;'
                            else:
                                (package, msg_type) = f.base_type.split('/')
                                samePackage = spec.package == package
                                if samePackage:
                                    line_to_write = 'length += {}.getMessageSize(val);'.format(msg_type,)
                                else:
                                    line_to_write = 'length += {}.msg.{}.getMessageSize(val);'.format(package, msg_type)
                            s.write('object.{}.forEach((val) => {{'.format(f.name))
                            with Indent(s):
                                s.write(line_to_write)
                            s.write('});')
                    elif field_size is not None:
                        len_constant_length_fields += field_size
                    else:
                        # field size is dynamic!
                        if f.is_builtin:
                            if not is_string(f.base_type):
                                raise Exception('Unexpected field {} with type {} has unknown length'.format(f.name, f.base_type))
                            # it's a string array!
                            len_constant_length_fields += 4
                            line_to_write = 'length += object.{}.length;'.format(f.name)
                        else:
                            (package, msg_type) = f.base_type.split('/')
                            samePackage = spec.package == package
                            if samePackage:
                                line_to_write = 'length += {}.getMessageSize(object.{});'.format(msg_type, f.name)
                            else:
                                line_to_write = 'length += {}.msg.{}.getMessageSize(object.{});'.format(package, msg_type, f.name)
                        s.write(line_to_write)

                if len_constant_length_fields > 0:
                    s.write('return length + {};'.format(len_constant_length_fields))
                else:
                    s.write('return length;')
        s.write('}')
        s.newline()

def write_package_index(s, package_dir):
    s.write('"use strict";')
    s.newline()
    s.write('module.exports = {')
    msgExists = os.path.exists(pjoin(package_dir, 'msg/_index.js'))
    srvExists = os.path.exists(pjoin(package_dir, 'srv/_index.js'))
    with Indent(s):
        if (msgExists):
            s.write('msg: require(\'./msg/_index.js\'),')
        if (srvExists):
            s.write('srv: require(\'./srv/_index.js\')')
    s.write('};')
    s.newline()

def write_msg_index(s, msgs, pkg, context):
    "Writes an index for the messages"
    s.write('"use strict";')
    s.newline()

    for msg in msgs:
        s.write('let {} = require(\'./{}.js\');'.format(msg, msg))
    s.newline()
    s.write('module.exports = {')
    with Indent(s):
        for msg in msgs:
            s.write('{}: {},'.format(msg, msg))
    s.write('};')
    s.newline()

def write_srv_index(s, srvs, pkg):
    "Writes an index for the messages"
    s.write('"use strict";')
    s.newline()
    for srv in srvs:
        s.write('let {} = require(\'./{}.js\')'.format(srv, srv))
    s.newline()
    s.write('module.exports = {')
    with Indent(s):
        for srv in srvs:
            s.write('{}: {},'.format(srv, srv))
    s.write('};')
    s.newline()

def write_ros_datatype(s, spec):
    with Indent(s):
        s.write('static datatype() {')
        with Indent(s):
            s.write('// Returns string type for a %s object'%spec.component_type)
            s.write('return \'{}\';'.format(spec.full_name))
        s.write('}')
        s.newline()

def write_md5sum(s, msg_context, spec, parent=None):
    md5sum = genmsg.compute_md5(msg_context, parent or spec)
    with Indent(s):
        s.write('static md5sum() {')
        with Indent(s):
            # t2 this should print 'service' instead of 'message' if it's a service request or response
            s.write('//Returns md5sum for a message object')
            s.write('return \'{}\';'.format(md5sum))
        s.write('}')
        s.newline()

def write_message_definition(s, msg_context, spec):
    with Indent(s):
        s.write('static messageDefinition() {')
        with Indent(s):
            s.write('// Returns full string definition for message')
            definition = genmsg.compute_full_text(msg_context, spec)
            lines = definition.split('\n')
            s.write('return `')
            for line in lines:
                s.write('{}'.format(line))
            s.write('`;')
        s.write('}')
        s.newline()

def write_constants(s, spec):
    if spec.constants:
        s.write('// Constants for message')
        s.write('{}.Constants = {{'.format(spec.short_name))
        with Indent(s):
            for c in spec.constants:
                if is_string(c.type):
                    s.write('{}: \'{}\','.format(c.name.upper(), c.val))
                elif is_bool(c.type):
                    s.write('{}: {},'.format(c.name.upper(), 'true' if c.val else 'false'))
                else:
                    s.write('{}: {},'.format(c.name.upper(), c.val))
        s.write('}')
        s.newline()

def write_srv_component(s, spec, context, parent, search_path):
    spec.component_type='service'
    write_class(s, spec)
    write_serialize(s, spec)
    write_deserialize(s, spec)
    write_get_message_size(s, spec, search_path)
    write_ros_datatype(s, spec)
    write_md5sum(s, context, spec)
    write_message_definition(s, context, spec)
    write_resolve(s, spec)
    s.write('};')
    s.newline()
    write_constants(s, spec)

def write_srv_end(s, context, spec):
    s.write('module.exports = {')
    name = spec.short_name
    with Indent(s):
        s.write('Request: {}Request,'.format(name))
        s.write('Response: {}Response,'.format(name))
        md5sum = genmsg.compute_md5(context, spec)
        s.write('md5sum() {{ return \'{}\'; }},'.format(md5sum))
        s.write('datatype() {{ return \'{}\'; }}'.format(spec.full_name))
    s.write('};')
    s.newline()

def generate_msg(pkg, files, out_dir, search_path):
    """
    Generate javascript code for all messages in a package
    """
    msg_context = MsgContext.create_default()
    for f in files:
        f = os.path.abspath(f)
        infile = os.path.basename(f)
        full_type = genmsg.gentools.compute_full_type_name(pkg, infile)
        spec = genmsg.msg_loader.load_msg_from_file(msg_context, f, full_type)
        generate_msg_from_spec(msg_context, spec, search_path, out_dir, pkg)

def generate_srv(pkg, files, out_dir, search_path):
    """
    Generate javascript code for all services in a package
    """
    msg_context = MsgContext.create_default()
    for f in files:
        f = os.path.abspath(f)
        infile = os.path.basename(f)
        full_type = genmsg.gentools.compute_full_type_name(pkg, infile)
        spec = genmsg.msg_loader.load_srv_from_file(msg_context, f, full_type)
        generate_srv_from_spec(msg_context, spec, search_path, out_dir, pkg, f)

def msg_list(pkg, search_path, ext):
    dir_list = search_path[pkg]
    files = []
    for d in dir_list:
        files.extend([f for f in os.listdir(d) if f.endswith(ext)])
    return [f[:-len(ext)] for f in files]

def generate_msg_from_spec(msg_context, spec, search_path, output_dir, package, msgs=None):
    """
    Generate a message

    @param msg_path: The path to the .msg file
    @type msg_path: str
    """
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    spec.actual_name=spec.short_name
    spec.component_type='message'
    msgs = msg_list(package, search_path, '.msg')
    for m in msgs:
        genmsg.load_msg_by_type(msg_context, '%s/%s'%(package, m), search_path)

    ########################################
    # 1. Write the .js file
    ########################################

    io = StringIO()
    s =  IndentedWriter(io)
    write_begin(s, spec)
    write_requires(s, spec)
    write_class(s, spec)
    write_serialize(s, spec)
    write_deserialize(s, spec)
    write_get_message_size(s, spec, search_path)
    write_ros_datatype(s, spec)
    write_md5sum(s, msg_context, spec)
    write_message_definition(s, msg_context, spec)
    write_resolve(s, spec)
    write_end(s, spec)

    if (not os.path.exists(output_dir)):
        # if we're being run concurrently, the above test can report false but os.makedirs can still fail if
        # another copy just created the directory
        try:
            os.makedirs(output_dir)
        except OSError as e:
            pass

    with open('%s/%s.js'%(output_dir, spec.short_name), 'w') as f:
        f.write(io.getvalue() + "\n")
    io.close()

    ########################################
    # 3. Write the msg/_index.js file
    # This is being rewritten once per msg
    # file, which is inefficient
    ########################################
    io = StringIO()
    s = IndentedWriter(io)
    write_msg_index(s, msgs, package, msg_context)
    with open('{}/_index.js'.format(output_dir), 'w') as f:
        f.write(io.getvalue())
    io.close()

    ########################################
    # 3. Write the package _index.js file
    # This is being rewritten once per msg
    # file, which is inefficient
    ########################################
    io = StringIO()
    s = IndentedWriter(io)
    package_dir = os.path.dirname(output_dir)
    write_package_index(s, package_dir)
    with open('{}/_index.js'.format(package_dir), 'w') as f:
        f.write(io.getvalue())
    io.close()

# t0 most of this could probably be refactored into being shared with messages
def generate_srv_from_spec(msg_context, spec, search_path, output_dir, package, path):
    "Generate code from .srv file"
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    ext = '.srv'
    srv_path = os.path.dirname(path)
    srvs = msg_list(package, {package: [srv_path]}, ext)
    for srv in srvs:
        load_srv_from_file(msg_context, '%s/%s%s'%(srv_path, srv, ext), '%s/%s'%(package, srv))

    ########################################
    # 1. Write the .js file
    ########################################

    io = StringIO()
    s = IndentedWriter(io)
    write_begin(s, spec, True)
    found_packages,local_deps = write_requires(s, spec.request, None, None, True)
    write_requires(s, spec.response, found_packages, local_deps, True)
    spec.request.actual_name='%sRequest'%spec.short_name
    spec.response.actual_name='%sResponse'%spec.short_name
    write_srv_component(s, spec.request, msg_context, spec, search_path)
    write_srv_component(s, spec.response, msg_context, spec, search_path)
    write_srv_end(s, msg_context, spec)

    with open('%s/%s.js'%(output_dir, spec.short_name), 'w') as f:
        f.write(io.getvalue())
    io.close()

    ########################################
    # 3. Write the msg/_index.js file
    # This is being rewritten once per msg
    # file, which is inefficient
    ########################################
    io = StringIO()
    s = IndentedWriter(io)
    write_srv_index(s, srvs, package)
    with open('{}/_index.js'.format(output_dir), 'w') as f:
        f.write(io.getvalue())
    io.close()

    ########################################
    # 3. Write the package _index.js file
    # This is being rewritten once per msg
    # file, which is inefficient
    ########################################
    io = StringIO()
    s = IndentedWriter(io)
    package_dir = os.path.dirname(output_dir)
    write_package_index(s, package_dir)
    with open('{}/_index.js'.format(package_dir), 'w') as f:
        f.write(io.getvalue())
    io.close()
