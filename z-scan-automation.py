import pyvisa
from ThorlabsPM100 import ThorlabsPM100
from kamal_motion import Units
from kamal_motion.ascii import Connection
import time
import matplotlib.pyplot as plt
import pandas as pd
# import searborn as sns

material_name ='kamal_ZnO-rGO_ 0'
sample= '90 mW'
light = '650 nm green laser'
aperture = 'linear transmission'

#RANGE : the range of the motion in mm
RANGE =  120
#SLEEP_TIME : Sleep time after executing each cycle 
SLEEP_TIME = 0.5
#Power_Data_Per_position: How many data instance for each position
Power_Data_Per_position = 9
#STEP_COUNT: Position Increment in mm
STEP_COUNT = 1
#for start position
START_POSITION=20
 

power_meter_readings= []
position = []


#setting power meter to the home position
with Connection.open_serial_port("COM3") as connection:
    connection.enable_alerts()
    device_list = connection.detect_devices()
    device = device_list[0]
    axis = device.get_axis(1)
    #axis.home()
    #time.sleep(1)
    axis.move_absolute(START_POSITION,Units.LENGTH_MILLIMETRES)
    print("Move to start position:",   START_POSITION ," mm")


  

rm = pyvisa.ResourceManager()

cols = {"data"+ str(a) : [] for a in range(Power_Data_Per_position)}

for pos in range(START_POSITION,int(RANGE)):   
    with Connection.open_serial_port("COM3") as connection:
        for i in range (Power_Data_Per_position):            
            inst = rm.open_resource('USB0::0x1313::0x8072::P2008614::INSTR', timeout=1)
            power_meter = ThorlabsPM100(inst=inst)
            print("Position: ", pos ,"mm",  "Instance:", i, power_meter.read*1000.000, "mW")
            cols["data"+str(i)].append(power_meter.read*1000.000)
            
            # power_meter_readings.append(power_meter.read)
        
        position.append(pos)          
        connection.enable_alerts()
        device_list = connection.detect_devices()
        device = device_list[0]
        axis = device.get_axis(1)        
        axis.move_relative(STEP_COUNT, Units.LENGTH_MILLIMETRES)
        time.sleep(SLEEP_TIME)
        pos+=STEP_COUNT
        
        # print("Position : ", pos, "mm; Power_meter reading: ", power_meter.read,"Watt")
        
# data_dict = {'Position': position, 'Power': power_meter_readings}
# df= pd.DataFrame(data_dict)

position_dict = {'Position': position}
df1 = pd.DataFrame(position_dict)
df2 = pd.DataFrame(cols)
df = pd.concat([df1, df2], axis =1)
df.to_csv(material_name+'_'+sample+'_'+light+'_'+aperture+"aperture"+".csv", index = False)

# sns.lineplot(
#     data=df,
#     x="Position", y="sPower", hue="event", style="event",
#     markers=True, dashes=False
# )

plt.plot(df.Position, df.data0)
plt.xlabel('Position (mm)')
plt.ylabel('Power meter reaeding (mWatt)')
plt.title('Power vs Position relationship of Laser')
plt.show()
        




        
        
    
    
    
    
