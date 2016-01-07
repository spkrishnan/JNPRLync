# JNPRLync
Objective of the project: Provide dynamic Quality of Service for endpoints in a Lync Call


Overview:
Lync calls are encrypted and dynamically chose the communication ports for each call. So, it is challenging to identify Lync calls on the Network Devices in the path and provide appropriate Quality of Service. 

The Microsoft Lync Software Defined Network (SDN) API provides an interface for network management systems to access Lync network diagnostic data for monitoring Lync network traffic and optimizing the Lync quality of service experiences.

The MS Lync SDN manager can be setup to send call details and call performance details for every Lync call to a listener.

We use these messages to identify the Lync endpoints and communcation ports and dynamically apply Quality of service for those endpoints on Juniper swithces. 

In this project we will use the Netconf support on Juniper switches to provision QoS for the endpoints. 


Step1:
Setup MSLync SDN API environment

Step2:
Run "python eventFlask.py"
This script will start the web service on 8080 that listens for the messages from the SDN Manager and queues the events for processing

Step3:
Run "python eqMonitor.py"
This script checks the event queue every 30 seconds looking for event messages. If there are any messages in the queue, it pulls the messages from the queue and calls the "lCentralMain" function that process these messages
The "lCentralMain" function takes the events and locates the switches on which these endpoints are located and queues events to be configured on the switches

Step4:
Run "python cqMonitor.py"
This script checks the config queue every 60 seconds looking for new configuration events. If there are any messages in the config queue, it pulls the messages and push the appropriate configuration to the switches.





