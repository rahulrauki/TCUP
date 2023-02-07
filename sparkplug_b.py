#/********************************************************************************
# * Copyright (c) 2014, 2018 Cirrus Link Solutions and others
# *
# * This program and the accompanying materials are made available under the
# * terms of the Eclipse Public License 2.0 which is available at
# * http://www.eclipse.org/legal/epl-2.0.
# *
# * SPDX-License-Identifier: EPL-2.0
# *
# * Contributors:
# *   Cirrus Link Solutions - initial implementation
# ********************************************************************************/
import sparkplug_b_pb2
import time
from sparkplug_b_pb2 import Payload

seqNum = 0
bdSeq = 0

class DataSetDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14

class MetricDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14
    UUID = 15
    DataSet = 16
    Bytes = 17
    File = 18
    Template = 19

python_datatype_mapping = {
    0 : "NoneType",
    1 : "int",
    2 : "int",
    3 : "int",
    4 : "int",
    5 : "int",
    6 : "int",
    7 : "int",
    8 : "int",
    9 : "float",
    10 : "float",
    11 : "bool",
    12 : "str",
    13 : "int",
    14 : "str",
    15 : "str",
    16 : "DataSet",
    17 : "bytes",
    18 : "bytes",
    19 : "Template",
}

class ParameterDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14

class ParameterDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14

######################################################################
# Always request this before requesting the Node Birth Payload
######################################################################
def getNodeDeathPayload():
    payload = sparkplug_b_pb2.Payload()
    addMetric(payload, "bdSeq", None, MetricDataType.Int64, getBdSeqNum())
    return payload
######################################################################

######################################################################
# Always request this after requesting the Node Death Payload
######################################################################
def getNodeBirthPayload():
    global seqNum
    seqNum = 0
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(round(time.time() * 1000))
    payload.seq = getSeqNum()
    addMetric(payload, "bdSeq", None, MetricDataType.Int64, --bdSeq)
    return payload
######################################################################

######################################################################
# Get the DBIRTH payload
######################################################################
def getDeviceBirthPayload():
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(round(time.time() * 1000))
    payload.seq = getSeqNum()
    return payload
######################################################################

######################################################################
# Get a DDATA payload
######################################################################
def getDdataPayload():
    return getDeviceBirthPayload()
######################################################################

######################################################################
# Helper method for adding dataset metrics to a payload
######################################################################
def initDatasetMetric(payload, name, alias, columns, types):
    metric = payload.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = int(round(time.time() * 1000))
    metric.datatype = MetricDataType.DataSet

    # Set up the dataset
    metric.dataset_value.num_of_columns = len(types)
    metric.dataset_value.columns.extend(columns)
    metric.dataset_value.types.extend(types)
    return metric.dataset_value
######################################################################

######################################################################
# Helper method for adding dataset metrics to a payload
######################################################################
def initTemplateMetric(payload, name, alias, templateRef):
    metric = payload.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = int(round(time.time() * 1000))
    metric.datatype = MetricDataType.Template

    # Set up the template
    if templateRef is not None:
        metric.template_value.template_ref = templateRef
        metric.template_value.is_definition = False
    else:
        metric.template_value.is_definition = True

    return metric.template_value
