import sparkplug_b as sparkplug
from sparkplug_b_pb2 import *
from sparkplug_b import *

test_payload = getDdataPayload() #creating DDATA payload

# Syntax addMetric(container(payload), name, alias, type, value, timestamp = default)
addMetric(test_payload, "avg_speed", None, MetricDataType.Int8, 80 )
addMetric(test_payload, "distance", None, MetricDataType.Int8, 200 )
addMetric(test_payload, "checkingIfValid", None, MetricDataType.Boolean, True )
addMetric(test_payload, "brand", None, MetricDataType.String, "Hyundai" )
addMetric(test_payload, "temperature", None, MetricDataType.Float, 37.5 )
# Checking for Arrays (packing and unpacking)
addMetric(test_payload, "Int8", None, MetricDataType.Int8Array, [-23, 123] )
addMetric(test_payload, "Int16", None, MetricDataType.Int16Array, [-30000, 30000] )
addMetric(test_payload, "Int32", None, MetricDataType.Int32Array, [-1, 315338746] )
addMetric(test_payload, "Int64", None, MetricDataType.Int64Array, [-4270929666821191986, -3601064768563266876] )
addMetric(test_payload, "UInt8", None, MetricDataType.UInt8Array, [23, 250] )
addMetric(test_payload, "UInt16", None, MetricDataType.UInt16Array, [30, 52360] )
addMetric(test_payload, "UInt32", None, MetricDataType.UInt32Array, [52, 3293969225] )
addMetric(test_payload, "UInt64", None, MetricDataType.UInt64Array, [52, 16444743074749521625] )
addMetric(test_payload, "Float", None, MetricDataType.FloatArray, [1.23, 89.341] )
addMetric(test_payload, "Double", None, MetricDataType.DoubleArray, [12.354213, 1022.9123213] )
addMetric(test_payload, "Boolean", None, MetricDataType.BooleanArray, [False, False, True, True, False, True, False, False, True, True, False, True] )
addMetric(test_payload, "String", None, MetricDataType.StringArray, ['ABC', 'hello'] )
addMetric(test_payload, "DateTime", None, MetricDataType.DateTimeArray, [1256102875335, 1656107875000] )

print(test_payload)

serialized_payload = test_payload.SerializeToString()

# Directly calling the sparkplug_b_pb2 classes

deserialized_payload = Payload()
deserialized_payload.ParseFromString(serialized_payload)
print(deserialized_payload)

# using the helper method

print(ddataToDictionary(serialized_payload))
