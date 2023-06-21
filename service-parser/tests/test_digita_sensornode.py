# Import KafkaConsumer from Kafka library
from kafka import KafkaConsumer
import os
import msgpack

expected_data = [
    {
        "time": "2022-02-24T16:23:17.468+00:00",
        "f": {"0": {"v": 5.264}, "1": {"v": 12.18}},
    }
]


def test_parsed_data_from_kafka():
    # Define server with port
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    # Define topic name from where the message will recieve
    KAFKA_PARSED_DATA_TOPIC_NAME = "digita.parseddata"

    # Initialize consumer variable and subscribe to parsed data topic
    consumer = KafkaConsumer(
        KAFKA_PARSED_DATA_TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
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
        parsed_msg["device"]["device_id"] == "70B3D57050011422"
    ), "retreived device metadata is correct"
    assert (
        parsed_msg["device"]["parser_module"] == "fvhiot.parsers.sensornode"
    ), "retreived device metadata is correct"