######################################################################

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template with a timestamp
######################################################################
#def addMetric(container, name, alias, type, value):
#    metric.timestamp = int(round(time.time() * 1000))
#    return addMetric(container, name, alias, type, value, timestamp)

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template
######################################################################
def addMetric(container, name, alias, type, value, timestamp=int(round(time.time() * 1000))):
    metric = container.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = timestamp

    # print( "Type: " + str(type))

    if type == MetricDataType.Int8:
        metric.datatype = MetricDataType.Int8
        if value < 0:
            value = value + 2**8
        metric.int_value = value
    elif type == MetricDataType.Int16:
        metric.datatype = MetricDataType.Int16
        if value < 0:
            value = value + 2**16
        metric.int_value = value
    elif type == MetricDataType.Int32:
        metric.datatype = MetricDataType.Int32
        if value < 0:
            value = value + 2**32
        metric.int_value = value
    elif type == MetricDataType.Int64:
        metric.datatype = MetricDataType.Int64
        if value < 0:
            value = value + 2**64
        metric.long_value = value
    elif type == MetricDataType.UInt8:
        metric.datatype = MetricDataType.UInt8
        metric.int_value = value
    elif type == MetricDataType.UInt16:
        metric.datatype = MetricDataType.UInt16
        metric.int_value = value
    elif type == MetricDataType.UInt32:
        metric.datatype = MetricDataType.UInt32
        metric.int_value = value
    elif type == MetricDataType.UInt64:
        metric.datatype = MetricDataType.UInt64
        metric.long_value = value
    elif type == MetricDataType.Float:
        metric.datatype = MetricDataType.Float
        metric.float_value = value
    elif type == MetricDataType.Double:
        metric.datatype = MetricDataType.Double
        metric.double_value = value
    elif type == MetricDataType.Boolean:
        metric.datatype = MetricDataType.Boolean
        metric.boolean_value = value
    elif type == MetricDataType.String:
        metric.datatype = MetricDataType.String
        metric.string_value = value
    elif type == MetricDataType.DateTime:
        metric.datatype = MetricDataType.DateTime
        metric.long_value = value
    elif type == MetricDataType.Text:
        metric.datatype = MetricDataType.Text
        metric.string_value = value
    elif type == MetricDataType.UUID:
        metric.datatype = MetricDataType.UUID
        metric.string_value = value
    elif type == MetricDataType.Bytes:
        metric.datatype = MetricDataType.Bytes
        metric.bytes_value = value
    elif type == MetricDataType.File:
        metric.datatype = MetricDataType.File
        metric.bytes_value = value
    elif type == MetricDataType.Template:
        metric.datatype = MetricDataType.Template
        metric.template_value = value
    else:
        print( "Invalid: " + str(type))

    # Return the metric
    return metric
######################################################################

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template
######################################################################
def addHistoricalMetric(container, name, alias, type, value):
    metric = addMetric(container, name, alias, type, value)
    metric.is_historical = True

    # Return the metric
    return metric
######################################################################

######################################################################
# Helper method for adding metrics to a container which can be a
# payload or a template
######################################################################
def addNullMetric(container, name, alias, type):
    metric = container.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = int(round(time.time() * 1000))
    metric.is_null = True

    # print( "Type: " + str(type))

    if type == MetricDataType.Int8:
        metric.datatype = MetricDataType.Int8
    elif type == MetricDataType.Int16:
        metric.datatype = MetricDataType.Int16
    elif type == MetricDataType.Int32:
        metric.datatype = MetricDataType.Int32
    elif type == MetricDataType.Int64:
        metric.datatype = MetricDataType.Int64
    elif type == MetricDataType.UInt8:
        metric.datatype = MetricDataType.UInt8
    elif type == MetricDataType.UInt16:
        metric.datatype = MetricDataType.UInt16
    elif type == MetricDataType.UInt32:
        metric.datatype = MetricDataType.UInt32
    elif type == MetricDataType.UInt64:
        metric.datatype = MetricDataType.UInt64
    elif type == MetricDataType.Float:
        metric.datatype = MetricDataType.Float
    elif type == MetricDataType.Double:
        metric.datatype = MetricDataType.Double
    elif type == MetricDataType.Boolean:
        metric.datatype = MetricDataType.Boolean
    elif type == MetricDataType.String:
        metric.datatype = MetricDataType.String
    elif type == MetricDataType.DateTime:
        metric.datatype = MetricDataType.DateTime
    elif type == MetricDataType.Text:
        metric.datatype = MetricDataType.Text
    elif type == MetricDataType.UUID:
        metric.datatype = MetricDataType.UUID
    elif type == MetricDataType.Bytes:
        metric.datatype = MetricDataType.Bytes
    elif type == MetricDataType.File:
        metric.datatype = MetricDataType.File
    elif type == MetricDataType.Template:
        metric.datatype = MetricDataType.Template
    else:
        print( "Invalid: " + str(type))

    # Return the metric
    return metric
