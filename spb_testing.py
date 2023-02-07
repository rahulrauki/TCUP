import sparkplug_b as sparkplug
from sparkplug_b_pb2 import *
from sparkplug_b import *

test_payload = getDdataPayload() #creating DDATA payload

# Syntax addMetric(container(payload), name, alias, type, value, timestamp = default)
addMetric(test_payload, "avg_speed", None, MetricDataType.Int8, 80 )
addMetric(test_payload, "distance", None, MetricDataType.Int8, 200 )

print(test_payload)

serialized_payload = test_payload.SerializeToString()

print(serialized_payload)

deserialized_payload = Payload()

deserialized_payload.ParseFromString(serialized_payload)

print(deserialized_payload.metrics[0])
