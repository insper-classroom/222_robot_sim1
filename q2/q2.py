#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np
import hough_helper
import fotogrametria

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
imgname = "bandeiras.png"

if __name__ == "__main__":

    frame = cv2.imread(imgname)
    
    # Our operations on the frame come here
    img = frame.copy()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, method=cv2.HOUGH_GRADIENT, dp=1, minDist=200, param1=80, param2=40, minRadius=20, maxRadius=40)
    img = hough_helper.desenha_circulos(img, circles)

    for circle in circles[0]:
        x0, y0, r = circle
        roi = img[int(y0-3*r):int(y0+3*r), int(x0-4*r):int(x0+4*r)]
        cv2.imshow(f"({x0},{y0})", roi)

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv,(30,25,39),(82,255,255))
        contorno = fotogrametria.encontrar_maior_contorno(mask_green)
        x,y,w,h = cv2.boundingRect(contorno)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),2)


    # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
    cv2.imshow('Input', frame)
    cv2.imshow('Output', img)

    cv2.waitKey()
    cv2.destroyAllWindows()

