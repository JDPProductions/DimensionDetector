import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

objects = []
buildings = []
finalBuilding = []

def evaluationOnObject(building):
    estimations = []
    estimation = 0.0

    buildingBottomY = float(building[1])
    buildingTopY = float(building[2])
    buildingLeftX = float(building[3])
    buildingRightX = float(building[4])

    for obj in objects:
        if((obj[0] == "2") or (obj[0] == "9")):
            objectBottomY = float(obj[1])
            objectTopY = float(obj[2])
            objectLeftX = float(obj[3])
            objectRightX = float(obj[4])

            #is object bottomY between buildingBottomY and buildingTopY
            #is object topY between buildingBottomY and buildingTopY
            if((buildingBottomY >= objectBottomY) and (objectTopY >= buildingTopY)):
                    if((objectLeftX >= buildingLeftX) and (buildingRightX >= objectRightX)):
                        objHeight = float(obj[5])
                        buildingPixelHeight = buildingBottomY - buildingTopY
                        objectPixelHeight = objectBottomY - objectTopY
                        buildingHeight = (objHeight / objectPixelHeight) * buildingPixelHeight
                        estimations.append(buildingHeight)
    for est in estimations:
        estimation = estimation + est

    if (len(estimations) != 0):
        estimation = estimation / len(estimations)
    else:
        estimation = 0
    return estimation

def evaluationOffObject(building):
    estimations = []
    estimation = 0.0

    buildingBottomY = float(building[1])
    buildingTopY = float(building[2])
    buildingLeftX = float(building[3])
    buildingRightX = float(building[4])

    for obj in objects:
        if((obj[0] != "1") and (obj[0] != "2") and (obj[0] != "9")):
            objectBottomY = float(obj[1])
            objectTopY = float(obj[2])
            objectLeftX = float(obj[3])
            objectRightX = float(obj[4])

            if(((objectTopY < buildingBottomY) and (objectTopY >= buildingTopY)) or
                ((objectBottomY > buildingTopY) and (objectBottomY <= buildingBottomY))):
                if(((objectLeftX < buildingRightX) and (objectLeftX >= buildingLeftX)) or
                    ((objectRightX > buildingLeftX) and (objectRightX <= buildingRightX))):

                    overlapBottomY = 0.0
                    overlapTopY = 0.0
                    overlapLeftX = 0.0
                    overlapRightX = 0.0

                    if(buildingBottomY <= objectBottomY):
                        overlapBottomY = buildingBottomY
                    else:
                        overlapBottomY = objectBottomY
                    if(objectTopY <= buildingTopY):
                        overlapTopY = buildingTopY
                    else:
                        overlapTopY = objectTopY
                    if(overlapLeftX >= buildingLeftX):
                        overlapLeftX = buildingLeftX
                    else:
                        overlapLeftX = objectLeftX
                    if(buildingRightX <= objectRightX):
                        overlapRightX = buildingRightX
                    else:
                        overlapRightX = objectRightX

                    overlapPixelWidth = overlapRightX - overlapLeftX
                    overlapPixelHeight = overlapBottomY - overlapTopY
                    objectPixelHeight = objectBottomY - objectTopY
                    objectPixelWidth = objectRightX - objectLeftX

                    overlapArea = overlapPixelWidth * overlapPixelHeight
                    objectArea = objectPixelWidth * objectPixelHeight

                    overlapPercentage = overlapArea / objectArea

                    if(overlapPercentage > 0.6):
                        objHeight = float(obj[5])
                        buildingPixelHeight = buildingBottomY - buildingTopY
                        buildingHeight = (objHeight / objectPixelHeight) * buildingPixelHeight
                        estimations.append(buildingHeight)

    for est in estimations:
        estimation = estimation + est
    if (len(estimations) != 0):
        estimation = estimation / len(estimations)
    else:
        estimation = 0
    return estimation

def evaluationFloorCount(building):
    estimation = 0.0
    windows = []
    doors = []

    buildingBottomY = float(building[1])
    buildingTopY = float(building[2])
    buildingLeftX = float(building[3])
    buildingRightX = float(building[4])

    for obj in objects:
        if((obj[0] == "2") or (obj[0] == "9")):

            objectBottomY = float(obj[1])
            objectTopY = float(obj[2])
            objectLeftX = float(obj[3])
            objectRightX = float(obj[4])

            if((buildingBottomY >= objectBottomY) and (objectTopY >= buildingTopY)):
                    if((objectLeftX >= buildingLeftX) and (buildingRightX >= objectRightX)):
                        if(obj[0] == "2"):
                            windows.append(obj)
                        if(obj[0] == "9"):
                            doors.append(obj)

    finalWindows = windows
    containsDoor = False
    for window in windows:
        windowBottomY = float(window[1])
        for door in doors:
            containsDoor = True
            doorTopY = float(door[2])
            if(windowBottomY > doorTopY):
                finalWindows.remove(window)


    maxFloorCount = 1
    otherWindows = finalWindows
    count = 0
    for window in finalWindows:
        otherWindows = []
        currentWindowBottomY = float(window[1])
        currentWindowTopY = float(window[2])
        currentWindowLeftX = float(window[3])
        currentWindowRightX = float(window[4])

        for test in finalWindows:
            if (test != window):
                otherWindows.append(window)
        #issue with removing from a different array - affects the original array somehow
        #otherWindows.pop(count)
        floorCount = 1

        for referenceWindow in otherWindows:
            #count = count + 1
            #print("HERE" + str(count))
            referenceWindowBottomY = float(referenceWindow[1])
            referenceWindowTopY = float(referenceWindow[2])
            referenceWindowLeftX = float(referenceWindow[3])
            referenceWindowRightX = float(referenceWindow[4])

            if((referenceWindowLeftX > (currentWindowRightX + 5)) or (referenceWindowRightX < (currentWindowLeftX + 5))):
                continue
            else:
                if((referenceWindowBottomY < (currentWindowTopY + 5)) or (referenceWindowTopY > (currentWindowBottomY + 5))):
                    floorCount = floorCount + 1
        #otherWindows = finalWindows
        if(floorCount > maxFloorCount):
            maxFloorCount = floorCount

    if(containsDoor == True):
        maxFloorCount = maxFloorCount + 1
    #estimation = ((3.5* maxFloorCount) + 9.625 + (2.625 * (maxFloorCount/25))) * 3.28
    estimation = 10 * 12 * maxFloorCount

    #((3.5* maxFloorCount) + 9.625 + (2.625 * (maxFloorCount/25))) * 39.3701
    if(maxFloorCount == 0):
        estimation = 0

    return estimation

