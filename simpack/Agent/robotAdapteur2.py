import math
from Agent.robot import Robot
from Agent.robot2I013 import Robot2IN013

class robotAdapteur2(robot2I013):
    def __init__(Robot:Robot) -> None:
        self.adapte=Robot
    
    
    def get_image(self):
        pass

    def get_images(self):
        pass
    
    
    ###########################################
    def set_motor_dps(self, port, dps):
        pass
    
    def get_motor_position(self):
        pass
    
    def offset_motor_encoder(self, port, offset):
        pass

    def get_distance(self):
        pass
    
    def start_recording(self):
        pass

    def _stop_recording(self):
        pass

    def _start_recording(self):
        pass

    def __getattr__(self,attr):
        pass
    
    ################################################
    def vitesse_to_dps():
        pass