# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auto_phat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x61uto_phat.proto\"2\n\x05Motor\x12\r\n\x05motor\x18\x01 \x01(\x05\x12\x0b\n\x03\x64ir\x18\x02 \x01(\x05\x12\r\n\x05speed\x18\x03 \x01(\x05\"(\n\x05Servo\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x12\x0e\n\x06\x64\x65gree\x18\x02 \x01(\x05\"\x19\n\x08Response\x12\r\n\x05\x65rror\x18\x01 \x01(\x08\x32L\n\x07\x43ontrol\x12 \n\tsetMorter\x12\x06.Motor\x1a\t.Response\"\x00\x12\x1f\n\x08setServo\x12\x06.Servo\x1a\t.Response\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auto_phat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_MOTOR']._serialized_start=19
  _globals['_MOTOR']._serialized_end=69
  _globals['_SERVO']._serialized_start=71
  _globals['_SERVO']._serialized_end=111
  _globals['_RESPONSE']._serialized_start=113
  _globals['_RESPONSE']._serialized_end=138
  _globals['_CONTROL']._serialized_start=140
  _globals['_CONTROL']._serialized_end=216
# @@protoc_insertion_point(module_scope)