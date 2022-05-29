#!/usr/bin/env python 
import rospy 
import numpy as np
from sensor_msgs.msg import LaserScan  
from geometry_msgs.msg import Twist
# This class implements a simple obstacle avoidance algorithm
class AvoidObstacleClass(): 
    def __init__(self): 
        rospy.on_shutdown(self.cleanup) 

        ####################### PUBLISEHRS AND SUBSCRIBERS ############################ 
        rospy.Subscriber("base_scan", LaserScan, self.laser_cb) 
        self.cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        
        ######################## CONSTANTS AND VARIABLES ############################## 

        v_desired = 2.0 #2.65 # m/s
        kw = 0.65 #Angular velocity gain
        
        self.closest_angle = 0.0 #Angle to the closest object
        self.closest_range = np.inf #Distance to the closest object
        vel_msg = Twist()
        r = rospy.Rate(10) #10Hz is the lidar's frequency 
        print("Node initialized 1hz")
        ############################### MAIN LOOP #####################################
        while not rospy.is_shutdown(): 
            range=self.closest_range
            theta_closest=self.closest_angle
            #limit the angle to -pi pi
            if np.isinf(range):
                vel_msg.linear.x = v_desired
                vel_msg.angular.z = 0
                print("Inf")
            else:
                if (theta_closest <= (np.pi)/2 or theta_closest >= -(np.pi)/2) and (range >= 0.4 and range <= 2):
                    theta_AO = theta_closest - np.pi
                    theta_AO = np.arctan2(np.sin(theta_AO), np.cos(theta_AO))
                    vel_msg.linear.x = v_desired
                    vel_msg.angular.z = kw * theta_AO
                    print("Avoid")
                elif (theta_closest > (np.pi)/2 or theta_closest < -(np.pi)/2) and (range > 2):
                    vel_msg.linear.x = v_desired
                    vel_msg.angular.z = 0
                    print("No obstacle")
                elif(range < 0.4):
                    vel_msg.linear.x = 0
                    vel_msg.angular.z = 0
                    print("No movement")
                else:
                    vel_msg.linear.x = v_desired
                    vel_msg.angular.z = 0
                    print("No obstacle")

            print("closest object distance: " + str(self.closest_range))
            print("theta_closest: " + str(theta_closest))
            self.cmd_vel_pub.publish(vel_msg)
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

        
    def cleanup(self): 
        #This function is called just before finishing the node 
        # You can use it to clean things up before leaving 
        # Example: stop the robot before finishing a node.   
        vel_msg = Twist()
        self.cmd_vel_pub.publish(vel_msg) 
############################### MAIN PROGRAM #################################### 
if __name__ == "__main__": 
    rospy.init_node("avoid_obstacle", anonymous=True) 
    AvoidObstacleClass()