from Models.modelComponent import mRS232

class cRS232():
    def __init__(self):
        self.model = mRS232()

    def send_data(self, data):
        return self.model.send_data(data)
    
    def close_port(self):
        return self.model.close_port()
