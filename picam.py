#! /usr/bin/env python3
from picamera2 import Picamera2
import atexit


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Camera:
    
    def __init__(self):
        self.cam = Picamera2()
        preview_config = self.cam.create_still_configuration(main={"size": (1280, 720)})
        print(preview_config)
        self.cam.configure(preview_config)
        self.cam.start()
    
    def capture_file(self, path):
        self.cam.capture_file(path)


camera = Camera()
camera.capture_file('./media/preview.jpeg')
