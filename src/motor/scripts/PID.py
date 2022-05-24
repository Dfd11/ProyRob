#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
const_L=0.422148
const_R=0.061595
#kp=1
#ki=0.0
#kd=0.0
Freq=10
#elapsed_time = 1.0/Freq
MAX_ANG_VEL = 15
class PIDClass():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        self.pub_wvel = rospy.Publisher('speed_rad', Twist, queue_size=1)
        rospy.Subscriber("speed", Twist, self.update_setpoint)
#        rospy.Subscriber("odom_rad", Twist, self.update_current)
        #********** INIT NODE **********###
#        self.prev_error_l = 0.0
#        self.prev_error_r = 0.0
        self.setpoint_wl = 0.0
        self.setpoint_wr = 0.0
#        self.current_wl = 0.0
#        self.current_wr = 0.0
#        self.error_l = 0.0
#        self.error_r = 0.0
#        self.cum_error_l = 0.0
#        self.cum_error_r = 0.0
#        self.rate_error_l = 0.0
#        self.rate_error_r = 0.0
#        self.out_l = 0.0
#        self.out_r = 0.0
        self.out = Twist()
        r = rospy.Rate(Freq)
        print("Node initialized 10.0hz")
        while not rospy.is_shutdown():
#            self.prev_error_l=self.error_l
#            self.prev_error_r=self.error_r

#            self.error_l = self.setpoint_wl - self.current_wl
#            self.error_r = self.setpoint_wr - self.current_wr

#            self.cum_error_l = self.cum_error_l + self.error_l * elapsed_time
#            self.cum_error_r = self.cum_error_r + self.error_r * elapsed_time

#            self.rate_error_l = (self.error_l - self.prev_error_l) / elapsed_time
#            self.rate_error_r = (self.error_r - self.prev_error_r) / elapsed_time

#            self.out_l = kp * self.error_l + ki * self.cum_error_l + kd * self.rate_error_l
#            self.out_r = kp * self.error_r + ki * self.cum_error_r + kd * self.rate_error_r

            #self.out.angular.x=self.out_l
            #self.out.angular.y=self.out_r
            self.out.angular.x=self.setpoint_wl
            self.out.angular.y=self.setpoint_wr
            print("hello")
            self.pub_wvel.publish(self.out)

            r.sleep()

    def update_setpoint(self, msg):
        self.setpoint_wl=(2*msg.linear.x - msg.angular.z*const_L)/(2*const_R)
        self.setpoint_wr=(2*msg.linear.x + msg.angular.z*const_L)/(2*const_R)
        if (self.setpoint_wl > MAX_ANG_VEL):
            self.setpoint_wl = MAX_ANG_VEL

        if (self.setpoint_wr > MAX_ANG_VEL):
            self.setpoint_wr = MAX_ANG_VEL

        if (self.setpoint_wl < -MAX_ANG_VEL):
            self.setpoint_wl = -MAX_ANG_VEL

        if (self.setpoint_wr < -MAX_ANG_VEL):
            self.setpoint_wr = -MAX_ANG_VEL
#    def update_current(self, msg):
#        self.current_wl = msg.angular.x
#        self.current_wr = msg.angular.y

    def cleanup(self):
        #This function is called just before finishing the node
        # You can use it to clean things up before leaving
        # Example: stop the robot before finishing a node.
        self.pub_wvel.publish(Twist())
        pass
############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("PID_node", anonymous=True)
    PIDClass()

