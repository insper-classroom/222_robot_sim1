#! /usr/bin/env python3
# -*- coding:utf-8 -*-

# Rodar com 
# roslaunch my_simulation ???.launch


from __future__ import print_function, division
import auxiliar
import rospy
import numpy as np
import math
import cv2
import time
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Vector3, Pose

from nav_msgs.msg import Odometry



if __name__=="__main__":
    rospy.init_node("Q3")

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    
    try:
        vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
        
        while not rospy.is_shutdown():
            
            # -- Loop de controle do robô -- #

            velocidade_saida.publish(vel)
            rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")

