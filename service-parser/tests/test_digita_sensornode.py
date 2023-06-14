# Import KafkaConsumer from Kafka library
from kafka import KafkaConsumer
import msgpack

expected_data = [
    {
        "time": "2022-02-24T16:23:17.468+00:00",
        "f": {"0": {"v": 5.264}, "1": {"v": 12.18}},
    }
]

expected_device = {
    "url": "http://devreg:8000/api/v1/devices/70B3D57050011422/",
    "device_id": "70B3D57050011422",
    "type": "http://devreg:8000/api/v1/device-types/1/",
    "name": "Digital Matter SensorNode 70B3D57050011422",
    "pseudonym": "",
    "description": "",
    "created_at": "2023-06-08T12:18:28.816461+03:00",
    "modified_at": "2023-06-08T12:18:28.816469+03:00",
    "equipment_condition": "AC",
    "last_active_at": None,
    "current_location": None,
    "sensor_config": None,
    "unit_of_measurement": "",
    "measurement_resolution": None,
    "quality_indicator": "RE",
    "owner": "http://devreg:8000/api/v1/users/1/",
    "parser_module": "fvhiot.parsers.sensornode",
    "maintenance_log_set": [],
    "installation_image_set": [],
}


def test_parsed_data_from_kafka():
    # Define server with port
    BOOTSTRAP_SERVERS = ["kafka:9092"]

    # Define topic name from where the message will recieve
    KAFKA_PARSED_DATA_TOPIC_NAME = "digita.parseddata"

    # Initialize consumer variable and subscribe to parsed data topic
    consumer = KafkaConsumer(
        KAFKA_PARSED_DATA_TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: msgpack.unpackb(m),
    )

    # Read and print message from consumer
    for msg in consumer:
        parsed_msg = msg.value
        break

    consumer.close()

    #  verify parsed data

    assert parsed_msg["data"] == expected_data, "parsed data is correct"
    assert (
        parsed_msg["device"] == expected_device
    ), "retreived device metadata is correct"
