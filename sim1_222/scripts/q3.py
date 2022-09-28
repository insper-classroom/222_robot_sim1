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

inicio = True
estado = "VAI FRENTE"

frente = None
direita = None
leituras = None

def scaneou(dado):
    global frente
    global direita
    global leituras
    #print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    #print("Leituras:")
    #print(np.array(dado.ranges).round(decimals=2))
    #print("Intensities")
    #print(np.array(dado.intensities).round(decimals=2))
    frente1 = min(dado.ranges[0:15])
    frente2 = min(dado.ranges[-15:])
    frente = min(frente1, frente2)
    direita = min(dado.ranges[250:290])
    leituras = dado.ranges


if __name__=="__main__":
    print("Iniciando o node...")
    rospy.init_node("Q3")


    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
    
    try:
        vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
        
        while not rospy.is_shutdown():
#           print(estado)
            
            # -- Loop de controle do robô -- #

            # 1 - Fazer o robo encontrar a parede da frente e seguir
            if estado == "VAI FRENTE":
                vel = Twist(Vector3(0.1,0,0), Vector3(0,0,0))

                # Somente se já passou do início do programa, o robô deve serguir a parede direita
                if not inicio and direita > 0.25:
                    vel = Twist(Vector3(0.1,0,0), Vector3(0,0,-0.2))
                if not inicio and direita < 0.25:
                    vel = Twist(Vector3(0.1,0,0), Vector3(0,0,0.2))
                    
            # 2 - Se sumir a parede direita, o robô deve dar uma guinada até encontrar a parede
            if estado == "VAI FRENTE" and not inicio and direita is not None and direita > 0.7:
                vel = Twist(Vector3(0.0,0,0), Vector3(0,0,-0.2))
                estado = "GIRA DIR"
            
            # 3 - Se encontrar uma parede à frente, deve girar à esquerda até ficar paralelo 
            elif estado == "VAI FRENTE" and frente is not None and frente < 0.25:
                vel = Twist(Vector3(0,0,0), Vector3(0,0,0.1))
                estado = "GIRA ESQ"

            # 4 - Se está girando à direita e encontra uma parede à direita, continua girando rápido até sumir de novo a parede
            elif estado == "GIRA DIR" and direita < 1.0:
                vel = Twist(Vector3(0.05,0,0), Vector3(0,0,-0.2))
                estado = "VAI FRENTE"

            # 5 - Se está girando à esquerda e fica paraleleo à parede da direita, que deve estar próxima, começa a seguir
            elif estado == "GIRA ESQ" and 17 < np.argmin(leituras[250:290]) < 23 and direita < 0.4:
                vel = Twist(Vector3(0.05,0,0), Vector3(0,0,0))
                estado = "VAI FRENTE"
                inicio = False

            velocidade_saida.publish(vel)
            # Intervalo bem pequeno entre um loop e outro para não perder situações importantes
            rospy.sleep(0.02)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")

