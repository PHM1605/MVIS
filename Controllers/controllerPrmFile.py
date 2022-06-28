from Models.modelPrmFile import mPRMFile
# ---------------------------------------------------
class cPRMFile():
    def __init__(self, _path_prm=''):
        self._path_prm = _path_prm
        self._model = mPRMFile(self._path_prm)

    # ---------------------------------------------------
    def getFileVersion(self):
        return self._model.getFileVersion()

    # ---------------------------------------------------
    # ---------------------------------------------------
    def getDbPhaseInfo(self):
        return self._model.getDbPhaseInfo()

    # ---------------------------------------------------
    def getEquipNum(self):
        return self._model.getEquipNum()

    # ---------------------------------------------------
    def getWCEna(self):
        return self._model.getWCEna()

    # ---------------------------------------------------
    def getWCUSBPort(self):
        return self._model.getWCUSBPort()
    # ---------------------------------------------------
    def getWCExposure(self):
        return self._model.getWCExposure()

    # ---------------------------------------------------
    def getWCResolution(self):
        return self._model.getWCResolution()

    # ---------------------------------------------------
    def getWCBrightness(self):
        return self._model.getWCBrightness()

    # ---------------------------------------------------
    def getWCContrast(self):
        return self._model.getWCContrast()

    # ---------------------------------------------------
    def getWCHue(self):
        return self._model.getWCHue()

    # ---------------------------------------------------
    def getWCSaturation(self):
        return self._model.getWCSaturation()

    # ---------------------------------------------------
    def getWCSharpness(self):
        return self._model.getWCSharpness()

    # ---------------------------------------------------
    def getWCGamma(self):
        return self._model.getWCGamma()

    # ---------------------------------------------------
    def getWCWhiteBalance(self):
        return self._model.getWCWhiteBalance()

    # ---------------------------------------------------
    def getWCGain(self):
        return self._model.getWCGain()

    # ---------------------------------------------------
    def getWCRotation(self):
        return self._model.getWCRotation()

    # ---------------------------------------------------
    def getRsEna(self):
        return self._model.getRsEna()

    def getTCPEna(self):
        return self._model.getTCPEna()

    # ---------------------------------------------------

    def getRoi(self):
        return self._model.getRoi()
    def getCnf(self):
        return self._model.getCnf()
    def getDistance(self):
        return self._model.getDistance()
    # ---------------------------------------------------
   

    def getCropEna(self):
        return self._model.getEnaCrop()

        # ---------------------------------------------------
    def getCropErea(self):
        return self._model.getCropArea()

