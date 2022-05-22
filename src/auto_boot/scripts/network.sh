#!/bin/bash
#RESPUESTA=0
#ITERATION=0
#while [[ $RESPUESTA != 1 ]] && [[ $ITERATION -lt 2 ]]
#do
#  ping -c 1 ubuntu #&> /dev/null
#  if [[ $? -eq 0 ]]; then
#    RESPUESTA=1
#  else
#    RESPUESTA=0
#  fi
#  sleep 3
#  ITERATION=$((ITERATION+1))
#  echo "$ITERATION Trying to connect..."
#done
#if [ $RESPUESTA == 1 ]; then
#  echo "*******************************************"
#  echo "       CONNECTED to net Ready to work"
#  echo "*******************************************"
#  echo ""
#  sleep 5
#  export ROS_MASTER_URI=http://ubuntu:11311/
#  export ROS_HOSTNAME=ubuntu
#  export ROS_IP=ubuntu
#  echo "192.168.0.106 jrtaf" >>> /etc/hosts
#  echo "192.168.0.109 ubuntu" >>> /etc/hosts
#  echo $ROS_MASTER_URI
#  echo "PLEASE"
#  echo $ROS_HOSTNAME
#  echo "WORK"
#  echo $ROS_IP

#else
#  echo "*******************************************"
#  echo "       CONNECTED to loc Ready to work"
#  echo "*******************************************"
#  export ROS_MASTER_URI=http://localhost:11311    #Use this when you are running the  roscore in your local pc.
#  export ROS_HOSTNAME=localhost    #Use this when you are running the  roscore in your local pc.
#  export ROS_IP=localhost    #Use this when you are running the  roscore in your local pc.
#  echo $ROS_MASTER_URI
#  echo "PLEASE"
#  echo $ROS_HOSTNAME
#  echo "WORK"
#  echo $ROS_IP
#fi
#while [[ $RESPUESTA != 0 ]] #&& $ITERATION -lt 180 ]]
#do
#  ping -c 1 192.168.0.106 &> /dev/null
#  if [[ $? -ne 0 ]]; then
#    RESPUESTA=1
#  else
#    RESPUESTA=0
#  fi
#  sleep 3
#  ITERATION=$((ITERATION+1))
#  echo "$ITERATION Trying to connect..."
#done

echo "*******************************************"
echo "       CONNECTED. Ready to work"
echo "*******************************************"
echo ""
#source ~/.bashrc
#source ~/ProyRob/devel/setup.bash
#sleep 5
#echo $ROS_MASTER_URI
#echo "PLEASE"
#echo $ROS_HOSTNAME
#echo "WORK"
#echo $ROS_IP
#roslaunch proyrob proyrob.launch
sudo systemctl stop proyrob_job.service
echo "*********** Starting system... ************"
sudo systemctl start proyrob_job.service
sleep 2
echo "************* I'm working :) **************"
sleep 15

#echo "PRESS ANY KEY TO CONTINUE"
while [ true ]; do
  read -t 3 -n 1
  if [ $? -eq 0 ]; then
    #source /home/ubuntu/ProyRob/src/auto_boot/scripts/start.sh
    #sudo systemctl stop proyrob_job.service
    echo ""
    #sudo systemctl start proyrob_job.service
    #sleep 2
    #echo "I'm working :)"
  fi
done
