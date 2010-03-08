Formal Status Report
--------------------

| *Project:* Activity Monitor
| *Name:* Jason Poon
| *Student ID:* 21736053
| *Technical Supervisor:* Prof. S. Gopalakrishnan

.. raw:: pdf

    SetPageCounter 0 lowerroman

MEMORANDUM
----------

| To: Ms. J. Pavelich
| From: Jason Poon
| Date: |date|
| Re: EECE 496 - Project Status

----

**Introduction**

Under the guidance of Professor Gopalakrishnan, I have been developing a system capable of monitoring various activities via several sensor nodes attached to the body.
The goal of the system will be the ability to monitor an individual's activities and motions.
With such a system, it can be used to detect harming motions such as falls where the system can notify the authorities (e.g. caregiver) where they can immediately respond to the situation.

The overall project progress is outlined below in three sections: work completed, work in progress, and work remaining.

**Work Completed**

* Order/Receive Necessary Hardware Components
    Hardware components required for this project include: wireless nodes, accelerometer sensors, and a USB debugger or flasher circuit.

    Prof. Gopalakrishnan ordered several Firefly nodes, Firefly sensor boards (3-axis accelerometer, temperature sensor, light sensor, and microphone), and a USB debugger [#]_.
    While waiting for the parts to arrive, Prof. Gopalakrishnan was able to lend me a micaZ mote and USB flasher.
    The Firefly components took longer than expected to arrive which pushed the schedule back approximately two weeks.

* Real-Time Operating System (RTOS)
    Following an initial investigation of which RTOS to use, I was left with two serious contenders: Nano-RK [#]_ and LiteOS [#]_. 
    In the end, Nano-RK was chosen over LiteOS.

    The LiteOS installation process was considerably buggy and development on LiteOS was unfortunately heavily geared towards Windows.
    Nano-RK, on the otherhand, is very well documented.
    Although Nano-RK does not have a forum or mailing list to post questions, the project owners were very helpful.
    For instance, Anthony Rowe, one of the primary contributors to the Nano-RK project, quickly responded and helped in solving a flashing issue I was experiencing with the Firefly nodes.
    He also provided me with write access to the Wiki and the SVN repository where I have since committed several patches to the Nano-RK project.

* Development Environment Setup
    No major difficulties arose while setting up my development environment.
    The combination of developing on a Linux machine and the quick-start guide from Nano-RK [#]_ made the process very straight forward.

    For source control, all files related to this project are hosted at GitHub and can be found at http://github.com/jpoon/eece496.

**Work in Progress**

* Mote Communication
    Nano-RK implements a multitude of networking protocols including: RT-Link, WiDom, and b-mac. 
    After some research, RT-Link seemed most suitable for the activity monitor due to its ability to provide bounded end-to-end delay across multiple hops and collision-free operation.
    RT-Link also has greater battery performance in comparison to WiDom and b-mac.

    After fixing several build issues with the Nano-RK RT-Link example program, I have managed to get several Firefly nodes to communicate with each other.
    However, it will require considerably more time to fully understand the protocol and optimize it for use with the activity monitor. 

* Accelerometer Drivers
    In order to obtain information from the sensor boards (e.g. accelerometers) attached to the Firefly node, software drivers will need to be built.
    I have developed basic drivers to read information from the sensor boards but am currently facing an issue where I am unsure of the meaning behind the values returned from the sensor boards.
    One would assume that if the node was stationary, the (x,y,z) values for the accelerometer would be (0,0,0); however, the accelerometer returns seemingly random values of (133, 82, 200).
    
    This problem can be solved via a reference document for the Firefly sensor boards or hopefully through individuals who have previously worked with the sensor boards (e.g. the Nano-RK contributors). 

**Work Remaining**

* Base Logic
    Once the sensor board drivers and the node communication software has been completed, I will then be able to proceed with implementing the base logic.
    The base logic will process the information obtained from the various sensors and notify the user interface (UI) of the changes in a person's motion.
    The main difficulty I foresee with this stage of development is the profiling of users; different users will have different thresholds for the various activities.
    The activity monitor system should be intelligent enough to work on all individuals.

* User Interface (UI)
    The UI will be the last major component of the activity monitor.
    Not much thought has been put invested in designing the user interface.
    The complexity of the UI will depend on the time available once the rest of the software components have been completed.
    The goal is to implement a graphical interface that abstracts the inner-workings of the program.
    However, if time is a factor, the UI could be as simple as prompting the user via minicom (serial communication).

**Conclusion**

Through this project, I have made my first contribution to a public project (Nano-RK).
It is my hope that the development of the remainder of the project will continue to be a great learning experience.

Although I am roughly two weeks behind schedule, since receiving the hardware components, I have made significant head-way in developing the system and am confident in the punctual completion of the activity monitor system.

|
|

*Jason Poon*

.. [#] http://www.ece.cmu.edu/firefly
.. [#] http://www.nanork.org
.. [#] http://www.liteos.net
.. [#] http://www.nano-rk.org/wiki/linux-install
.. |date| date:: %B %d, %Y

