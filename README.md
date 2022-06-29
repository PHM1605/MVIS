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
* **Data**: store necessary data for the program and the resulting data

Scripts are all saved in the main modules, with descriptions below:
* **controllerMain**: contain the main logics of the program
* **viewMain**: define the structure of the GUI
* **modelMain.py**: load the pretrained Torch model saved in Data folder (**best.pt**) to detect the bounding box; define the camera; define the CNN to classify (four) cells in a detected bounding box
* **modelPath.py**: define the location of the files in the program
* **modelRS232.py**: define RS232 port model to open, send data and close port. The port number is defined in file **Data/config.txt**
* **modelStatus.py**: define dictionary to convert four-digit box status (e.g. 0001) to meaningful sentences, to be display on screen; define a box of statistics to calculate the stats box on the lower right corner.

## Run program
The GUI of the program is shown as below:
![alt text](https://github.com/PHM1605/MVIS/blob/main/images/app.png)

To open existing video from local computer:
* Step 1: Choose the model from the **Model** section (top right)
* Step 2: Open the **File** menu (top left corner)
* Step 3: Press **Open**. Choose a video from the local computer. For instance, choose **Data/270522_UDMP00SD.avi**
* Step 4: Press the **Play** button (right panel). Video is running and results are viewable on the screen. 

To monitor via camera:
* Step 1: Choose the model from the **Model** section (top right)
* Step 2: Press the **Play** button (right panel)

## Program explanation
The algorithm executes in two steps:
* Step 1: Detect the outer bounding box of the component box (blue box in image)
* Step 2: For each bounding box being detected, apply four classifiers corresponding to four items in the box, at four **Cell** locations. Green indicates OK cells, which means there is a correct component in that cell. Red indicates Not OK cell(s), which means the component in that cell is missing. In the image, the power cord is missing, therefore the color of the power cord cell is red.

The instant result is in the **Issue list** section; saved in the **Data/log.txt** file and sent via RS232. It shows the time of the analysis and the status of the box at that time. Summary report is on the **Stats** section (lower right) and saved in the **Data/daily_log.txt**. The following information is in the summary box: pass rate, fail rate, yield rate and the most 3 common types of error.

## Train on a new dataset
### Train model to detect the outer bounding box
* use Yolov5
* copy the **best.pt** Torch model into **Data/**

### Train four CNN models to classify four cells inside each bounding box
* collect video from the production line.
* fix the path inside **models/modelPath** to the path of the video which we have just collected.
* create for folders inside **Data**: **Folder1**, **Folder2**, **Folder3**, **Folder4**. These are to store the cropped images from the cells, at four locations, within the bounding boxes. 
* run the script **crop_images_to_train_dataset.py**. 
* arrange the images in the four folders into **0** and **1** groups (by creating two **0** and **1** folders inside each **Folder#** folder). **0** contains cell with missing component. **1** contains cell with component existing. 
* run the script **train_sub_models.py**. We created four CNN models inside **Data/**: **submodel_1.h5**, **submodel_2.h5**, **submodel_3.h5**, **submodel_4.h5**
* create a folder inside **Data/** with the name of the box model (e.g. **UDMP00SD**). Move the four submodels into that.
