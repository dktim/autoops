import time

class TASK():
    
    def __init__(self, name, job):
        self.serial = str(time.time()) + name
        self.name = name
        self.job = job
        
        self.status = 0 # -1:exception, 0:stop, 1:running, 2:pause
    
    def get_name(self):
        return self.name
    
    def get_serial(self):
        return self.serial
    
        
    def get_status(self):
        return self.status
    
    def get_job(self):
        return self.job
    
    def get_job_listener(self):
        return self.job_listener