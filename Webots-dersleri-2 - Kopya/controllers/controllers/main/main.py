"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor,DistanceSensor

hizi=6.28
maxMesafe=1024

#sensörün mesafede nasıl algı m
min_uzaklık=1.0

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


# motorların tagını getirir 
#motorları getirir
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
    "so0","so1","so2","so3",
    "so4","so5","so6","so7"
    ]

for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(timestep)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # mesafe sensörü çıkışları
    psDegerleri=[]
    for i in range(8):
        psDegerleri.append(ps[i].getValue())
        print(" mesafe değerlerimiz",ps[i].getValue())
    
    sag_engeller=psDegerleri[0]>70.0 or psDegerleri[1]>70.0 or psDegerleri[2]>70.0
    sol_engeller=psDegerleri[5]>70.0 or psDegerleri[6]>70.0 or psDegerleri[7]>70.0
    ileri_engeller=psDegerleri[3]>70.0 or psDegerleri[4]>50.0    
    print("sağ engeller mesafe :", sag_engeller)
    print("sol engeller mesafe :", sol_engeller)
    
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
# Enter here exit cleanup code.
