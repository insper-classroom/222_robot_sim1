#! /usr/bin/env python3
# -*- coding:utf-8 -*-

# Rodar com 
# roslaunch my_simulation ???.launch


from __future__ import print_function, division
import rospy
import numpy as np
import math
import cv2
import time
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Vector3, Pose

from nav_msgs.msg import Odometry

frente = None
direita = None


def scaneou(msg):
    global frente
    global direita
    frente = min(min(msg.ranges[:5]),min(msg.ranges[355:]))
    direita = min(msg.ranges[260:280])

    print(f"Frente: {frente}")
    print(f"Direita: {direita}")


if __name__=="__main__":
    print("Iniciando o node...")
    rospy.init_node("Q3")

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    laser_sub = rospy.Subscriber("/scan", LaserScan, scaneou)
    
    try:
        
        # Primeiro passo: aproximar-se da frente
        while frente is None or frente > 0.3:
            vel = Twist(Vector3(0.15,0,0), Vector3(0,0,0))
            velocidade_saida.publish(vel)
            rospy.sleep(0.05)

        # Segundo passo: girar à esquerda
        while frente < 0.5:
            vel = Twist(Vector3(0.0,0,0), Vector3(0,0,0.15))
            velocidade_saida.publish(vel)
            rospy.sleep(0.05)

        # Terceiro passo: percorrer a parede da direita
        while not rospy.is_shutdown():
            vel = Twist(Vector3(0.1,0,0), Vector3(0,0,0))

            # Se a direita estiver muito longe, girar no sentido horário, 
            # enquanto vai para frente
            if direita > 0.7:
                # Aqui estamos "roubando" e usando o rospy.sleep()
                # O robô anda "cego" durante esse tempo, não é algo recomendado, mas pode ser usado na prova se não houver outra forma
                vel = Twist(Vector3(0,0,0), Vector3(0,0,-0.1))
                velocidade_saida.publish(vel)
                rospy.sleep(3.1416/4/0.1)

            elif frente < 0.3:
                vel = Twist(Vector3(0,0,0), Vector3(0,0,0.2))

            elif direita > 0.4:
                vel.angular.z = -0.06
            elif direita < 0.3:
                vel.angular.z = 0.06
            # Se a frente estiver ocupada, girar no sentido antihorário até desocupar
            
                
            # -- Loop de controle do robô -- #

            velocidade_saida.publish(vel)
            rospy.sleep(0.05)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")

