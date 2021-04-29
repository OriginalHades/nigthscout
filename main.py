import requests as req
import sys
from PIL import Image, ImageDraw, ImageFont
import json
import random
import os
from datetime import datetime,timedelta


widthInPixels = 1400
heightInPixels = 1024

verticalOffset = 60

rawData = []
historyCount = 36

for a in open("links.txt","r").read().split("\n"):
    try:
        print(a.strip() + "api/v1/entries/sgv?count="+str(historyCount))
        data = json.loads(req.get(a.strip() + "api/v1/entries/sgv?count="+str(historyCount),headers={"accept":"application/json"}).text)
        parsedData = {
            "link":a.strip(),
            "data":data
        }
        rawData.append(parsedData)
        print("success")
    except Exception as err:
        print(err)
        
#print("= " * 25) 

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

imageHeight = heightInPixels
imageWidth = widthInPixels
colorDiference = 20

img = Image.new('RGB', (imageWidth, imageHeight), color = 'black')

fontSize = 10
font = ImageFont.truetype("Roboto-Black.ttf", fontSize)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

(h, m, s) = current_time.split(':')
currentTime = int(h) * 60 + int(m)

scaler = widthInPixels / (3*60)

draw = ImageDraw.Draw(img)
draw.line((0,imageHeight - translate(3.9 * 18,40,400,0,imageHeight)-verticalOffset,imageWidth,imageHeight - translate(3.9 * 18,40,400,0,imageHeight)-verticalOffset), fill = (100,100,100),width=2)
draw.line((0,imageHeight - translate(10 * 18,40,400,0,imageHeight)-verticalOffset,imageWidth,imageHeight - translate(10 * 18,40,400,0,imageHeight)-verticalOffset), fill = (100,100,100),width=2)

draw.rectangle((0,0,imageWidth,imageHeight - translate(10 * 18,40,400,0,imageHeight)-verticalOffset), fill ="#331111")
draw.rectangle((0,imageHeight - translate(3.9 * 18,40,400,0,imageHeight)-verticalOffset,imageWidth,imageHeight), fill ="#331111")

for a in range(22):
    draw.line((imageWidth-10,imageHeight - translate(a * 18,40,400,0,imageHeight)-verticalOffset,imageWidth,imageHeight - translate(a * 18,40,400,0,imageHeight)-verticalOffset), fill = (100,100,100),width=2)
    draw.text((imageWidth-(fontSize*len(str(a)))-10,imageHeight - translate(a * 18,40,400,0,imageHeight)-verticalOffset-5,imageWidth),str(a),(255,255,255),font=font)

c = 0            
for i in range(0,3*60):
    if c == 9:
        c = 0
        timeString = str(timedelta(minutes=currentTime-abs(i-180)))[:-3]
        draw.line(((i*scaler),imageHeight,(i*scaler),imageHeight - 10), fill=(225,225,225),width = 2)
        draw.text(((i*scaler)-((font.getsize(timeString)[0])/2), imageHeight - fontSize - 12),timeString,(255,255,255),font=font)
    else:
        c += 1    


colorBlackList = [(0,0,0),(51,17,17)]
formatedData = []

for a in rawData:
    formatedData.append([])

for a in formatedData:
    for i in reversed(range(0,3*60)):
        a.append({
            "time":str(timedelta(minutes=currentTime-i))[:-3],
            "draw":False,
            "index":abs(i-180)
            })
        
for i,data in enumerate(formatedData):
        for b in rawData[i]["data"]:
                time = str(timedelta(seconds=b["date"]/1000))
                time = time.split(" ")[2][:time.split(" ")[2].rfind(":")]
                time = time.split(":")
                time[0] = str(int(time[0])+2)
                time = ":".join(time)
                for j,c in enumerate(data):
                    if str(c["time"]) == str(time):
                        temp_data = data[j]
                        data[j] = {
                            "time":temp_data["time"],
                            "draw":True,
                            "index":temp_data["index"],
                            "sgv":b["sgv"]
                        }
           
#draw.line(0,(i*scaler),imageHeight - int(b["sgv"]), fill=randomColor,width = 4)

for data in formatedData:
    while True:
                randomColor = (random.randrange(0,225),random.randrange(0,225),random.randrange(0,225))
                if not randomColor in colorBlackList:
                    for i in range(0,colorDiference):
                        colorBlackList.append((int(randomColor[0]+i-(colorDiference/2)),int(randomColor[1]+i-(colorDiference/2)),int(randomColor[2]+i-(colorDiference/2))))
                    
                    break
                
    #print(randomColor)
    lastEmpty = False
    last = {
        "sgv":0,
        "index":0
    }
    dat = 0
    for b in data:
        if b["draw"]:
            dat += 1
            if(last["sgv"] > 40):
                lastSgv = translate(last["sgv"],40,400,0,imageHeight)
                sgv = translate(b["sgv"],40,400,0,imageHeight)
                draw.line((int(last["index"]) * scaler,imageHeight - int(lastSgv) - verticalOffset,int(b["index"]) * scaler,imageHeight - int(sgv) - verticalOffset), fill=randomColor,width = 4)
                last = b
            else:
                sgv = translate(b["sgv"],40,400,0,imageHeight)
                draw.line((int(b["index"]) * scaler,imageHeight - int(sgv) - verticalOffset,int(b["index"]) * scaler,imageHeight - int(sgv) - verticalOffset), fill=randomColor,width = 4)
                last = b

    #print(dat)
img.save("image.jpg")
#img.show()
