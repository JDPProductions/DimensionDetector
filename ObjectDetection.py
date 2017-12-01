import PIL
from PIL import Image
import os
import shutil

def main():
    #userImg = Image.open("./user_image/userimage_full.png")
    #pass user image to yolo for detection
    #save yolo output for measurement and display


    #manual grab from samples
    shutil.copy("./demo_samples/userimage_detection.png", "./object_detection/userimage_detection.png")
    shutil.copy("./demo_samples/userimage_detection.txt", "./object_detection/userimage_detection.txt")

    detectionImg = Image.open("./object_detection/userimage_detection.png")

    width = int(detectionImg.size[0])
    height = int(detectionImg.size[1])

    canvasDimsHeight = 500
    canvasDimsWidth = int((500 / height) * width)
    canvasImg = detectionImg.resize((canvasDimsWidth, canvasDimsHeight), Image.ANTIALIAS)
    canvasImg.save("./assets/userimage_detectioncanvas.png")

    buttonDimsHeight = 160
    buttonDimsWidth = 220
    buttonImg = detectionImg.resize((buttonDimsWidth, buttonDimsHeight), Image.ANTIALIAS)
    buttonImg.save("./assets/userimage_detectionbutton.gif")
