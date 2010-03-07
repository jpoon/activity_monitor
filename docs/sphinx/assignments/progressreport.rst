Formal Status Report
====================

| Activity Monitor
| Name: Jason Poon
| Student ID: 21736053
| Technical Supervisor: Prof. S. Gopalakrishnan


MEMORANDUM
----------

| To: Ms. J. Pavelich
| From: Jason Poon
| Date: |date|
| Re: EECE 496 - Project Status

----

In complete sentences and coherent paragraphs, create the following sections. Do not rely excessively on point or list form. Double space your work and use a size 12 font. Ensure your status report is no longer than 4 sheets of paper (including the cover page). This means 3 pages of text. If status reports are longer, we will throw out the extra pages -- these will not be graded.

**Introduction**

Under the guidance of Professor S. Gopalakrishnan, I have been developing a system capable of monitoring various activities via several sensor nodes attached to the body.
With the usage of such a system, it is then possible to monitor an individual's activities and, in scenario that the system detects a fall, it can automatically notify the authorities (e.g. caregiver) such that they can immediately respond to the situation.

The overall project progress is outlined below in three sections: work completed, work in progress, and work remaining.

**Work Completed**

* Order/Receive Necessary Hardware Components
    Hardware components requird for this project include: wireless nodes, accelerometer sensors, and a USB debugger or flasher circuit.

    Prof. Gopalakrishnan ordered several Firefly nodes, Firefly sensor boards (3-axis accelerometer, temperature sensor, light sensor, and microphone), and a USB debugger [#]_.
    While waiting for the parts to arrive, Prof. Gopalakrishnan was able to lend me a micaZ mote and USB flasher.
    The Firefly components took longer than expected to arrive which pushed the schedule back approximately two weeks.

* Real-Time Operating System (RTOS)
    Before writing any code, it was first imperative to choose a real-time operating system.
    Following an initial investigation, there were two serious contenders: Nano-RK [#]_ and LiteOS [#]_. 

    In the end, I decided to use Nano-RK as the installation process for LiteOS was considerably buggy.
    Development on LiteOS was unfortunately heavily geared towards Windows (e.g. Java installer).
    Nano-RK, on the otherhand, was well-documented; their 'quick-start' guide was very helpful and I managed to flash the example programs onto the micaZ motes within an hour or so.
    Although Nano-RK does not have a forum or mailing list to post questions, the project contributors were very helpful.
    For instance, Anthony Rowe, one of the primary contributors to the Nano-RK project, was very helpful in solving a flashing issue I was experiencing with the Firefly nodes.
    He also provided me with write access to the Wiki and the SVN repo where I have since committed several patches to the Nano-RK project.

* Development Environment Setup
    No major difficulties arose while setting up my development environment.
    The combination of developing on a Linux machine and the well-documented quick-start guide from Nano-RK [#]_ made the process very straight forward.

    For source control, all files related to this project are hosted at GitHub and can be found at http://github.com/jpoon/eece496.

**Work in Progress**

    * Describe what you are currently doing
    * Explain any difficulties you are currently facing
    * Explain how you are dealing with them

**Work Remaining**

    * Describe what remains to be done
    * Forecast any potential difficulties
    * Explain how you will deal with them

**Conclusion**

Although I am roughly two weeks behind schedule according to my original Gantt chart, I am confident that I will be able to complete this project on time.
Since receiving the hardware components, I have made significant head-way in developing the systm.

    * Evaluate your performance so far
    * Describe whether you are confident or concerned about the project as a whole so far and why
    * Indicate that the project will be completed on time


|
|

*Jason Poon*

.. [#] http://www.ece.cmu.edu/firefly
.. [#] http://www.nanork.org
.. [#] http://www.liteos.net
.. [#] http://www.nano-rk.org/wiki/linux-install
.. |date| date:: %B %d, %Y
