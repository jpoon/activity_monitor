Activity Monitor
================

Introduction
------------
The project entails the development of an activity monitor where sensory data obtained via wireless nodes attached to the body are used to determine an individual’s movement. The following report outlines the behavior of the system.
The objectives for this project are to design and develop a system that is able to monitor a user’s activities based on data retrieved from accelerometers on wireless sensor nodes that are attached to an individual. This involves the development of a software framework on the wireless sensor nodes and a client on the gateway computer to process the data retrieved from the wireless nodes.
An activity monitoring system will provide a mechanism to unobtrusively monitor an individual’s daily activities. Additionally, the system can also be used to track an individual’s exercise routine.
The scope of the project is limited by the FireFly hardware. Being a wireless node, the FireFly sensor node possesses limited memory and processing power.

System Overview
---------------
The activity monitoring system is composed of three subcomponents: the wireless nodes, the server, and the client. Five wireless nodes are used to form the wireless sensor network. Sensory data obtained by the wireless nodes is transmitted via RS-232 to the server which then forwards the data to a client via UDP for processing.

Features
--------
The system currently contains the following features and functionalities:
*	Classification of the User’s Current Motion
* Using the sensor data retrieved from the wireless sensor network, the system is able to classify a user’s motion as either walking, running, sitting, standing, or lying down
* Programmatic Generation of Acceleration Graphs
* Line graphs of the acceleration are programmatically generated for each sensor node. The graphs are of scalable vector graphic (SVG) type but can also be converted to portable network graphic (PNG) type.
* Terminal-Based User Interface
* The user interface prompts provides users with an informative display; the messages displayed on the terminal are also customizable.
* Calibration of Sensor Nodes
* The sensor nodes can be calibrated such that the values read by the accelerometers are converted to a more understandable unit such as acceleration in G’s. Calibration data can be saved to or loaded from a file. 
