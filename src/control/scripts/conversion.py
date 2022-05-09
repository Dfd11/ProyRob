#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
#This class will receive a number and an increment and it will publish the
# result of adding number + increment in a recursive way.
######JOYSTICK INDEX############
LEFT_X_AXIS = 0
LEFT_Y_AXIS = 1
LEFT_TRIGGER = 2
RIGHT_X_AXIS = 3
RIGHT_Y_AXIS = 4
RIGHT_TRIGGER = 5
NUM_X_AXIS = 6
NUM_Y_AXIS = 7

###########BUTTON INDEX
BTN_A = 0
BTN_B = 1
BTN_X = 2
BTN_Y = 3
BTN_LEFT_TRIG = 4
BTN_RIGHT_TRIG = 5
BTN_LEFT_PAUSE = 6
BTN_RIGHT_PAUSE = 7
BTN_CENTER_PAUSE = 8
BTN_LEFT_JOY = 9
BTN_RIGHT_JOY = 10

######FACTORS#######
LEFT_X_FACTOR = 4
LEFT_Y_FACTOR = 0.95
RIGHT_X_FACTOR = 1.0
RIGHT_Y_FACTOR = 1.0
class ConversionClass():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        #READS FROM A TOPIC WHICH HAS THE VALUES OF THE CONTROLLER
        rospy.Subscriber("joy", Joy, self.control_cb)
        self.pub_speed = rospy.Publisher('speed',Twist,queue_size=1)

        self.in_joy = Joy(axes=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],buttons=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        self.out_speed=Twist()
        #********** INIT NODE **********###
        r = rospy.Rate(10) #1Hz
        while not rospy.is_shutdown():
            #print(self.in_joy.axes[0])
            self.out_speed.linear.x=LEFT_Y_FACTOR * self.in_joy.axes[LEFT_Y_AXIS]
            self.out_speed.angular.z=LEFT_X_FACTOR * self.in_joy.axes[LEFT_X_AXIS]
            self.pub_speed.publish(self.out_speed)
            r.sleep()
    def control_cb(self,msg):
        self.in_joy=msg

    def cleanup(self):
        self.out_speed=Twist()
        self.pub_speed.publish(self.out_speed)
        pass
############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("conversion_node", anonymous=True)
    ConversionClass()



