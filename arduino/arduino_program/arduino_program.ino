//ROS LIBRARIES
#include <ros.h>
#include <geometry_msgs/Twist.h>
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROBOCLAW LIBRARIES
#include <SoftwareSerial.h>
#include "RoboClaw.h"
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROBOCLAW INTI
SoftwareSerial serial(10,11);
RoboClaw roboclaw(&serial,10000);
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROBOCLAW DEFINES
#define address 0x80
#define address2 0x81
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROS NODEHANDLER
ros::NodeHandle  nh;
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROS VARIABLES
volatile float  wl, wr, odoml,odomr;
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROS CALLBACKS
    //READ "motor/speed_bits"
void motor_speed_cb( const geometry_msgs::Twist& msg){
    wl=msg.angular.x;
    wr=msg.angular.y;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROS SUBSCRIBERS
ros::Subscriber<geometry_msgs::Twist> motor_speed_sub("/motor/speed_bits", motor_speed_cb );
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROS PUBLISHER
geometry_msgs::Twist odom_msg;
ros::Publisher odom_pub("/motor/odom_bits", &odom_msg);

///////////////////////////////////////////////////////////////////////////////////////////////////////////////
//ROBOCLAW FUNCTIONS
void read_roboclaw(){
}

void write_left_motor(float x){
    if (x>=0){
      roboclaw.BackwardM2(address2,int(x));
      roboclaw.BackwardM2(address,int(x));    
    }else{
      roboclaw.ForwardM2(address2,int(abs(x)));
      roboclaw.ForwardM2(address,int(abs(x)));   
    }
}
void write_right_motor(float y){
    if (y>=0){
      roboclaw.BackwardM1(address2,int(y));
      roboclaw.BackwardM1(address,int(y));    
    }else{
      roboclaw.ForwardM1(address2,int(abs(y)));
      roboclaw.ForwardM1(address,int(abs(y)));   
    }
}
void write_roboclaw(float wl, float wr){
  write_left_motor(wl);
  write_right_motor(wr);
}
void readSpeed(void)
{
  uint8_t status1,status2,status3,status4;
  bool valid1,valid2,valid3,valid4;
  int32_t motorBR = roboclaw.ReadSpeedM1(address, &status1, &valid1);
  int32_t motorBL = roboclaw.ReadSpeedM2(address, &status2, &valid2);
  int32_t motorFR = roboclaw.ReadSpeedM1(address2, &status3, &valid3);
  int32_t motorFL = roboclaw.ReadSpeedM2(address2, &status4, &valid4);

  odoml = float(motorBL);
  odomr = -float(motorBR);
  
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
void setup() {
   //ROS NODE INIT
   nh.initNode();
   nh.advertise(odom_pub);
   nh.subscribe(motor_speed_sub);
   //ROBOCLAW INIT
   Serial.begin(57600);
   roboclaw.begin(38400);

}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
void loop() {
  if (!(millis() % 100)) {        
  /* 
  *  Enter here every 100 ms
  *  Add your code here 
  *  str_pub.publish(&str_msg); //Example publish data
  */
    readSpeed();
    odom_msg.angular.x=odoml;
    odom_msg.angular.y=odomr;
    odom_pub.publish( &odom_msg );
    write_roboclaw(wl,wr);     
  }
  
  nh.spinOnce();
}
