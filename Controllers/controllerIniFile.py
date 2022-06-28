from Models.modelIniFile import mINIFile


class cINIFile():
    def __init__(self, path_ini=''):
        self.path_ini = path_ini
        self.model = mINIFile(self.path_ini)

    def getCameraNum(self):
        return self.model.getCameraNum()

    def getSpecFileName(self):
        return self.model.getSpecFileName()

    def getPrmFileName(self):
        return self.model.getPrmFileName()

    def getOpeMode(self):
        return self.model.getOpeMode()

    def getResultBeep(self):
        return self.model.getResultBeep()

    def getImageSaveType(self):
        return self.model.getImageSaveType()

    def getMaxPhase(self):
        return self.model.getMaxPhase()

    def getMaxGen(self):
        return self.model.getMaxGen()

    def getMaxStep(self):
        return self.model.getMaxStep()

    def getCurrentPhase(self):
        return self.model.getCurrentPhase()

    def getMaxJg(self):
        return self.model.getMaxJg()

    def getOutNameImg(self):
        return self.model.getOutNameImg()
