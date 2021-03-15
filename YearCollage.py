#!/usr/bin/python

from tkinter import *
from tkinter import filedialog
import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageOps
import math
import random
from tkinter import ttk

def main():
    runApp()
    
def runApp():
    global app
    app = Tk()
    app.title("Year Collage")
    app.geometry('900x600')
    labelForDirChooser = Label(app, text="Select Directory") 
    labelForDirChooser.place(x=5, y=5)
    # creating a box for selecting where the images are
    global dirLocBox
    dirLocBox = Entry(app, width=30) 
    dirLocBox.insert(0,"Directory...")
    dirLocBox.place(x=10, y=30)
    browseInputButton = Button(app, text="Browse", command=selectDirectory)
    browseInputButton.place(x=200, y=30)

    #selecting directory where the output image will be saved
    labelForOutputDir = Label(app, text="Output Directory")
    labelForOutputDir.place(x=280, y=5)
    global dirLocOutput
    dirLocOutput = Entry(app,width=30)
    dirLocOutput.insert(0,"D:/")
    dirLocOutput.place(x=290, y=30)
    browseOutputButton = Button(app, text="Browse", command=selectOutputDir)
    browseOutputButton.place(x=480,y=30)
    #Box for input the text i.e year
    labelForYearSelection = Label(app, text="Select Year")
    labelForYearSelection.place(x=5, y=55)
    inputOfYears = Entry(app, width=30)
    inputOfYears.place(x=10, y=80)

    #Selection options of output image size
    labelForImageSize = Label(app, text="Select Image Size")
    labelForImageSize.place(x=5, y=105)
    IMAGESIZE = ['1200x800','2100x1400','3000x2000','4500x3000','5400x3600', '6000x4000', '7500x5000', '9600x6400','12000x8000']
    var = StringVar(app)
    var.set(IMAGESIZE[0])
    sizeOptions = OptionMenu(app, var, *IMAGESIZE)
    sizeOptions.place(x=10, y=130)
    btLabel = Label(app, text="Border Thickness")
    btLabel.place(x=630, y=270)
    global borderThickness
    borderThickness = Scale(app, from_= 0, to=5, orient= HORIZONTAL)
    borderThickness.set(2)
    borderThickness.place(x=630, y=290)
    dgLabel = Label(app, text="Degree + -")
    dgLabel.place(x=630, y=340)
    global degreeLevel
    degreeLevel = Scale(app, from_ = 0, to=50, orient = HORIZONTAL)
    degreeLevel.set(30)
    degreeLevel.place(x=630, y=360)
    imsLabel = Label(app, text="Images Size")
    imsLabel.place(x=630, y=410)
    global ims
    ims = Scale(app, from_ = 1, to=6, orient = HORIZONTAL, resolution=0.2)
    ims.set(2.0)
    ims.place(x=630, y=430)
    #previewing the output image
    imagePreviewLabel = Label(app, text="Image Preview")
    imagePreviewLabel.place(x=10, y=165)
    global imagePreview
    imagePreview = Canvas(app, width=600, height = 400, borderwidth=2, relief="solid")
    imagePreview.place(x=10, y=190)
    generate = Button(app, text="Generate", width=20, command=lambda : generateImage(inputOfYears.get(), var.get()))
    generate.place(x=630,y=190)
    
    app.mainloop()
    
def selectDirectory(): #funtion of input directory selection triggered on browse button
    dirLocBox.delete(0,END)
    dirLocBox.insert(0, filedialog.askdirectory())
def selectOutputDir(): #function of output directory selection triggered on browse button
    dirLocOutput.delete(0,END)
    dirLocOutput.insert(0,filedialog.askdirectory())
