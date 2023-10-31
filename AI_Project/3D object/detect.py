import torch
import pandas
import cv2

def process(img_bgr,model):
    xA,yA,xB,yB = 0,0,0,0
    send_P=[]
    result=model(img_bgr)
    for box in result.xyxy[0]:         
        xA = int(box[0])
        yA = int(box[1])
        xB = int(box[2])
        yB = int(box[3])
    cv2.rectangle(img_bgr, (xA, yA), (xB, yB), (0, 255, 0), 2)
    
    gx=int((xB-xA)//2+xA)
    send_P.append(gx)
    gy=int((yB-yA)//2+yA)
    send_P.append(gy)
    cv2.circle(img_bgr, (gx, gy), 10, (255, 255, 0), -1, cv2.LINE_AA)
            
    return img_bgr,send_P

def modDel():
    model=torch.hub.load('ultralytics/yolov5','custom','./weights/realFinal.pt')
    model.conf=0.4
    return model
