#!/usr/bin/env python
from operator import index
import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

#This node receives a LaserScan msg and computes the angle to the closest object
class LidarClass():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        ###******* INIT PUBLISHERS *******###
        ##  pub = rospy.Publisher('setPoint', UInt16MultiArray, queue_size=1)
        self.pub_cmdvel = rospy.Publisher('speed_F', Twist, queue_size=1)

        ############################### SUBSCRIBERS #####################################
        rospy.Subscriber("/vision/scan", LaserScan, self.laser_cb)

        ############ CONSTANTS ################
        self.my_scan = LaserScan()
        self.my_vel = Twist()
        #self.my_cmd = "None"

        #********** INIT NODE **********###
        r = rospy.Rate(20) # Para velocidad tomar en cuenta entre 10 - 40 Hz
        print("Node initialized 1hz")
        while not rospy.is_shutdown():
            print("I'm working")
            r.sleep()

    def laser_cb(self,msg):
        #This function receives a Laser Scan and computes the angle to the closest object.
        closest_range = min(msg.ranges)
        index = msg.ranges.index(closest_range)
        closest_angle = msg.angle_min + index*msg.angle_increment
        print("Closest Angle: "+ str(closest_angle) + ". Located at position: "+str(index) + ", whith a closest range of: "+str(closest_range))
        print("\n")
        print("Current velocity: LINEAR => "+ str(self.my_vel.linear.x)+ " ANGULAR=> "+ str(self.my_vel.angular.z))
        if not np.isfinite(closest_range):
            self.my_vel.linear.x = 0
            self.my_vel.angular.z = 0
            #self.pub_cmdvel.publish(self.my_vel)
        elif closest_range <= 2.0:
            if closest_range >= 0.60:
                angleMin = -0.07*closest_angle
                angleMax = 0.07*closest_angle
                if closest_angle <= angleMax or closest_angle >= angleMin:
                    Kw = 2.65
                    Kv = .65
                    self.my_vel.linear.x = Kv * closest_range
                    self.my_vel.angular.z = Kw * closest_angle
                else:
                    self.my_vel.linear.x = 0
                    self.my_vel.angular.z = 0
                #self.pub_cmdvel.publish(self.my_vel)
            else:
                self.my_vel.linear.x = 0
                self.my_vel.angular.z = 0
            #self.pub_cmdvel.publish(self.my_vel)
	else:
	    self.my_vel.linear.x = 0
            self.my_vel.angular.z =0

        self.pub_cmdvel.publish(self.my_vel)

    def cleanup(self):
        #This function is called just before finishing the node
        # You can use it to clean things up before leaving
        # Example: stop the robot before finishing a node.
        print("Stopping the robot")
        stop_twist = Twist()
        self.pub_cmdvel.publish(stop_twist)

if __name__ == "__main__":
    rospy.init_node("closest_detector_node", anonymous=True)
    LidarClass()
