#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np
import fotogrametria

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
videos = [
    "attempt1.mp4",
    "attempt2.mp4",
    "attempt3.mp4"
]

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

def meteoro_acertou(bgr):
    """
    Identifica se o meteoro acertou o personagem e imprime  resposta na imagem,
    junto com os bounding boxes e imprimir as profundidades no terminal
    """ 

    img = bgr.copy()
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # Você deverá trabalhar aqui
    # 1 - Encontrar o distancia focal

    green_lama = cv2.imread('green_lama.png')
    foco = fotogrametria.encontrar_foco(60, 180, green_lama.shape[0])

    print(f"Distancia focal: {foco}")

    # Segmenta o meteoro e personagem
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Meteoro
    mask_meteoro = cv2.inRange(hsv,(0,0,37),(9,255,255))
    cv2.imshow("Mask meteoro", mask_meteoro)
    # Green Lama
    mask_green = cv2.inRange(hsv,(30,25,39),(82,255,255))
    mask_green = cv2.morphologyEx(mask_green,cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    cv2.imshow("Mask personagem", mask_green)

    # Bounding box meteoro
    contorno_meteoro = fotogrametria.encontrar_maior_contorno(mask_meteoro)
    x,y,w,h_m = cv2.boundingRect(contorno_meteoro)
    bb_meteoro = [x, y, x+w, y+h_m]
    cv2.rectangle(img,(x,y),(x+w,y+h_m),(0,0,255),2)

    # Bounding box personagem
    contorno_lama = fotogrametria.encontrar_maior_contorno(mask_green)
    x,y,w,h_g = cv2.boundingRect(contorno_lama)
    bb_lama = [x, y, x+w, y+h_g]
    cv2.rectangle(img,(x,y),(x+w,y+h_g),(0,255,0),2)

    # Calcular as distancias
    dist_meteoro = fotogrametria.encontrar_distancia(foco, 98.1, h_m)
    dist_green = fotogrametria.encontrar_distancia(foco, 180, h_g)
    print(f"Distancia meteoro: {dist_meteoro} cm")
    print(f"Distancia personagem: {dist_green} cm")

    iou = bb_intersection_over_union(bb_lama, bb_meteoro)

    if iou > 0.1 and abs(dist_meteoro - dist_green) < 40:
        cv2.putText(img, "ACERTOU", (200,200), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

    return img


if __name__ == "__main__":

    for video in videos:
        # Inicializa a aquisição da webcam
        cap = cv2.VideoCapture(video)

        print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret == False:
                #print("Codigo de retorno FALSO - problema para capturar o frame")
                #cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                break

            # Our operations on the frame come here
            img = meteoro_acertou(frame.copy())

            # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
            cv2.imshow('Input', frame)
            cv2.imshow('Output', img)

            # Pressione 'q' para interromper o video
            if cv2.waitKey(1000//30) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

