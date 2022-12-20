from PIL import ImageGrab
from concurrent.futures import  ThreadPoolExecutor
from pygame import time as ptime
import time
import numpy

def GetImage(filepath,fps,t,threadPool=None):

    threadPool: ThreadPoolExecutor

    totalfps = fps * t
    currenttime = int(1 / fps * 1000)
    def SaveImage(file):
        with ImageGrab.grab() as picture :
            pass
            #f.write(picture)
            #f.flush()

    with open(filepath,'ab') as f:
        if threadPool == None :
            for i in range(totalfps):
                SaveImage(file=f)
                #time.sleep(currenttime)
        else :
            for i in range(totalfps):
                threadPool.submit(SaveImage,f)
                ptime.wait(currenttime)
        f.close()


def Main():
    t = time.time()
    p = ThreadPoolExecutor(10)
    GetImage('hhh.txt',60,3,p)
    t = time.time() - t
    print(t)
    return None

if __name__ == '__main__':
    Main()