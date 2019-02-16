import ctypes
import os
import shutil
import random
import time
import queue

#to auto launch, copy shortcut to startup folder
#C:\Users\Josh\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

'''param_data = open("param_data.txt", "r")
mainFolder = "E:\\Users\\Josh\\Google Drive\\random"

sec = int((param_data.readline().split()[1]))
min = int((param_data.readline().split()[1]))
hour = int((param_data.readline().split()[1]))
blacklistSize = int((param_data.readline().split()[1]))
param_data.close()'''

mainFolder = "E:\\Users\\Josh\\Google Drive\\random"

sec = 0
min = 0
hour = 3
blacklistSize = 20

interval = sec + 60*min + 3600*hour #in seconds
blacklist = queue.Queue(blacklistSize)

#need to write first time write
def save_blacklist(name):
    bFile = open("blacklist.txt", "w")
    list = blacklist.queue
    for i in range(0, blacklist.qsize()):
        bFile.write(list[i] + '\n')
    bFile.close()
    
def load_blacklist():
    bFile = open("blacklist.txt", "r")
    for line in bFile:
        blacklist.put(line.rstrip("\n\r"))

def add_blacklist(name):
    if blacklist.full():
        blacklist.get()
    blacklist.put(name)

def check_blacklist(name):
    testList = blacklist.queue
    #print(testList)
    if name in testList:
        return True
    return False
    
def change_Background(imgCount):

    imageName = os.listdir(mainFolder)[random.randint(0,imgCount)]
    imageRoot, imageExt = os.path.splitext(mainFolder + "\\" + imageName)
    if (imageExt == ".png" or imageExt == ".jpg"):
        if (check_blacklist(imageName) == False):
            print(imageName)
            add_blacklist(imageName)
            save_blacklist(imageName)
            SPI_SETDESKWALLPAPER = 20 
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imageRoot + imageExt, 0)
        else:
            change_Background(imgCount)
            

def get_Image_Count():
    imgCount = 0
    
    for file in os.listdir(mainFolder):
        imgCount += 1
        
    print("Detected " + str(imgCount) + " images.")
    return imgCount

    
    
#########################
starttime=time.time()
totalCount = get_Image_Count()

bCheck = os.path.exists("blacklist.txt")
if bCheck:
    load_blacklist()
else:
    newfile = open("blacklist.txt", "w")
    newfile.close()

while True:
    print(" ")
    print("switching to...")
    change_Background(totalCount)
    time.sleep(interval)



        
