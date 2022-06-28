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

Scripts are all saved in the main modules, with descriptions below:
* **controllerMain**: contain the main logics of the program
* **viewMain**: define the structure of the GUI
* **modelMain.py**: load the pretrained Torch model saved in Data folder (**best.pt**) to detect the bounding box; define the camera; define the CNN to classify (four) cells in a detected bounding box
* **modelPath.py**: define the location of the files in the program
* **modelRS232.py**: define RS232 port model to open, send data and close port. The port number is defined in file **Data/config.txt**
* **modelStatus.py**: define dictionary to convert four-digit box status (e.g. 0001) to meaningful sentences, to be display on screen; define a box of statistics to calculate the stats box on the lower right corner, with pass rate, fail rate, yield rate and the most 3 common types of error

## Running program
The GUI of the program is shown as below:
![alt text](https://github.com/PHM1605/MVIS/blob/main/images/app.png)

To open existing video from local computer:
* Step 1: Open the **File** menu (top left corner)
* Step 2: Press **Open**. Choose a video from the local computer. For instance, choose **Data/270522_UDMP00SD.avi**
* Step 3: Press the **Play** button (right panel). Video is running and results are viewable on the screen
