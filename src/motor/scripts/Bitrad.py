#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
Freq = 10
max_bitBR = 11870
max_bitBL = 11640
max_bitFR = 11050
max_bitFL = 1 #not working
max_rad = 15
class BitradClass():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        self.pub_rad = rospy.Publisher('odom_rad', Twist, queue_size=1)
        rospy.Subscriber("odom_bits", Twist, self.update_current)
        #********** INIT NODE **********###
        r = rospy.Rate(Freq)
        print("Node initialized 10.0hz")
        while not rospy.is_shutdown():

            r.sleep()

    def update_current(self, msg):
        bits_l = msg.angular.x * max_rad / max_bitBL
        bits_r = msg.angular.y * max_rad / max_bitBR
        out = Twist()
        out.angular.x=bits_l
        out.angular.y=bits_r
        self.pub_rad.publish(out)

    def cleanup(self):
        #This function is called just before finishing the node
        # You can use it to clean things up before leaving
        # Example: stop the robot before finishing a node.
        self.pub_rad.publish(Twist())
        pass
############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("Bit_to_rad_node", anonymous=True)
    BitradClass()

