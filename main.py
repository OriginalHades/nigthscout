import requests as req
import sys
from PIL import Image, ImageDraw, ImageFont
import json
import random
import os
from datetime import datetime,timedelta


widthInPixels = 1024
heightInPixels = 300

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

imageHeight = heightInPixels
imageWidth = widthInPixels
colorDiference = 20

img = Image.new('RGB', (imageWidth, imageHeight), color = 'black')

draw = ImageDraw.Draw(img)
draw.line((0,imageHeight - 3.9 * 18,imageWidth,imageHeight - 3.9 * 18), fill = (100,100,100),width=2)
draw.line((0,imageHeight - 10 * 18,imageWidth,imageHeight - 10 * 18), fill = (100,100,100),width=2)

fontSize = 10
font = ImageFont.truetype("Roboto-Black.ttf", fontSize)


colorBlackList = []

formatedData = []

for a in rawData:
    formatedData.append([])

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

(h, m, s) = current_time.split(':')
currentTime = int(h) * 60 + int(m)
#print(currentTime,3*60,current_time)

scaler = widthInPixels / (3*60)

for a in formatedData:
    for i in reversed(range(0,3*60)):
        a.append({
            "time":str(timedelta(minutes=currentTime-i))[:-3],
            "draw":False,
            "index":abs(i-180)
            })
        
scaler = widthInPixels / (historyCount * 5)

for i,data in enumerate(formatedData):
        print(rawData[i]["link"])
        errors = []
        for b in rawData[i]["data"]:
            try:
                time = b["dateString"]
                time = ":".join([str(int(time.split("T")[1].replace("Z","").split(":")[:2][0])+2),time.split("T")[1].replace("Z","").split(":")[:2][1]])
                #print(time)
                for j,c in enumerate(data):
                    if str(c["time"]) == str(time):
                        temp_data = data[j]
                        data[j] = {
                            "time":temp_data["time"],
                            "draw":True,
                            "index":temp_data["index"],
                            "sgv":b["sgv"]
                        }
            except Exception as err:
                errors.append(err)
        if errors != []:
            print(errors)
        
c = 0            
for i in range(0,3*60):
    if c == 9:
        c = 0
        timeString = str(timedelta(minutes=currentTime-abs(i-180)))[:-3]
        draw.line(((i*scaler),imageHeight,(i*scaler),imageHeight - 10), fill=(225,225,225),width = 2)
        draw.text(((i*scaler)-((font.getsize(timeString)[0])/2), imageHeight - fontSize - 12),timeString,(255,255,255),font=font)
    else:
        c += 1    
           
#draw.line(0,(i*scaler),imageHeight - int(b["sgv"]), fill=randomColor,width = 4)

for data in formatedData:
    while True:
                randomColor = (random.randrange(0,225),random.randrange(0,225),random.randrange(0,225))
                if not randomColor in colorBlackList:
                    for i in range(0,colorDiference):
                        colorBlackList.append((randomColor[0]+i-(colorDiference/2),randomColor[1]+i-(colorDiference/2),randomColor[2]+i-(colorDiference/2)))
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
            if(b["sgv"] > 40):
                if(last["sgv"] > 40):
                    draw.line((int(last["index"]) * scaler,imageHeight - int(last["sgv"]),int(b["index"]) * scaler,imageHeight - int(b["sgv"])), fill=randomColor,width = 4)
                    last = b
                else:
                    draw.line((int(b["index"]) * scaler,imageHeight - int(b["sgv"]),int(b["index"]) * scaler,imageHeight - int(b["sgv"])), fill=randomColor,width = 4)
                    last = b
    #print(dat)
img.save("image.jpg")
#img.show()
