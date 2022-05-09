#!/bin/bash
RESPUESTA=1
ITERATION=0
while [[ $RESPUESTA != 0 ]] #&& $ITERATION -lt 180 ]]
do
  ping -c 1 192.168.0.106 &> /dev/null
  if [[ $? -ne 0 ]]; then
    RESPUESTA=1
  else
    RESPUESTA=0
  fi
  sleep 3
  ITERATION=$((ITERATION+1))
  echo "$ITERATION Trying to connect..."
done

if [ $RESPUESTA == 0 ]; then
  echo "*******************************************"
  echo "       CONNECTED. Ready to work"
  echo "*******************************************"
  echo ""
  sudo systemctl stop proyrob_job.service
  echo "*********** Starting system... ************"
  sudo systemctl start proyrob_job.service
  sleep 2
  echo "************* I'm working :) **************"
  sleep 3
else
  echo "*******************************************"
  echo "UNABLE TO CONNECT to ----> Ros_robot"
  echo "*******************************************"
  echo ""
fi

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
