from tkinter import *
from tkinter import filedialog
from shutil import copyfile
import shutil
import PIL
from sys import exit
from PIL import Image
import subprocess
import time
import MeasurementDetection
import ObjectDetection
import os

#
# Function: uploadImageFile()
#    - Copies image in various sizes to root folder,
#       *overwrites existing image files with same names
#       uses images_sized to load algorithms
def uploadImageFile():
    #subprocess.call("explorer C:\\", shell=True)

    #askopenfilename method opens dialog with the computer
    #  and stores selected photo into filename
    root.filename =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("All Files","*.*"),("png Files", "*.png"),("jpeg Files","*.jpg")))
    print (root.filename) #Console Check Test

    rootname = os.path.basename(root.filename)
    name =  rootname.replace('.png','')
    reference = open("./demo_samples/imageToUse.txt", 'w')
    reference.write(name)
    reference.close()

    #open image, resize, and save
    shutil.copy(root.filename,"./user_image/userimage_full.png")
    userImg = Image.open("./user_image/userimage_full.png")

    width = int(userImg.size[0])
    height = int(userImg.size[1])

    canvasDimsHeight = 500
    canvasDimsWidth = int((500 / height) * width)
    canvasImg = userImg.resize((canvasDimsWidth, canvasDimsHeight), Image.ANTIALIAS)
    canvasImg.save("./assets/userimage_originalcanvas.png")

    buttonDimsHeight = 160
    buttonDimsWidth = 220
    buttonImg = userImg.resize((buttonDimsWidth, buttonDimsHeight), Image.ANTIALIAS)
    buttonImg.save("./assets/userimage_originalbutton.gif")

    #Create the buttons with the appropriate images contained on button interface
    createImgButtons()

def changeImage1():
    canvas.delete("all")
    newImage1 = PhotoImage(file = "assets/userimage_originalcanvas.png")
    canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2, anchor='center', image=newImage1)
    canvas.image = newImage1
    canvas.pack(side=LEFT, pady=10, padx=50)

def changeImage2():
    canvas.delete("all")
    newImage2 = PhotoImage(file = "assets/userimage_detectioncanvas.png")
    canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2, anchor='center', image=newImage2)
    canvas.image = newImage2
    canvas.pack(side=LEFT, pady=10, padx=50)

def changeImage3():
    canvas.delete("all")
    newImage3 = PhotoImage(file = "assets/userimage_measurementcanvas.png")
    canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2, anchor='center', image=newImage3)
    canvas.image = newImage3
    canvas.pack(side=LEFT, pady=10, padx=50)

#
# Function: createImgButtons()
#    - Creates the imageDetection, objectDetection, and mesurementDetection
#      buttons with the matched images from the root folder
#      and apply image to button surface
def createImgButtons():
    rightFrame.destroy()
    rightFrame = Frame(mainFrame, width=255, height=150, bg="#343434")
    rightFrame.pack(side=LEFT, fill=Y, expand=False, anchor=W)

    #count testing purposes
    originalPhoto = PhotoImage(file="assets/3.png")
    originalButton = Button(rightFrame, image=originalPhoto, borderwidth=0, bg="#343434")
    originalButton.image = originalPhoto
    originalButton.pack(padx=8, pady=8)

    objectPhoto = PhotoImage(file="assets/3.png")
    objectButton = Button(rightFrame, image=objectPhoto, borderwidth=0, bg="#343434")
    objectButton.image = objectPhoto
    objectButton.pack(padx=8, pady=8)

    measurementPhoto = PhotoImage(file="assets/3.png")
    measurementButton = Button(rightFrame, image=measurementPhoto, borderwidth=0, bg="#343434")
    measurementButton.image = measurementPhoto
    measurementButton.pack(padx=8, pady=8)
    rightFrame.update_idletasks()

    originalPhoto2 = PhotoImage(file="assets/userimage_originalbutton.gif")
    originalButton.config(image=originalPhoto2, command=changeImage1)
    originalButton.image = originalPhoto2
    rightFrame.update_idletasks()

    time.sleep(1)
    #call object detection function
    ObjectDetection.main()
    objectPhoto2 = PhotoImage(file="assets/userimage_detectionbutton.gif")
    objectButton.config(image=objectPhoto2, command=changeImage2)
    objectButton.image = objectPhoto2
    rightFrame.update_idletasks()

    time.sleep(1)

    #call measurement detection function
    MeasurementDetection.main()
    measurementPhoto2 = PhotoImage(file="assets/userimage_measurementbutton.gif")
    measurementButton.config(image=measurementPhoto2, command=changeImage3)
    measurementButton.image = measurementPhoto2
    rightFrame.update_idletasks()

