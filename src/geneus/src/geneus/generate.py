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

## ROS message source code generation for EusLisp(roseus)
##
## Converts ROS .msg and .srv files in a package into EUsLisp source code

import sys
import os
import traceback
import re

from genmsg import SrvSpec, MsgSpec, MsgContext
from genmsg.msg_loader import load_srv_from_file, load_msg_by_type
import genmsg.gentools

try:
    from cStringIO import StringIO #Python 2.x
except ImportError:
    from io import StringIO #Python 3.x

############################################################
# Built in types
############################################################

def is_integer(t):
    return t in ['byte', 'char', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64'] #t char/byte  deprecated alias for uint8/int8, see http://wiki.ros.org/msg#Fields

def is_signed_int(t):
    return t in ['byte', 'int8', 'int16', 'int32', 'int64']

def is_unsigned_int(t):
    return t in ['char', 'uint8', 'uint16', 'uint32', 'uint64']

def is_bool(t):
    return t == 'bool'

def is_string(t):
    return t == 'string'

def is_float(t):
    return t in ['float16', 'float32', 'float64']

def is_time(t):
    return t in ['time', 'duration']

def field_type(f):
    if f.is_builtin:
        elt_type = lisp_type(f.base_type, f.is_array)
    else:
        elt_type = msg_type(f)
    return elt_type

def parse_msg_type(f):
    "returns (package, msg_or_srv)"
    if f.base_type == 'Header':
        return ('std_msgs', 'Header')
    else:
        return f.base_type.split('/')

def msg_type(f):
    "returns roseus namespace package::msg_or_srv"
    (pkg, msg) = parse_msg_type(f)
    return '%s::%s'%(pkg, msg)

def lisp_type(t, array):
    if t == 'uint8' and array:
        return 'char'
    if is_integer(t):
        return 'integer'
    elif is_bool(t):
        return 'object'
    elif is_float(t):
        return 'float'
    elif is_time(t):
        return 'ros::time'
    elif is_string(t):
        return 'string'
    else:
        raise ValueError('%s is not a recognized primitive type'%t)

def field_initform(f):
    var = "__%s"%f.name
    if f.is_builtin and not f.is_array:
        if is_integer(f.base_type):
            return '(round %s)'%var
        elif is_float(f.base_type):
            return '(float %s)'%var
        elif is_string(f.base_type):
            return '(string %s)'%var
    return var

def field_initvalue(f):
    initvalue = lisp_initvalue(f.base_type)
    elt_type = lisp_type(f.base_type, f.is_array)
    if not is_time(f.base_type):
        elt_type = ':'+elt_type
    if f.is_array:
        len = f.array_len or 0
        if f.is_builtin and not is_string(f.base_type) and not is_bool(f.base_type) and not is_time(f.base_type):
            return '(make-array %s :initial-element %s :element-type %s)'%(len, initvalue, elt_type)
        else:
            return '(let (r) (dotimes (i %s) (push %s r)) r)'%(len, initvalue)
    else:
        return initvalue

def lisp_initvalue(t):
    if is_integer(t):
        return '0'
    elif is_bool(t):
        return 'nil'
    elif is_float(t):
        return '0.0'
    elif is_time(t):
        return '(instance ros::time :init)'
    elif is_string(t):
        return '\"\"'
    else:
        raise ValueError('%s is not a recognized primitive type'%t)

def lisp_initform(t):
    if is_integer(t):
        return 'round'
    elif is_bool(t):
        return 'nil'
    elif is_float(t):
        return 'float'
    elif is_time(t):
        return 'ros::time'
    elif is_string(t):
        return 'string'
    else:
        raise ValueError('%s is not a recognized primitive type'%t)

NUM_BYTES = {'byte': 1, 'int8': 1, 'int16': 2, 'int32': 4, 'int64': 8,
             'char': 1, 'uint8': 1, 'uint16': 2, 'uint32': 4, 'uint64': 8}
             
             

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

def write_begin(s, spec, is_service=False):
    "Writes the beginning of the file: a comment saying it's auto-generated and the in-package form"

    s.write(';; Auto-generated. Do not edit!\n\n', newline=False)
    suffix = 'srv' if is_service else 'msg'
    if is_service:
        spec.actual_name=spec.short_name
    s.write('(when (boundp \'%s::%s)'%(spec.package, spec.actual_name))
    s.write('  (if (not (find-package "%s"))'%(spec.package.upper()))
    s.write('    (make-package "%s"))'%(spec.package.upper()))
    s.write('  (shadow \'%s (find-package "%s")))'%(spec.actual_name, spec.package.upper()))
    s.write('(unless (find-package "%s::%s")'%(spec.package.upper(), spec.actual_name.upper()))
    s.write('  (make-package "%s::%s"))'%(spec.package.upper(), spec.actual_name.upper()))
    if is_service:
        s.write('(unless (find-package "%s::%sREQUEST")'%(spec.package.upper(), spec.actual_name.upper()))
        s.write('  (make-package "%s::%sREQUEST"))'%(spec.package.upper(), spec.actual_name.upper()))
        s.write('(unless (find-package "%s::%sRESPONSE")'%(spec.package.upper(), spec.actual_name.upper()))
        s.write('  (make-package "%s::%sRESPONSE"))'%(spec.package.upper(), spec.actual_name.upper()))
    s.write('')
    s.write('(in-package "ROS")')
    s.newline()

def write_include(s, spec, is_srv=False):
    if not is_srv:
        s.write(';;//! \\htmlinclude %s.msg.html'%spec.actual_name, newline=False) # t2
    for msg_type in sorted(set([parse_msg_type(field)[0] for field in spec.parsed_fields() if not field.is_builtin and parse_msg_type(field)[0] != spec.package])):
        s.write('(if (not (find-package "%s"))'%msg_type.upper())
        s.write('  (ros::roseus-add-msgs "%s"))'%msg_type)
    s.newline()
    s.newline()

def write_slot_definition(s, field):
    "Write the definition of a slot corresponding to a single message field"
    s.write('_%s '%field.name, indent=False, newline=False)


def write_slot_argument(s, field):
    "Write the key arguments of a slot corresponding to a single message field"
    var = field.name
    if field.is_builtin:
        s.write('((:%s __%s) %s)'%(var, var, field_initvalue(field)))
    else:
        if field.is_array:
            len = field.array_len or 0
            s.write('((:%s __%s) (let (r) (dotimes (i %s) (push (instance %s :init) r)) r))'%(var, var, len, field_type(field))) ## FIX??? need to use len = f.array_len or 0
        else:
            s.write('((:%s __%s) (instance %s :init))'%(var, var, field_type(field)))

def write_slot_initialize(s, field):
    "Write the initialization of a slot corresponding to a single message field"
    s.write('(setq _%s %s)'%(field.name, field_initform(field)))

def write_defclass(s, spec):
    "Writes the defclass that defines the message type"
    s.write('(defclass %s::%s'%(spec.package, spec.actual_name))
    with Indent(s):
        s.write(':super ros::object')
        s.write(':slots (')
        with Indent(s, inc=1, indent_first=False):
            for field in spec.parsed_fields():
                write_slot_definition(s, field)
        s.write('))', indent=False)
    s.newline()

def write_defmethod(s, spec):
    s.write('(defmethod %s::%s'%(spec.package, spec.actual_name))
    with Indent(s):
        s.write('(:init')
        with Indent(s, inc=1):
            s.write('(&key')
            with Indent(s, inc=1):
                for field in spec.parsed_fields():
                    write_slot_argument(s, field)
                s.write(')')
            s.write('(send-super :init)')
            for field in spec.parsed_fields():
                write_slot_initialize(s, field)
            s.write('self)')


def write_accessors(s, spec):
    with Indent(s):
        for field in spec.parsed_fields():
            s.write('(:%s'%field.name)
            var = '_%s'%field.name
            with Indent(s, inc=1):
                if field.is_builtin:
                    s.write('(&optional _%s)'%var)
                    s.write('(if _%s (setq %s _%s)) %s)'%(var,var,var,var))
                else:
                    s.write('(&rest _%s)'%var)
                    s.write('(if (keywordp (car _%s))'%var)
                    s.write('    (send* %s _%s)'%(var,var))
                    with Indent(s, inc=2):
                        s.write('(progn')
                        s.write('  (if _%s (setq %s (car _%s)))'%(var,var,var))
                        s.write('  %s)))'%var)

def write_serialize_length(s, v, is_array=False):
    if is_array:
        s.write('(write-long (length %s) s)'%(v))
    else:
        s.write('(write-long (length %s) s) (princ %s s)'%(v,v))


def write_serialize_bits(s, v, num_bytes): 
    if num_bytes == 1:
        s.write('(write-byte %s s)'%v)
    elif num_bytes == 2:
        s.write('(write-word %s s)'%v)
    elif num_bytes == 4:
        s.write('(write-long %s s)'%v)
    else:
        s.write('\n', indent=False)
        s.write('#+(or :alpha :irix6 :x86_64)', indent=False, newline=False)
        s.write('(progn (sys::poke %s (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))'%v)
        s.write('\n', indent=False)
        s.write('#-(or :alpha :irix6 :x86_64)', indent=False)
        s.write('(cond ((and (class %s) (= (length (%s . bv)) 2)) ;; bignum'%(v,v))
        s.write('       (write-long (ash (elt (%s . bv) 0) 0) s)'%v)
        s.write('       (write-long (ash (elt (%s . bv) 1) -1) s))'%v)
        s.write('      ((and (class %s) (= (length (%s . bv)) 1)) ;; big1'%(v,v))
        s.write('       (write-long (elt (%s . bv) 0) s)'%v)
        s.write('       (write-long (if (>= %s 0) 0 #xffffffff) s))'%v)
        s.write('      (t                                         ;; integer')
        s.write('       (write-long %s s)(write-long (if (>= %s 0) 0 #xffffffff) s)))'%(v,v))


def write_serialize_bits_signed(s, v, num_bytes):
    write_serialize_bits(s, v, num_bytes)

def write_serialize_builtin(s, f, v):
    if f.base_type == 'string':
        write_serialize_length(s, v)
    elif f.base_type == 'float32':
        s.write('(sys::poke %s (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)'%v)
    elif f.base_type == 'float64':
        s.write('(sys::poke %s (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)'%v)
    elif f.base_type == 'bool':
        s.write('(if %s (write-byte -1 s) (write-byte 0 s))'%v)
    elif f.base_type in ['byte', 'char']:
        s.write('(write-byte %s s)'%v)
    elif f.base_type in ['duration', 'time']:
        s.write('(write-long (send %s :sec) s) (write-long (send %s :nsec) s)'%(v,v))
    elif is_signed_int(f.base_type):
        write_serialize_bits_signed(s, v, NUM_BYTES[f.base_type])
    elif is_unsigned_int(f.base_type):
        write_serialize_bits(s, v, NUM_BYTES[f.base_type])
    else:
        raise ValueError('Unknown type: %s', f.base_type)

def write_serialize_field(s, f):
    s.write(';; %s _%s'%(f.type, f.name))
    slot = '_%s'%f.name
    var = slot
    if f.is_array and f.base_type == 'uint8':
        if not f.array_len:
            s.write('(write-long (length %s) s)'%slot)
        s.write('(princ %s s)'%slot)
    elif f.is_array and is_string(f.base_type):
        s.write('(write-long (length %s) s)'%slot)
        s.write('(dolist (elem %s)'%slot)
        var = 'elem'
    elif f.is_array:
        if not f.array_len:
            write_serialize_length(s, slot, True)
        if f.is_builtin and f.array_len:
            s.write('(dotimes (i %s)'%f.array_len)
        elif f.is_builtin and not f.array_len:
            s.write('(dotimes (i (length %s))'%var)
        else:
            s.write('(dolist (elem %s)'%slot)
        slot = 'elem'
        var = '(elt %s i)'%var
        s.block_next_indent()
        s.write('')

    if f.is_array and f.base_type == 'uint8':
        pass
    elif f.is_builtin:
        with Indent(s):
            write_serialize_builtin(s, f, var)
    else:
        with Indent(s):
            s.write('(send %s :serialize s)'%slot)

    if f.is_array and f.base_type != 'uint8':
        s.write('  )')
 
def write_serialize(s, spec):
    """
    Write the serialize method
    """
    with Indent(s):
        s.write('(:serialize')
        with Indent(s,inc=1):
            s.write('(&optional strm)')
            s.write('(let ((s (if strm strm')
            s.write('           (make-string-output-stream (send self :serialization-length)))))')
            with Indent(s):
                for f in spec.parsed_fields():
                    write_serialize_field(s, f)
                s.write(';;')
                s.write('(if (null strm) (get-output-stream-string s))))')

def write_deserialize_length(s, f, v, is_array=False):
    if is_array:
        s.write('(let (n)') ## TODO should not be here
        with Indent(s):
            s.write('(setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)')
            s.write('(setq %s (let (r) (dotimes (i n) (push (instance %s :init) r)) r))'%(v,field_type(f)))
    else:
        set = 'setf' if v[0] == '(' else 'setq'
        s.write('(let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (%s %s (subseq buf ptr- (+ ptr- n))) (incf ptr- n))'%(set, v))

def write_deserialize_bits(s, v, num_bytes):
    if num_bytes == 1:
        type = ':char'
    elif num_bytes == 2:
        type = ':short'
    elif num_bytes == 4:
        type = ':integer'
    elif num_bytes == 8:
        type = ':long'
        s.write('')
        return write_deserialize_bits_signed(s,v,num_bytes)
    else:
        raise ValueError('Unknown size: %s', num_bytes)

    set = 'setf' if v[0] == '(' else 'setq'
    s.write('(%s %s (sys::peek buf ptr- %s)) (incf ptr- %s)'%(set,v,type,num_bytes))

def write_deserialize_bits_signed(s, v, num_bytes):
    if num_bytes in [1,2,4]:
        write_deserialize_bits(s, v, num_bytes)
    else:
        s.write('\n', indent=False)
        s.write('#+(or :alpha :irix6 :x86_64)', indent=False)
        s.write(' (setf %s (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))\n'%v)
        s.write('#-(or :alpha :irix6 :x86_64)', indent=False)
        s.write(' (setf %s (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))'%v)
        s.write('             (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))')
        s.write('         (cond ((= b1 -1) b0)')
        s.write('                ((and (= b1  0)')
        s.write('                      (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))')
        s.write('                 b0)')
        s.write('               ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))')
        s.write('               (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))')

def write_deserialize_builtin(s, f, v):
    set = 'setf' if v[0] == '(' else 'setq'
    if f.base_type == 'string':
        write_deserialize_length(s,f,v)
    elif f.base_type == 'float32':
        s.write('(%s %s (sys::peek buf ptr- :float)) (incf ptr- 4)'%(set, v))
    elif f.base_type == 'float64':
        s.write('(%s %s (sys::peek buf ptr- :double)) (incf ptr- 8)'%(set, v))
    elif f.base_type == 'bool':
        s.write('(%s %s (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)'%(set, v))
    elif f.base_type in ['duration', 'time']:
        s.write('(send %s :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send %s :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)'%(v,v))
    elif is_signed_int(f.base_type):
        write_deserialize_bits_signed(s, v, NUM_BYTES[f.base_type])
        if NUM_BYTES[f.base_type] == 1: # if signed byte, we have to convert to -128-127
            s.write('(if (> %s 127) (%s %s (- %s 256)))'%(v,set,v,v))
    elif is_unsigned_int(f.base_type):
        write_deserialize_bits(s, v, NUM_BYTES[f.base_type])
    else:
        raise ValueError('%s unknown'%f.base_type)

def write_deserialize_field(s, f, pkg):
    var = '_%s'%f.name
    s.write(';; %s %s'%(f.type, var))
    if f.is_array:
        if f.is_builtin:
            if f.base_type == 'uint8':
                if f.array_len:
                    s.write('(setq %s (make-array %d :element-type :char))'%(var,f.array_len))
                    s.write('(replace %s buf :start2 ptr-) (incf ptr- %d)'%(var,f.array_len))
                else:
                    s.write('(let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)')
                    s.write('  (setq %s (make-array n :element-type :char))'%var)
                    s.write('  (replace %s buf :start2 ptr-) (incf ptr- n))'%(var))
            elif f.array_len:
                s.write('(dotimes (i (length %s))'%var)
                var = '(elt %s i)'%var
            else:
                if is_float(f.base_type) or is_integer(f.base_type) or is_string(f.base_type) or is_bool(f.base_type):
                    s.write('(let (n)')
                    with Indent(s):
                        s.write('(setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)')
                        if is_string(f.base_type) or is_bool(f.base_type):
                            s.write('(setq %s (make-list n))'%var)
                        else:
                            s.write('(setq %s (instantiate %s-vector n))'%(var, lisp_type(f.base_type, f.is_array)))
                        s.write('(dotimes (i n)')
                        var = '(elt %s i)'%var
                else:
                    write_deserialize_length(s, f, var, True)
                    var = 'elem-'
                    with Indent(s):
                        s.write('(dolist (%s _%s)'%(var, f.name))
        else: # array but not builtin
            if f.array_len:
                s.write('(dotimes (i %s)'%f.array_len)
                var = '(elt _%s i)'%f.name
            else:
                write_deserialize_length(s, f, var, True)
                var = 'elem-'
                with Indent(s):
                    s.write('(dolist (%s _%s)'%(var, f.name))
    if f.is_array and f.base_type == 'uint8':
        pass
    elif f.is_builtin:
        with Indent(s):
            write_deserialize_builtin(s, f, var)
    else:
        with Indent(s):
            s.write('(send %s :deserialize buf ptr-) (incf ptr- (send %s :serialization-length))'%(var, var))

    if f.is_array and not f.base_type == 'uint8':
        with Indent(s):
            if f.array_len:
                s.write(')')
            else:
                s.write('))')


def write_deserialize(s, spec):
    """
    Write the deserialize method
    """
    with Indent(s):
        s.write('(:deserialize')
        with Indent(s,inc=1):
            s.write('(buf &optional (ptr- 0))')
            for f in spec.parsed_fields():
                write_deserialize_field(s, f, spec.package)
            s.write(';;')
            s.write('self)')
        s.write(')')
        s.newline()

def write_md5sum(s, msg_context, spec, parent=None):
    md5sum = genmsg.compute_md5(msg_context, parent or spec)
    s.write('(setf (get %s::%s :md5sum-) "%s")'%(spec.package, spec.actual_name, md5sum))

def write_ros_datatype(s, spec):
    s.write('(setf (get %s::%s :datatype-) "%s/%s")'%(spec.package, spec.actual_name, spec.package, spec.actual_name))

def write_message_definition(s, msg_context, spec):
    s.write('(setf (get %s::%s :definition-)'%(spec.package, spec.actual_name))
    with Indent(s,6):
        s.write('"')
        definition = genmsg.compute_full_text(msg_context, spec)
        lines = definition.split('\n')
        for line in lines:
            l = line.replace('\\', '\\\\')
            l = l.replace('"', '\\"')
            s.write('%s\n'%l, indent=False, newline=False)
    s.write('")', newline=False)
    s.write('\n\n')

def write_service_definition(s, msg_context, spec, parent):
    s.write('(setf (get %s::%s :definition-)'%(parent.package, parent.actual_name))
    with Indent(s,6):
        s.write('"')
        for spec_service in [spec.request, spec.response]:
            definition = genmsg.compute_full_text(msg_context, spec_service)
            lines = definition.split('\n')
            for line in lines[:-1]:
                l = line.replace('\\', '\\\\')
                l = l.replace('"', '\\"')
                s.write('%s\n'%l, indent=False, newline=False)
            if spec_service == spec.request:
                s.write('---\n', indent=False, newline=False)
    s.write('")', newline=False)

def write_builtin_length(s, f, var='msg'):
    if f.base_type in ['int8', 'uint8']:
        s.write('1')
    elif f.base_type in ['int16', 'uint16']:
        s.write('2')
    elif f.base_type in ['int32', 'uint32', 'float32']:
        s.write('4')
    elif f.base_type in ['int64', 'uint64', 'float64', 'duration', 'time']:
        s.write('8')
    elif f.base_type == 'string':
        s.write('4 (length _%s)'%f.name)
    elif f.base_type in ['bool', 'byte', 'char']:
        s.write('1')
    else:
        raise ValueError('Unknown: %s', f.base_type)

def write_serialization_length(s, spec):
    with Indent(s):
        s.write('(:serialization-length')
        with Indent(s, inc=1):
            s.write('()')
            s.write('(+')
            with Indent(s, 1):
                if not spec.parsed_fields():
                    s.write('0')
                for field in spec.parsed_fields():
                    s.write(';; %s _%s'%(field.type, field.name))
                    if field.is_array:
                        if field.is_builtin and not is_string(field.base_type):
                            s.write('(* ')
                        else:
                            s.write('(apply #\'+ ')
                        s.block_next_indent()

                        if field.is_builtin:
                            if not field.array_len:
                                if is_string(field.base_type):
                                    s.write('(mapcar #\'(lambda (x) (+ 4 (length x))) _%s)) 4'%(field.name))
                                else:
                                    write_builtin_length(s, field)
                                    s.write('(length _%s)) 4'%field.name, newline=False)
                            else:
                                write_builtin_length(s, field)
                                s.write('%s)'%field.array_len, newline=False)
                        else:
                            if field.array_len:
                                s.write('(send-all _%s :serialization-length))'%field.name)
                            else:
                                s.write('(send-all _%s :serialization-length)) 4'%field.name)
                    else:
                        if field.is_builtin:
                            write_builtin_length(s, field)
                        else:
                            s.write('(send _%s :serialization-length)'%field.name)

                s.write('))')


def write_provide(s, msg_context, spec):
    md5sum = genmsg.compute_md5(msg_context, spec)
    s.write('(provide :%s/%s "%s")'%(spec.package, spec.actual_name,md5sum))
    s.write('\n')

def write_constants(s, spec):
    if spec.constants:
        for c in spec.constants:
            s.write('(intern "*%s*" (find-package "%s::%s"))'%(c.name.upper(), spec.package.upper(), spec.actual_name.upper()))
            s.write('(shadow \'*%s* (find-package "%s::%s"))'%(c.name.upper(), spec.package.upper(), spec.actual_name.upper()))
            if c.type == 'string':
                s.write('(defconstant %s::%s::*%s* "%s")'%(spec.package, spec.actual_name, c.name.upper(), c.val.replace('"', '\\"')))
            elif c.type == 'bool':
                s.write('(defconstant %s::%s::*%s* %s)'%(spec.package, spec.actual_name, c.name.upper(), "t" if c.val == "True" else "nil"))
            else:
                s.write('(defconstant %s::%s::*%s* %s)'%(spec.package, spec.actual_name, c.name.upper(), c.val))

def write_srv_component(s, spec, context, parent):
    spec.component_type='service'
    write_constants(s, spec)
    write_defclass(s, spec)
    write_defmethod(s, spec)
    write_accessors(s, spec)
    write_serialization_length(s, spec)
    write_serialize(s, spec)
    write_deserialize(s, spec)

def write_service_specific_methods(s, context, spec):
    ### this should be move to previsou definition section ???
    s.write('(defclass %s::%s'%(spec.package, spec.actual_name))
    with Indent(s):
        s.write(':super ros::object')
        s.write(':slots ())')
    s.newline()
    write_md5sum(s, context, spec, parent=spec)
    write_ros_datatype(s, spec)
    s.write('(setf (get %s::%s :request) %s::%s)'%(spec.package, spec.actual_name, spec.request.package, spec.request.actual_name))
    s.write('(setf (get %s::%s :response) %s::%s)'%(spec.package, spec.actual_name, spec.response.package, spec.response.actual_name))
    s.newline()
    s.write('(defmethod %s::%s'%(spec.request.package, spec.request.actual_name))
    s.write('  (:response () (instance %s::%s :init)))'%(spec.response.package, spec.response.actual_name))
    s.newline()
    for spec_service in [spec.request, spec.response]:
        write_md5sum(s, context, spec_service, parent=spec)
        write_ros_datatype(s, spec_service)
        write_service_definition(s, context, spec, spec_service)
        s.newline()
    s.write('\n')
    write_provide(s, context, spec)
    s.write('\n', newline=False)

def generate_msg(pkg, files, out_dir, search_path):
    """
    Generate euslisp code for all messages in a package
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
    Generate euslisp code for all services in a package
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

def generate_msg_from_spec(msg_context, spec, search_path, output_dir, package):
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
    # 1. Write the .l file
    ########################################
    
    io = StringIO()
    s =  IndentedWriter(io)
    write_begin(s, spec)
    write_include(s, spec)
    write_constants(s, spec)
    write_defclass(s, spec)
    write_defmethod(s, spec)
    write_accessors(s, spec)
    write_serialization_length(s, spec)
    write_serialize(s, spec)
    write_deserialize(s, spec)
    write_md5sum(s, msg_context, spec)
    write_ros_datatype(s, spec)
    write_message_definition(s, msg_context, spec)
    write_provide(s, msg_context, spec)
    
    if (not os.path.exists(output_dir)):
        # if we're being run concurrently, the above test can report false but os.makedirs can still fail if
        # another copy just created the directory
        try:
            os.makedirs(output_dir)
        except OSError as e:
            pass

    with open('%s/%s.l'%(output_dir, spec.short_name), 'w') as f:
        f.write(io.getvalue() + "\n")
    io.close()


# t0 most of this could probably be refactored into being shared with messages
def generate_srv_from_spec(msg_context, spec, search_path, output_dir, package, path):
    "Generate code from .srv file"
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    ext = '.srv'
    srvs = [f[:-len(ext)] for f in os.listdir(os.path.dirname(path)) if f.endswith(ext)]
    for s in srvs:
        load_srv_from_file(msg_context, path, '%s/%s'%(package, s))

    ########################################
    # 1. Write the .l file
    ########################################

    io = StringIO()
    s = IndentedWriter(io)
    write_begin(s, spec, True)
    write_include(s, spec.request, is_srv=True)
    write_include(s, spec.response, is_srv=True)
    spec.request.actual_name='%sRequest'%spec.short_name
    spec.response.actual_name='%sResponse'%spec.short_name
    write_srv_component(s, spec.request, msg_context, spec)
    write_srv_component(s, spec.response, msg_context, spec)
    write_service_specific_methods(s, msg_context, spec)

    with open('%s/%s.l'%(output_dir, spec.short_name), 'w') as f:
        f.write(io.getvalue())
    io.close()


