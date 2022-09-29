#! /usr/bin/env python3
# -*- coding:utf-8 -*-


from __future__ import print_function, division
import rospy
import numpy as np
import math
import cv2
import time
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Vector3, Pose, Vector3Stamped

from nav_msgs.msg import Odometry

import object_detection_webcam as mnet

bridge = CvBridge()

cv_image = None

results = None

# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
    print("frame")
    global cv_image
    global results

    try:
        temp_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        cv_image = temp_image.copy()
        img_out, results = mnet.detect(cv_image)
        # ATENÇÃO: ao mostrar a imagem aqui, não podemos usar cv2.imshow() dentro do while principal!! 
        cv2.imshow("cv_image", cv_image)
        cv2.imshow("output", img_out)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print('ex', e)
    


ditancia = None
def scaneou(dado):
    global distancia
    distancia = dado.ranges[0]



if __name__=="__main__":
    rospy.init_node("Q5")

    topico_imagem = "/camera/image/compressed"

    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)
    lidar = rospy.Subscriber("/scan", LaserScan, scaneou)
    print("Usando ", topico_imagem)

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

    try:
        
        girou = False
        procurado = 'car'
        while not rospy.is_shutdown():

            if girou:
                # Apenas vai reto
                vel = Twist(Vector3(0.2,0,0), Vector3(0,0,0))

            # Plano A: girar no sentido anti-horário, procurando a figura
            else :
                vel = Twist(Vector3(0,0,0), Vector3(0,0,0.2))
    
                if results is not None:
                    for result in results:
                        if result[0] == procurado:
                            
                            # Plano B: encontrou a figura, vamos centralizar nela
                            centro = cv_image.shape[1]//2, cv_image.shape[0]//2,
                            media_x = (result[2][0] + result[3][0])//2

                            erro = centro[0] - media_x
                            vel = Twist(Vector3(0,0,0), Vector3(0,0,erro/1000))

                            if abs(erro) < 25:
                                # Plano C: a figura está centralizada
                                vel = Twist(Vector3(0.2,0,0), Vector3(0,0,erro/1000))

                                if distancia < 0.3:
                                    # Plano D: gira 180 graus e vai adiante
                                    velocidade_saida.publish(Twist(Vector3(0,0,0), Vector3(0,0,0.31416)))
                                    rospy.sleep(10)
                                    vel = Twist(Vector3(0.2,0,0), Vector3(0,0,0))
                                    girou = True

            velocidade_saida.publish(vel)
            rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")