#initialize root view
root = Tk()

newF = open("./measurement_detection/building_measurements.txt", 'w')
newF.write("")
newF.close()
#override default layout and functionalities
root.overrideredirect(True)
#customize screen size
root.geometry('1280x680+0+0')
print("file called")
topFrame = Frame(root, height=50, padx=10, pady=5, bg="#343434")
topFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

photo = PhotoImage(file="window_thumbnail_icon_52x60.png")
titleImage = Label(topFrame, image=photo, anchor=W, bg="#343434")
titleImage.photo = photo
titleImage.pack(side=LEFT)

titleLabel = Label(topFrame, font=('arial', 12, 'bold'),
                   text="Dimension Detector",
                   bd=5, anchor=W, bg="#343434", fg="white")
titleLabel.pack(side=LEFT)

windowCloseFrame = Frame(topFrame, width=50, height=50)
windowCloseFrame.pack(side=RIGHT)
closeButton = Button(windowCloseFrame, font=('arial', 12, 'bold'), text="X", command=root.destroy, bg="#343434", fg="white")
closeButton.pack()


#MAIN WINDOW
mainFrame = Frame(root, width=1350, height=50, bg="#343434")
mainFrame.pack(side=BOTTOM, fill=BOTH, expand=1, anchor=S)

#Left Frame
leftFrame = Frame(mainFrame, width=125, height=50, bg="#343434", padx=20, pady=12)
leftFrame.pack(side=LEFT, fill=Y, expand=False, anchor=W)


uploadPhoto = PhotoImage(file="assets/1.png")
uploadButton = Button(leftFrame, image=uploadPhoto, command=uploadImageFile)
uploadButton.image = uploadPhoto
uploadButton.pack(pady=8)
#uploadButton = Button(leftFrame, width=6, height=3, font=('arial', 12, 'bold'), text="IMAGE", bg="#343434", fg="white", command=uploadImageFile)
#uploadButton.pack(pady=8)


#linkPhoto = PhotoImage(file="assets/2.png")
#linkButton = Button(leftFrame, image=linkPhoto, command=uploadImageFile)
#linkButton.image = linkPhoto
#linkButton.pack(pady=8)
#secondButton = Button(leftFrame, width=6, height=3, font=('arial', 12, 'bold'), text="LINK", bg="#343434", fg="white")
#secondButton.pack(pady=8)

#Center Frame
centerFrame = Frame(mainFrame, width=900, height=100, bg="#808080")
centerFrame.pack(side=LEFT, fill=Y, expand=False, anchor=W)

canvas = Canvas(centerFrame, width=900, height=500, bg="#808080", borderwidth=0)
canvas.pack(side=LEFT, pady=10, padx=50)

###NOTE: IMAGE HEIGHT MUST BE 500 or less - will need to use opencv to resize
#mainPhotoView = Label(centerFrame, image=mainPhoto, anchor=CENTER, bg="#343434")
#mainPhotoView.photo = photo

#mainPhotoView.place(x=25, y=25, anchor="center")
#mainPhotoView.pack(side=LEFT, pady=10, padx=50)

#Right Frame
rightFrame = Frame(mainFrame, width=255, height=150, bg="#343434")
rightFrame.pack(side=LEFT, fill=Y, expand=False, anchor=W)

#Divides the top and main frames with a small black bar
divider = Frame(root, width=1350, height=5, bg="black")
divider.pack(side=BOTTOM, fill=X, expand=False, anchor=S)

#Closes application when escape button is pressed
root.bind('<Escape>', lambda e: root.destroy())

root.mainloop()
