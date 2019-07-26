# -*- coding: utf-8 -*-
import numpy as np
import cv2
import json

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_light_pink = np.array([168, 100, 100])
    upper_light_pink = np.array([188, 255, 255])
    mask = cv2.inRange(hsv, lower_light_pink, upper_light_pink)

    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    contours , hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    
    file =open('test.pos','w')
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
    if len(rects) > 0:
      rect = max(rects, key=(lambda x: x[2] * x[3]))
      cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
      print(rect)
      file.writelines(str(rect))
      file.close()
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindo