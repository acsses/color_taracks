# -*- coding: utf-8 -*-
import numpy as np
import cv2
import json
import smbus    

cap = cv2.VideoCapture(0)

while(1):
    bus = smbus.SMBus(1)
    adress = 0x04 
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_light_pink = np.array([0, 100, 53])
    upper_light_pink = np.array([0, 100, 100])
    lower_black = np.array([0,0,0])
    upper_black =np.array([0,0,80])
    mask = cv2.inRange(hsv, lower_light_pink, upper_light_pink)
    mask_line = cv2.inRange(hsv,lower_black,upper_black)

    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('balck',mask_line)

    contours , hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    balck_rect , black_shape = cv2.findContours(mask_line, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    rects_black = []
    tar=[0,0,0,0]
    i = 0
    file =open('test.json','w')
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
    for target in balck_rect:
        approx_black = cv2.convexHull(target)
        rect_black = cv2.boundingRect(approx_black)
        rects_black.append(np.array(rect_black))
    if len(rects) > 0:
      rect = max(rects, key=(lambda x: x[2] * x[3]))
      cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
      key = ["x","y","xw","yh"]
      tar = rect.tolist()
      key=["x","y","xw","yh"]
      dic=dict(zip(key,tar))
      bus.write_byte(adress, dic)
      print(dic)
      json.dump(dic,file)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindo