from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import time
import json

host = "a2kb6m6oytlvpe-ats.iot.eu-west-1.amazonaws.com"
port = 8883
rootCAPath = "root-CA.crt"
privateKeyPath = "gateway.private.key"
certificatePath = "gateway.cert.pem"
bridgeId = "0bcf2c83-5578-4f2b-9626-e4dc8663949c"
topic = "B/%s/%s/tc" %(bridgeId, 'self')

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
# myAWSIoTMQTTClient.configureCredentials(rootCAPath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

# Connect to AWS IoT
myAWSIoTMQTTClient.connect()

print(topic)

message = {}
message['message'] = "sdfsdf"
message['sequence'] = 1
messageJson = json.dumps(message)

myAWSIoTMQTTClient.publish(topic, messageJson, 0)

while True:
	time.sleep(1)

myAWSIoTMQTTClient.disconnect()
