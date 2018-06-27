import os

def free_Mb():
    """ return number of free Mb available """
    s = os.statvfs('/')
    Mb = (s.f_bavail * s.f_frsize) / 1024 / 1024
    return Mb
