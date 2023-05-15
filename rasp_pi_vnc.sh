#!/bin/bash

# VNC Viewer 설치
sudo apt-get update
sudo apt-get install realvnc-vnc-viewer

# VNC 사용 설정 변경
sudo raspi-config nonint do_vnc 0

# VNC Viewer 실행
READ_IP="라즈베리파이의 IP 주소를 입력하세요 : "
read -p $READ_IP RASP_IP_ADDRESS
READ_PW="VNC Viewer 비밀번호(8자리 이상)를 입력하세요 : "
read -sp $READ_PW VNC_PASSWORD
sleep 1
echo "VNC Viewer를 실행합니다."
vncviewer $RASP_IP_ADDRESS -passwd <(echo $VNC_PASSWORD)