def generateImage(year, imageSize):
    imageWidth = int(imageSize.split('x')[0]) #taking the output image width & height from the given image size
    imageHeight = int(imageSize.split('x')[1])
    orignalImage = Image.new('RGB', (imageWidth,imageHeight ), color = (215, 215, 219)) #draws a image with grey color background of the given size
    fontSize = math.floor(imageWidth/100*45) #font size in ratio of image width
    fontForYear = ImageFont.truetype("arial.ttf",fontSize)
    textPlacing = math.floor(imageWidth/100*10) #vertical placing of the text
    drawObject = ImageDraw.Draw(orignalImage)
    drawObject.text((5,textPlacing), year, font=fontForYear, fill=(255,255,255)) #writes text, for which the output is being generated, on the image
    pathName = dirLocOutput.get() +'/'+ year+'.jpeg' #saves the image with change i.e text on it
    orignalImage.save(pathName, dpi=(1000,1000))
    global pleaseWait
    pleaseWait = Label(app, text="Please wait, Image is being generated...")
    pleaseWait.place(x=630, y=220)
    app.update()
    placeImages(pathName) #Calls the fucntion which will place the images
    pleaseWait.configure(text="Image Generated")
    im = Image.open(pathName)
    im.thumbnail((600,400), Image.ANTIALIAS)
    im = ImageTk.PhotoImage(im)
    label = Label(image=im)
    label.image = im
    imagePreview.create_image(0,0, anchor=NW, image=label.image)
    Image.open(pathName).show()

def placeImages(imageLocation):
    global progressbar
    inputDir = dirLocBox.get()
    orignalImage = Image.open(imageLocation).convert("RGBA") #opens the saved image
    images = os.listdir(inputDir) #takes all the images in the directory
    global tempImsize
    tempImsize = (math.floor(orignalImage.size[0]/100*float(ims.get())),math.floor(orignalImage.size[0]/100*(1.35 * float(ims.get())))) #size of the images which will be pasted on the original image
    locationsOfPlacing = findLoc(imageLocation, len(images)) #call the function which will find the places where images should be pasted
    sizeReduceLevel = 0.2
    while locationsOfPlacing is None:
        tempImsize = (math.floor(orignalImage.size[0]/100*(float(ims.get())-sizeReduceLevel)),math.floor(orignalImage.size[0]/100*((1.35 * float(ims.get()))-sizeReduceLevel)))
        locationsOfPlacing = findLoc(imageLocation, len(images))
        sizeReduceLevel = sizeReduceLevel + 0.2
    orignalImage = Image.new('RGB', (orignalImage.size), color = (255,255,255)) #replaces the current orignal image with a image which has no text
    counter = 0
    progress_var = DoubleVar()
    progressbar = ttk.Progressbar(app, variable=progress_var, maximum=len(locationsOfPlacing))
    progressbar.place(x=630, y=250)
    for image in images:
        tempImage = Image.open(inputDir+"/"+image) #opens images one by one
        tempImage.thumbnail(tempImsize, Image.LANCZOS)
        tempImage = ImageOps.expand(tempImage, border=int(borderThickness.get()), fill='black') #gives them a black border
        rotationDegree = random.randint(5,int(degreeLevel.get())+6) if random.randint(0,1)==0 else random.randint(360-int(degreeLevel.get())-6,355) #finding rotation degree randomly between the degrees 10 to 2 O'clock
        #tempImage.thumbnail(tempImsize,Image.ANTIALIAS) #resize them to paste it
        tempImage = tempImage.convert("RGBA")
        tempImage = tempImage.rotate(rotationDegree, expand=True)#rotate them
        if counter in range(0, len(locationsOfPlacing)):
            currentPlacingLoc = locationsOfPlacing[counter] #takes one placing location from the found locations
        else:
            break
        progress_var.set(counter)
        pleaseWait.configure(text="Placing images...  " + str(counter) + "/" + str(len(locationsOfPlacing)))
        app.update()
        counter = counter+1
        orignalImage.paste(tempImage, (currentPlacingLoc), tempImage) #pastes them on them image
    orignalImage.save(imageLocation, dpi=(1000,1000))
    extraCounter = len(images)
    while extraCounter < len(locationsOfPlacing):
        imageindex = random.randint(0,len(images)-1)
        tempImage = Image.open(inputDir+"/"+images[imageindex]) #opens images one by one
        tempImage.thumbnail(tempImsize, Image.LANCZOS)
        tempImage = ImageOps.expand(tempImage, border=int(borderThickness.get()), fill='black') #gives them a black border
        rotationDegree = random.randint(3,25) if random.randint(0,1)==0 else random.randint(335,358) #finding rotation degree randomly between the degrees 10 to 2 O'clock
        #tempImage.thumbnail(tempImsize,Image.ANTIALIAS) #resize them to paste it
        tempImage = tempImage.convert("RGBA")
        tempImage = tempImage.rotate(rotationDegree, expand=True)#.resize(tempImsize)#rotate them
        if counter in range(0, len(locationsOfPlacing)):
            currentPlacingLoc = locationsOfPlacing[counter] #takes one placing location from the found locations
        else:
            break
        progress_var.set(counter)
        pleaseWait.configure(text="Placing images...  " + str(counter) + "/" + str(len(locationsOfPlacing)))
        app.update()
        counter = counter+1
        orignalImage.paste(tempImage, (currentPlacingLoc), tempImage) #pastes them on them image
        extraCounter = extraCounter + 1
    orignalImage.save(imageLocation, dpi=(1000,1000))#finally saving the orignal image
