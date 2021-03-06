"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor,DistanceSensor,Camera
import cv2
import numpy as np
hizi=6.28
maxMesafe=1024

#sensörün mesafede nasıl algı m
min_uzaklık=1.0

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


camera=Camera("camera")
# motorların tagını getirir 
#motorları getirir
Camera.enable(camera,timestep)
solMotorİleri=robot.getMotor("front left wheel")
sağMotorİleri=robot.getMotor("front right wheel")
sağMotorGeri=robot.getMotor("back right wheel")
solMotorGeri=robot.getMotor("back left wheel")

#motorları hareket etirir
solMotorİleri.setPosition(float("inf"))
solMotorGeri.setPosition(float("inf"))
sağMotorİleri.setPosition(float("inf"))
sağMotorGeri.setPosition(float("inf"))

ps=[]
psNames=[
    "so0","so3","so4","so7"
    ]

for i in range(4):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(timestep)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # mesafe sensörü çıkışları
    psDegerleri=[]
    for i in range(4):
        psDegerleri.append(ps[i].getValue())
        print(" mesafe değerlerimiz",ps[i].getValue())
    
    # sag_engeller=psDegerleri[0]>70.0 or psDegerleri[1]>70.0 or psDegerleri[2]>70.0
    sag_engeller=psDegerleri[0]>70.0 
    sol_engeller=psDegerleri[3]>70.0 
    # sol_engeller=psDegerleri[5]>70.0 or psDegerleri[6]>70.0 or psDegerleri[7]>70.0
    ileri_engeller=psDegerleri[1]>50.0 or psDegerleri[2]>50.0    
    print("sağ engeller mesafe :", sag_engeller)
    print("sol engeller mesafe :", sol_engeller)
    print("ileri engeller mesafe :", ileri_engeller)
    
    sol_hiz=0.5*hizi
    sag_hiz=0.5*hizi
    
    if ileri_engeller:
        sol_hiz-=0.5*hizi
        sag_hiz+=0.5*hizi
        print("önümüzde bir engel var")
    elif sol_engeller:
        sol_hiz-=0.5*hizi
        sag_hiz+=0.5*hizi
        print("sol bir engel var")
    elif sag_engeller:
        sol_hiz+=0.5*hizi
        sag_hiz-=0.5*hizi
        print("sag bir engel var")
     
     # motoların hızını belirler
    # - koyarsak araç geri geri gelir
    solMotorİleri.setVelocity(sol_hiz)
    solMotorGeri.setVelocity(sol_hiz)
    sağMotorİleri.setVelocity(sag_hiz)
    sağMotorGeri.setVelocity(sag_hiz)
    
    Camera.getImage(camera)
    Camera.saveImage(camera,"color.png",1)
    
    frame=cv2.imread("color.png")
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    # lower_blue = np.array([110,50,50])
    lower_blue = np.array([0,191,0])
    # lower_blue = np.array([91,159,255])#Sualtında ki Çember
    # upper_blue = np.array([130,255,255])
    upper_blue = np.array([15,255,255])
    # upper_blue = np.array([112,255,255])#Sualtında ki Çember
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    
    # cv2.imshow("Color",frame)
    
    cv2.waitKey(timestep)
# Enter here exit cleanup code.
