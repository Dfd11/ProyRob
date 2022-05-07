#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
Freq = 10
max_bit = 127.0
max_rad = 15
class RadbitClass():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        self.pub_bit = rospy.Publisher('speed_bits', Twist, queue_size=1)
        rospy.Subscriber("speed_rad", Twist, self.update_current)
        #********** INIT NODE **********###
        r = rospy.Rate(Freq)
        print("Node initialized 10.0hz")
        while not rospy.is_shutdown():

            r.sleep()

    def update_current(self, msg):
        bits_l = int(msg.angular.x * max_bit / max_rad)
        bits_r = int(msg.angular.y * max_bit / max_rad)
        out = Twist()
        out.angular.x=bits_l
        out.angular.y=bits_r
        self.pub_bit.publish(out)

    def cleanup(self):
        #This function is called just before finishing the node
        # You can use it to clean things up before leaving
        # Example: stop the robot before finishing a node.
        self.pub_bit.publish(Twist())
        pass
############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("Rad_to_bit_node", anonymous=True)
    RadbitClass()