def findLoc(imagename, nImages): #this function track the text on the orignal image to find the locations where images should be pasted
    img = Image.open(imagename) #opens the orignal image
    pix = img.load() #convert it to rgb pixels values
    halfTIS = (math.floor(tempImsize[0]/2), math.floor(tempImsize[1]/2)) 
    locations= []
    flag = False
    x = 0
    y = math.floor(img.size[1]/10)-10
    widthIterator = img.size[0]
    heightIterator = img.size[1]
    countx = 0
    #now it will iterate through whole image and find the white pixels (of text) from the background of grey
    while x < widthIterator :
        while y < heightIterator :
            r, g, b = pix[x,y]
            if r==255 and g==255 and b==255: #if the rgb values are for white color
                locations.append((x-halfTIS[0], y-halfTIS[1])) #saves the location where pic should be placed
                y = y + tempImsize[1] #if pixel found them move down the image height size to find next locations to avoid overlaping of images
                flag = True
                countx = countx + 1
                continue
            y = y+1
        if flag is True:
            x = x + tempImsize[0]#if pixels found move width size to find next locations to avoid overlaping of images
            flag = False
        elif countx > 1:
            x = x + 1
            countx = 0
        else:
            x = x + math.floor(tempImsize[0]/2)
            countx = 0
        y = math.floor(img.size[1]/10)-10

    if len(locations) < nImages:
           return None
    pixels = img.load()
    index = 0
    var = DoubleVar()
    progressbar = ttk.Progressbar(app, variable=var, maximum=len(locations))
    progressbar.place(x=630, y=250)
    while index < len(locations):
        tempLocx = findBestLocation(locations[index], pixels)
        if tempLocx is None:
            locations.pop(index)
        else:
            locations[index] = tempLocx
        pleaseWait.configure(text = "Finding best locations for images...  " + str(index) + "/" + str(len(locations)))
        var.set(index)
        app.update()
        index = index + 1
    return locations

def findBestLocation(currentLoc, pixels):
    halfTIS = (math.floor(tempImsize[0]/6), math.floor(tempImsize[1]/6))
    if isOnBestLocation(currentLoc, pixels):
        return (currentLoc)
    newLoc = (currentLoc[0] + halfTIS[0], currentLoc[1] - halfTIS[1]) #pull top right
    if isOnBestLocation(newLoc, pixels):
        return newLoc
    newLoc = (currentLoc[0] - halfTIS[0], currentLoc[1] - halfTIS[1]) #pull top left
    if isOnBestLocation(newLoc, pixels):
        return newLoc
    newLoc = (currentLoc[0] + halfTIS[0], currentLoc[1] + halfTIS[1]) #pull bottom right
    if isOnBestLocation(newLoc, pixels):
        return newLoc
    newLoc = (currentLoc[0] - halfTIS[0], currentLoc[1] + halfTIS[1]) #pull bottom left
    if isOnBestLocation(newLoc, pixels):
        return newLoc
    return None

def isOnBestLocation(loc, pixels):
    pixOnTrack = 0
    x = 0
    y = 0
    while x < tempImsize[0]:
        while y < tempImsize[1]:
            r, g, b = pixels[loc[0] + x, loc[1] + y]
            app.update()
            if r == 255 and g == 255 and b==255:
                pixOnTrack = pixOnTrack + 1
            y = y+1
        x = x + 1
        y = 0
    percent = pixOnTrack / (tempImsize[0] * tempImsize[1]) * 100
    if percent > 40:
        return True
    else:
        return False
    
if __name__ == "__main__": main()