def createImage():
    measurements = []
    with open("./demo_samples/imageToUse.txt") as f:
        for line in f:
            imagename = line
    img = Image.open('./demo_samples/'+ imagename +'.png').convert('RGBA')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf",60)

    with open("./measurement_detection/building_measurements.txt") as f:
        for line in f:
            seperateMeasurement = line.split()
            measurements.append(seperateMeasurement)

        for measurement in measurements:
            yBottomCoord = int(float(measurement[1]))
            yTopCoord = int(float(measurement[2]))
            xLeftCoord = int(float(measurement[3]))
            xRightCoord = int(float(measurement[4]))
            predictedHeight = float(measurement[7])
            #actual - expected / actual * 100 = percent error
            actualBuildingHeight = measurement[5]
            if(actualBuildingHeight != "0"):
                #we know the height of the building
                percentError = abs(((float(actualBuildingHeight) - predictedHeight) / float(actualBuildingHeight)) * 100)
            else:
                percentError = 0

            draw.rectangle((xLeftCoord, yBottomCoord, xRightCoord, yTopCoord), outline ='red')
            draw.rectangle((xLeftCoord+1, yBottomCoord+1, xRightCoord+1, yTopCoord+1), outline ='red')
            draw.rectangle((xLeftCoord+2, yBottomCoord+2, xRightCoord+2, yTopCoord+2), outline ='red')
            draw.rectangle((xLeftCoord+3, yBottomCoord+3, xRightCoord+3, yTopCoord+3), outline ='red')
            draw.rectangle((xLeftCoord+4, yBottomCoord+4, xRightCoord+4, yTopCoord+4), outline ='red')
            draw.text((xLeftCoord,yTopCoord - 60), "Height: " + str(float(predictedHeight/12)) + "ft   % Error: " + str(int(percentError)) + "   Actual Height: " + str(int(float(actualBuildingHeight)/12)) + "ft", font = font)

    img.save("./measurement_detection/userimage_measurement.png")

    width = int(img.size[0])
    height = int(img.size[1])

    canvasDimsHeight = 500
    canvasDimsWidth = int((500 / height) * width)
    canvasImg = img.resize((canvasDimsWidth, canvasDimsHeight), Image.ANTIALIAS)
    canvasImg.save("./assets/userimage_measurementcanvas.png")

    buttonDimsHeight = 160
    buttonDimsWidth = 220
    buttonImg = img.resize((buttonDimsWidth, buttonDimsHeight), Image.ANTIALIAS)
    buttonImg.save("./assets/userimage_measurementbutton.gif")

def main():

    print("measurement file called")

    objectDetectionFile = "./object_detection/userimage_detection.txt"

    with open(objectDetectionFile) as f:
        for line in f:
            seperateObject = line.split()
            objects.append(seperateObject)

        for obj in objects:
            if obj[0] == "1":
                buildings.append(obj)

        newF = open("./measurement_detection/building_measurements.txt", 'w')
        for building in buildings:
            #EVALUATION ESTIMATION 1
            estimation1 = evaluationOnObject(building)
            #EVALUATION ESTIMATION 2
            estimation2 = evaluationOffObject(building)
            #EVALUATION ESTIMATION 3
            estimation3 = evaluationFloorCount(building)

            divideCount = 0
            if(estimation1 != 0):
                divideCount = divideCount + 1
            if(estimation2 != 0):
                divideCount = divideCount + 1
            if(estimation3 != 0):
                divideCount = divideCount + 1
            if(divideCount == 0):
                print("Measurement detection could not find any estimations.")
                average = 0
            else:
                #averages the estimations. Currently weight for each estimation is equal
                # the * 1 attached to each estimation is the weight for those estimations

                average = ((estimation1 * 0.3) + (estimation2 * 0.2) + (estimation3 * 0.5))

            building[7] = average

            for data in building:
                newF.write(str(data) + " ")
            newF.write("\n")
        newF.close()
        createImage()
