#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


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
class MuxClass():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        rospy.Subscriber("in_A", Twist, self.A_cb)
        rospy.Subscriber("in_B", Twist, self.B_cb)
        rospy.Subscriber("in_Sel", Joy, self.sel_cb)
        self.pub_out = rospy.Publisher('out',Twist,queue_size=1)

        self.A=Twist()
        self.B=Twist()
        self.sel=0
        self.out=Twist()
        #********** INIT NODE **********###
        r = rospy.Rate(10) #1Hz
        while not rospy.is_shutdown():
            if (self.sel == 0):
                self.out=self.A
            else:
                self.out=self.B

            self.pub_out.publish(self.out)

            r.sleep()
    def A_cb(self,msg):
        self.A=msg

    def B_cb(self,msg):
        self.B=msg

    def sel_cb(self,msg):
        if (msg.buttons[BTN_A]):
            self.sel=1-self.sel

            if (self.sel == 0):
                self.out=self.A
            else:
                self.out=self.B

            self.pub_out.publish(self.out)
    def cleanup(self):
        self.pub_out.publish(Twist())
        pass
############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("mux_node", anonymous=True)
    MuxClass()



