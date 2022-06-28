# Moving Visual Inspection System
Author: Minh H. Pham

## Abstract 
The Moving Visual Inspection System (MVIS) project is a part of Intelligent Visual Inspection System (IVIS). The aim of the project is to monitor the state of component boxes, to check whether the components are sufficient, and alarm otherwise. The current status of the project is as follows:

* Only detect missing or not. Do not include wrong or reverse component placement
* Include 2 models: UDMP00SD and USWP24SD
* Can run in 2 ways: choose video and run or run camera directly

Notice: the box needs to be put pretty straight (incline angle no greater than 45 degrees) to have accurate predictions.

## Code organization
The key modules of the project is organize as:
* **Controllers**: contain the logics of the program
* **Models**: define data types and interact with data
* **Views**: define the Graphical User Interface (GUI)

![alt text](https://github.com/PHM1605/MVIS/blob/main/images/app.png)
