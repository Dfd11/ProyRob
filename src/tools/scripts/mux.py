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
        rospy.Subscriber("in_C", Twist, self.C_cb)
        rospy.Subscriber("in_D", Twist, self.D_cb)
        #ADD MORE LINES FOR MORE OPTIONS
        rospy.Subscriber("in_Sel", Joy, self.sel_cb)
        self.pub_out = rospy.Publisher('out',Twist,queue_size=1)

        self.A=Twist()
        self.B=Twist()
        self.C=Twist()
        self.D=Twist()
        #ADD MORE LINES FOR MORE OPTIONS
        self.selA=0
        self.selB=0
        self.selC=0
        self.selD=0
        #ADD MORE LINES FOR MORE OPTIONS
        self.out=Twist()
        #********** INIT NODE **********###
        r = rospy.Rate(10) #1Hz
        while not rospy.is_shutdown():
            if (self.selB == 1):
                self.out=self.B
            elif(self.selC == 1):
                self.out=self.C
            elif(self.selD == 1):
                self.out=self.D
            else:
                self.out=self.A

            self.pub_out.publish(self.out)

            r.sleep()
    def A_cb(self,msg):
        self.A=msg

    def B_cb(self,msg):
        self.B=msg

    def C_cb(self,msg):
        self.C=msg

    def D_cb(self,msg):
        self.D=msg
#    def X_cb(self,msg):
#        self.X=msg
     #ADD MORE LINES FOR MORE OPTIONS

    def sel_cb(self,msg):
        if (msg.buttons[BTN_A]):
            self.selB = 1 - self.selB
            self.selC = 0
            self.selD = 0
            #ADD MORE LINES FOR MORE OPTIONS
        elif (msg.buttons[BTN_B]):
            self.selB = 0
            self.selC = 1 - self.selC
            self.selD = 0
            #ADD MORE LINES FOR MORE OPTIONS
        elif (msg.buttons[BTN_X]):
            self.selB = 0
            self.selC = 0
            self.selD = 1 - self.selD
        else :
            self.selB = 0
            self.selC = 0
            self.selD = 0
            #ADD MORE LINES FOR MORE OPTIONS

    def cleanup(self):
        self.pub_out.publish(Twist())
        pass
############################### MAIN PROGRAM ####################################
if __name__ == "__main__":
    rospy.init_node("mux_node", anonymous=True)
    MuxClass()