######################################################################

######################################################################
# Helper method for getting the next sequence number
######################################################################
def getSeqNum():
    global seqNum
    retVal = seqNum
    # print("seqNum: " + str(retVal))
    seqNum += 1
    if seqNum == 256:
        seqNum = 0
    return retVal
######################################################################

######################################################################
# Helper method for getting the next birth/death sequence number
######################################################################
def getBdSeqNum():
    global bdSeq
    retVal = bdSeq
    # print("bdSeqNum: " + str(retVal))
    bdSeq += 1
    if bdSeq == 256:
        bdSeq = 0
    return retVal
######################################################################

######################################################################
# Helper method to covert serialized DDATA payload into a dictionary
######################################################################

def ddataToDictionary(s_payload):
    ddata_dict = {
        "timestamp" : 0,
        "metrics" : [],
        "seq" : 0
    }
    deserialized_payload = sparkplug_b_pb2.Payload()
    deserialized_payload.ParseFromString(s_payload)
    # Populate the dictionary
    ddata_dict["timestamp"] = deserialized_payload.timestamp
    ddata_dict["seq"] = deserialized_payload.seq
    for metric in deserialized_payload.metrics:
        metric_format = {
            "name" : "",
            "timestamp" : 0,
            "dataType" : "",
            "value" : ""
        }
        metric_format["name"] = metric.name
        metric_format["timestamp"] = metric.timestamp
        metric_format["dataType"] = python_datatype_mapping[metric.datatype] 
        # deciding the value type
        if MetricDataType.Int8 == metric.datatype:
            metric_format["value"] = metric.int_value
        elif MetricDataType.Float == metric.datatype:
            metric_format["value"] = metric.float_value
        elif MetricDataType.Double == metric.datatype:
            metric_format["value"] = metric.double_value
        elif MetricDataType.String == metric.datatype:
            metric_format["value"] = metric.string_value
        elif MetricDataType.Boolean == metric.datatype:
            if metric.boolean_value is True: metric_format["value"] = True
            else: metric_format["value"] = False
        elif MetricDataType.Int16 == metric.datatype:
            metric_format["value"] = metric.int_value
        elif MetricDataType.Int32 == metric.datatype:
            metric_format["value"] = metric.int_value
        elif MetricDataType.Int64 == metric.datatype:
            metric_format["value"] = metric.long_value
        elif MetricDataType.UInt8 == metric.datatype:
            metric_format["value"] = metric.int_value
        elif MetricDataType.UInt16 == metric.datatype:
            metric_format["value"] = metric.int_value
        elif MetricDataType.UInt32 == metric.datatype:
            metric_format["value"] = metric.int_value
        elif MetricDataType.UInt64 == metric.datatype:
            metric_format["value"] = metric.long_value
        elif MetricDataType.Text == metric.datatype:
            metric_format["value"] = metric.string_value
        elif MetricDataType.DateTime == metric.datatype:
            metric_format["value"] = metric.long_value
        elif MetricDataType.Bytes == metric.datatype:
            metric_format["value"] = metric.bytes_value
        elif MetricDataType.File == metric.datatype:
            metric_format["value"] = metric.bytes_value
        elif MetricDataType.DataSet == metric.datatype:
            metric_format["value"] = metric.dataset_value
        elif MetricDataType.Template == metric.datatype:
            metric_format["value"] = metric.template_value
        elif MetricDataType.UUID == metric.datatype:
            metric_format["value"] = metric.string_value
        else: metric_format["value"] = None

        ddata_dict["metrics"].append(metric_format)
    
    return ddata_dict

    # Thoughts

    # To accomodate the massive messages that is received we have to think of a queueing system that can receive the data and add them to the queue
    # instead of making the publisher to wait for response,
    # Possibly look into async/await functions, or even multithreading, event emitters, or a queueing system

    #Note : 
    # Since we are fixing the type in proto files, make sure to add the reference in a config or a readme file
    
