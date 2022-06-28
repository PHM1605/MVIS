import tkinter as tk
import cv2, os, uuid, hashlib, copy, pytesseract
import numpy as np
from tkinter import filedialog, messagebox
from Views.viewMain import View
from Models.modelComponent import Component, Camera
from Models.modelData import dPRMFile, dINIFile
from Models.modelPath import mGetPath
from Models.modelOCR import mOCR
from Controllers.controllerPrmFile import cPRMFile
from Controllers.controllerIniFile import cINIFile
from Controllers.controllerRS232 import cRS232 
from datetime import datetime
from tensorflow.python.keras.models import load_model
# from sklearn.preprocessing import LabelEncoder

class Controller():
    def __init__(self):
        self.root = tk.Tk()

        _ = self.init_value_ini()
        _ = self.init_value_prm()
        
        self.view = View(self, self.root) # control the appearance of the app
        self.load_model()
        self.camera = Camera(usb_port = 0)
        self.camera.change_default_settings(self.dataPRM.WCExposure,
                                            self.dataPRM.WCResolutionWidth,
                                            self.dataPRM.WCResolutionHigh,
                                            self.dataPRM.WCBrightness,
                                            self.dataPRM.WCContrast,
                                            self.dataPRM.WCHue,
                                            self.dataPRM.WCSaturation,
                                            self.dataPRM.WCSharpness,
                                            self.dataPRM.WCGamma,
                                            self.dataPRM.WCWhiteBalance,
                                            self.dataPRM.WCGain)
            
        self.ctrlRS232 = cRS232()
        self.MAC = None        
        self.ocr = mOCR()
        self.get_barcode_from_scanner()        
        
        # set event when close window
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.title("JBD_AI_CCD")
        self.get_mac_add() # to check license                
        
        self.root.mainloop() # wait for click events
    
    """" convert from '1 0.9 0.1 0.2 0.3' to (x1, y1, w, h), do not use label; dw, dh are the size of the original image """
    def convert_yolofm_to_pixels(self, line, dw, dh):
        label, x_cell, y_cell, w_cell, h_cell = line.split(' ')
        label, x_cell, y_cell, w_cell, h_cell = int(label), float(x_cell), float(y_cell), float(w_cell), float(h_cell)
        w_pixel = int( w_cell * dw )
        h_pixel = int( h_cell * dh )
        x_pixel = int( x_cell * dw - w_pixel / 2 )
        y_pixel = int( y_cell * dh - h_pixel / 2 )
        return (x_pixel, y_pixel, w_pixel, h_pixel)

    """" convert from '1 0.9 0.1 0.2 0.3' to '1' and 'Radiator' (label), do not use (x, y, w, h) """
    def convert_yolofm_to_label(self, line):
        # read the first character of standard_labels.txt
        idx = int( line[0] )
        # read file classes.txt
        with open(mGetPath.classesPath, 'r+') as file:
            lines = file.readlines()
        lines = [ line.replace('\n', '') for line in lines ]
        return idx, lines[idx] 
            
    def get_comps_from_path(self):
        with open(mGetPath.standardLabelsPath, "r+") as label_file:
            lines = label_file.readlines()
        lines = [ line.replace('\n', '') for line in lines ]
        # convert labels to readable format
        ret = []
        for line in lines:
            label, name = self.convert_yolofm_to_label(line)
            x, y, w, h = self.convert_yolofm_to_pixels(line, self.view.curr_img.shape[1],\
                                                       self.view.curr_img.shape[0])
            component = Component( box = [x, y, w, h], label = label, name = name )
            ret.append( component )
        return ret
    
    def load_model(self):
        self.model = load_model(mGetPath.modelPath)
        self.model_conf = 0.8 
    
    def on_menu_open(self):
        path = filedialog.askopenfilename()
        self.img_path = path
        img = None
        if len(path) > 0: # if open file successfully
            img = cv2.imread(path)
        img = cv2.resize(img, (2592, 1944))
        if img is not None:
            self.view.curr_img = img
            self.img_shape = img.shape[:2]
            self.view.update_canvas(img)
            self.image_analyze(0)
             
    # when pressing the CAPTURE button
    def on_btn_capture(self, evt): # evt is the event object
        img = self.camera.take_pic()
        if img is not None:
            img = cv2.resize(img, (2592, 1944))
            self.view.curr_img = img
            self.img_shape = img.shape[:2]
            self.view.update_canvas(img)
            self.image_analyze(0)
    
    # when pressing the ANALYZE button
    def image_analyze(self, evt):        
        # list of components read from standard file
        self.comps = self.get_comps_from_path()
        self.get_barcode_from_image(self.comps[0])
        self.ana_res = True
        pred = self.model( self.create_test_dataset_from_image( resizedSize = 28) )
        pred = pred.numpy()[:,0]
        self.preds = np.array( [ round(pred[i]) for i in range(len(pred)) ] )
        
        # convert range of predictions from [0, 1,....] to [1, 4, 6...]
        # le = LabelEncoder()
        # le.classes_ = np.load(mGetPath.lePath)
        # self.preds = le.inverse_transform(self.preds.astype(int))
        self.preds = self.preds.astype(int) + 1
        
        for pred in self.preds:
            # 'NoRadiator' class or no barcode detected
            if pred == 2 or self.barcode_res == False:
                self.ana_res = False
                break
            
        self.view.update_result( self.ana_res )
        
        if self.ana_res == True and self.MAC is not None:
            data_send = str(self.MAC) + 13 * ' ' + 'FT' + 10 * '+' + chr(13) # chr(13) is '\n'
            self.ctrlRS232.send_data(data_send.encode())
        
        self.res_img = self.view.draw_result() 
        
        ## save image to a folder
        def get_img_name():
            if self.MAC is None:
                img_name = datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg'
            else:
                img_name = self.MAC + '.jpg'
            return img_name
        
        img_name = get_img_name()
        if self.ana_res == True:
            folder_name = os.path.join(mGetPath.saveImagesPath, 'Pass')
        else:
            folder_name = os.path.join(mGetPath.saveImagesPath, 'Fail')           
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)            
        file_path = os.path.join(folder_name, img_name)
        cv2.imwrite(file_path, self.view.curr_img)
        self.MAC = None

    """" read an image, read areas of interest from standard_labels.txt file, """
    """" resize those areas, resize to desized input size to feed into CNN, pack all together """
    def create_test_dataset_from_image(self, resizedSize):            
        xTest = []
        img = copy.deepcopy(self.view.curr_img)
        dw, dh = img.shape[1], img.shape[0]
        with open(mGetPath.standardLabelsPath, 'r+') as file:
            lines = file.readlines()
        lines = [ line.replace('\n', '') for line in lines]
        for line in lines:
            iLabel, label = self.convert_yolofm_to_label(line)
            # only choose the radiator box (label 1 in the standard_labels.txt file)
            if label == 'Radiator':
                x, y, w, h = self.convert_yolofm_to_pixels(line, dw, dh)
                cropImg = img[ y : (y + h), x : (x + w)  ]
                xTest.append( cv2.resize(cropImg, (resizedSize, resizedSize), interpolation = cv2.INTER_AREA) )
        return np.array(xTest)     

    def init_value_prm(self):
        _ret = 0
        self.dataPRM = dPRMFile()
        self.controllerPRM = cPRMFile(mGetPath.prmPath)
        # Basic
        _ret, self.dataPRM.FileVersion = self.controllerPRM.getFileVersion()
        # EquipmentInfo
        _ret, self.dataPRM.EquipNum = self.controllerPRM.getEquipNum()
        # DEBUGInfo
        _ret, self.dataPRM.CurrentPhaseDb = self.controllerPRM.getDbPhaseInfo()
        # Crop
        _ret, self.dataPRM.EnCrop = self.controllerPRM.getCropEna()
        _ret, self.dataPRM.CropArea = self.controllerPRM.getCropErea()
        # RSCOMM
        _ret, self.dataPRM.RSEna = self.controllerPRM.getRsEna()
        # WebCamCtrl
        _ret, self.dataPRM.WCEna = self.controllerPRM.getWCEna()
        if self.dataPRM.WCEna == 1:
            _ret, self.dataPRM.WCExposure = self.controllerPRM.getWCExposure()
            _ret, self.dataPRM.WCUSBPort = self.controllerPRM.getWCUSBPort()
            _ret, self.dataPRM.WCResolutionWidth, self.dataPRM.WCResolutionHigh = \
                self.controllerPRM.getWCResolution()

            _ret, self.dataPRM.WCBrightness = self.controllerPRM.getWCBrightness()
            _ret, self.dataPRM.WCContrast = self.controllerPRM.getWCContrast()
            _ret, self.dataPRM.WCHue = self.controllerPRM.getWCHue()
            _ret, self.dataPRM.WCSaturation = self.controllerPRM.getWCSaturation()
            _ret, self.dataPRM.WCSharpness = self.controllerPRM.getWCSharpness()
            _ret, self.dataPRM.WCGamma = self.controllerPRM.getWCGamma()
            _ret, self.dataPRM.WCGain = self.controllerPRM.getWCGain()
            _ret, self.dataPRM.WCWhiteBalance = self.controllerPRM.getWCWhiteBalance()
            _ret, self.dataPRM.WCRotation = self.controllerPRM.getWCRotation()


            _ret, self.dataPRM.Roi = self.controllerPRM.getRoi()
            _ret, self.dataPRM.Cnf = self.controllerPRM.getCnf()
            _ret, self.dataPRM.Distance = self.controllerPRM.getDistance()

        return _ret
    
    def init_value_ini(self):
        self.dataINI = dINIFile()
        self._INI = cINIFile( mGetPath.iniPath )

        # ------------------------------------------------------
        # WebCamInfo
        _ret, self.dataINI.CameraNum = self._INI.getCameraNum()
        # FileInfo
        _ret, self.dataINI.SpecFileName = self._INI.getSpecFileName()
        _ret, self.dataINI.PrmFileName = self._INI.getPrmFileName()
        # OperationMode
        _ret, self.dataINI.OpeMode = self._INI.getOpeMode()
        _ret, self.dataINI.ResultBeep = self._INI.getResultBeep()
        _ret, self.dataINI.ImageSaveType = self._INI.getImageSaveType()
        _ret, self.dataINI.MaxPhase = self._INI.getMaxPhase()
        _ret, self.dataINI.MaxGen = self._INI.getMaxGen()
        _ret, self.dataINI.MaxStep = self._INI.getMaxStep()
        _ret, self.dataINI.CurrentPhase = self._INI.getCurrentPhase()
        _ret, self.dataINI.MaxJg = self._INI.getMaxJg()
        _ret, self.dataINI.OutNameImg = self._INI.getOutNameImg()

        return _ret
    
    def on_edit_prm_file(self):
        _ret = 0
        _ret, path_prm = mGetPath.get_prm_path(self.dataINI.PrmFileName)
        os.startfile(path_prm)

    def on_edit_ini_file(self):
        _ret = 0
        _ret, _path_ini = mGetPath.iniPath
        os.startfile(_path_ini)
        
    # def restart(self):
    #     rest = sys.executable
    #     os.execl(rest, rest, * sys.argv)
 
    def on_close(self):
        response = messagebox.askyesno('Exit', 'Are you sure you want to exit?')
        if response:
            self.ctrlRS232.close_port()
            self.root.destroy()
            
    """ get MAC address, convert to hex -> true password. Compare with password the user writes into Data/License/license.lic """
    def get_mac_add(self):
        # lấy 8 giá trị của MAC address
        str2hash = hex(uuid.getnode())[2:14]
        str2hash = str2hash.upper()
        true_pw = hashlib.md5(str2hash.encode())
        true_pw = true_pw.hexdigest()
        curr_pw = self.read_license()
        if true_pw != curr_pw:
            self.show_license()
        else:
            pass
    
    def read_license(self):
        with open(mGetPath.licensePath, "r+") as lic_file:
            line = lic_file.readlines()
            line = line[0]
            if line[-1] == '\n':
                line = line.strip()
            lic_file.close()
        return line

    def show_license(self):
        self.view.create_license_window()
         
    # by image
    def get_barcode_from_image(self, component):
        img = copy.deepcopy(self.view.curr_img)
        x, y, w, h = component.box[0], component.box[1], component.box[2], component.box[3]
        cropImg = img[ y - 10 : (y + h + 10), x - 10 : (x + w + 10)  ]
        detectedBarcode = self.ocr.decode(cropImg)
        if len(detectedBarcode) < 10:
            self.view.barcode_text.config(text = 'Barcode not detected')
            self.barcode_res = False
        else:
            self.view.barcode_text.config(text = detectedBarcode)
            self.barcode_res = True
    
    # by scanner
    def get_barcode_from_scanner(self):
        self.root.after(1000, self.get_barcode_from_scanner) # run barcode scan every 1000ms
        barcode = self.view.barcode_entry.get()
        self.view.barcode_entry.delete(0, 'end') # erase the entry box to clear accidental keystroke
        if (len(barcode)) > 10: # if MAC is true
            self.barcode_res = True
            self.MAC = barcode[:12]
            self.on_btn_capture(0)
            self.image_analyze(0)
            self.view.barcode_entry.delete(0, 'end')
        else: 
            self.barcode_res = False