#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
Freq = 10
mid_err = 1
LIN=1.2
ANG=0.36

class Baulbot():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        self.pub = rospy.Publisher('speed_baul', Twist, queue_size=1)
        rospy.Subscriber("scan", LaserScan, self.laser_cb)
        rospy.Subscriber("wifi_raw", Twist, self.update_wifi)

        #ROS
        r = rospy.Rate(Freq)
        self.out = Twist()
        vel_lin=0
        vel_ang=0
        LIDARS=0
        WIFISLR=0
        WIFISFB=0
        #WIFI
        mod1=0
        mod2=0
        mod3=0

        #AVOID OBSTACLE
        kw = 0.65 #Angular velocity gain
        max_obstacle_avoidance_range = 2
        min_obstacle_range = 0.4
        self.closest_angle = 0.0 #Angle to the closest object
        self.closest_range = np.inf #Distance to the closest object



        while not rospy.is_shutdown():
            #WIFI---------------------------------------------------
            if (mod2 - mid_err <= mod3 and mod2 + mid_err >= mod3):
                #IN MIDDLE
                vel_ang = 0
                WIFISLR=0
            elif (mod3 < mod2-mid_err):
                #LEFT
                vel_ang = ANG
                WIFISLR=1
            elif (mod3 > mod2+mid_err):
                #RIGHT
                vel_ang = -ANG
                WIFISLR=-1

            if ((mod2+mod3)/2 < mod1):
                #FRONT
                vel_lin = LIN
                WIFISFB=0
            elif ((mod2+mod3)/2 > mod1):
                #BACK
                vel_lin = 0
                WIFISFB=1
            else:
                #??? WTF
                pass
            #-----------------------------------------------------
            #AVOID OBSTACLE---------------------------------------
#            range=self.closest_range
#            theta_closest=self.closest_angle
            #limit the angle to -pi pi
#            if np.isinf(range) or range > max_obstacle_avoidance_range or abs(theta_closest) > np.pi/2:
                #NO DETECTION
                #vel_msg.linear.x = v_desired
                #vel_msg.angular.z = 0
                #print("INF", np.isinf(range))
                #print("MAX", range > max_obstacle_avoidance_range )
                #print("OUT", abs(theta_closest) > np.pi/2)
#            elif (range > min_obstacle_range and range <= max_obstacle_avoidance_range):
                #DETECTION WITHIN AVOID
                #theta_AO = theta_closest - np.pi
                #theta_AO = np.arctan2(np.sin(theta_AO), np.cos(theta_AO))
                #vel_msg.linear.x = v_desired
                #vel_msg.angular.z = kw * theta_AO
                #print("OK")
#            elif (range < min_obstacle_range):
                #DETECTION EMERGENCY STOP
                #vel_msg.linear.x = 0
                #vel_msg.angular.z = 0
                #print("STOP")
            self.out.linear.x = vel_lin
            self.out.angular.z = vel_ang
            self.pub.publish(self.out)
            r.sleep()

    def laser_cb(self, msg):
        ## This function receives a message of type LaserScan and computes the closest object direction and range
        closest_range = min(msg.ranges)
        idx = msg.ranges.index(closest_range)
        closest_angle = msg.angle_min + idx * msg.angle_increment
        # Limit the angle to [-pi,pi]
        closest_angle = np.arctan2(np.sin(closest_angle),np.cos(closest_angle))
        self.closest_range = closest_range
        self.closest_angle = closest_angle

    def update_wifi (self,msg):
        mod1 = msg.linear.x
        mod2 = msg.linear.y
        mod3 = msg.linear.z

    def cleanup(self):
        #This function is called just before finishing the node
        # You can use it to clean things up before leaving
        # Example: stop the robot before finishing a node.
        self.pub.publish(Twist())
        pass
