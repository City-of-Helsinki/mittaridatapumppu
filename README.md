# mittaridatapumppu
Realtime data processing and management

![plot](architecture.png)

# Introduction

This repository holds the code for data pipeline as shown in diagram above.
* [service-endpoint](service-endpoint/README.md): a fastapi app that receives sensor data in POST requests and produces them to kafka
* [service-parser](service-parser/README.md): python based microservice that consumer streaming data and converts them from raw format to something else as defined in corresponding parser modules obtained from device metadata
* [service-deviceregistry](service-deviceregistry/README.md): django app for storing device metadata into postgres db

# Build and Test

Go To [test set up](tests/README.md)
