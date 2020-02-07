#Mazda 6 2006 CAN data processor
#(c) Sergey Staroletov
#
import pandas as pd
import numpy as np
import sys

dataset = "long"
dirr = "/Volumes/SD128/CAN_DATA_ARTICLE/" + dataset + "/"

#speed
byte1_speed = pd.read_csv(dirr + "CAN1_201_4.csv") #201 id 4th byte
byte2_speed = pd.read_csv(dirr + "CAN1_201_5.csv")

#rpm
byte1_rpm = pd.read_csv(dirr + "CAN1_201_0.csv")
byte2_rpm = pd.read_csv(dirr + "CAN1_201_1.csv")

#left front wheel speed
byte1_speed_lf = pd.read_csv(dirr + "CAN1_4b0_0.csv")
byte2_speed_lf = pd.read_csv(dirr + "CAN1_4b0_1.csv")

#right front wheel speed
byte1_speed_rf = pd.read_csv(dirr + "CAN1_4b0_2.csv")
byte2_speed_rf = pd.read_csv(dirr + "CAN1_4b0_3.csv")

#left rear wheel speed
byte1_speed_lr = pd.read_csv(dirr + "CAN1_4b0_4.csv")
byte2_speed_lr = pd.read_csv(dirr + "CAN1_4b0_5.csv")

#right rear wheel speed
byte1_speed_rr = pd.read_csv(dirr + "CAN1_4b0_6.csv")
byte2_speed_rr = pd.read_csv(dirr + "CAN1_4b0_7.csv")

#gear
byte_gear = pd.read_csv(dirr + "CAN1_231_0.csv")

#accel
byte_acc = pd.read_csv(dirr + "CAN1_201_6.csv")

#engine temp
byte_temp = pd.read_csv(dirr + "CAN1_420_0.csv")


#fuel
#byte1_fuel = pd.read_csv(dirr + "CAN1_400_2.csv")
#byte2_fuel = pd.read_csv(dirr + "CAN1_400_3.csv")


#get data series
timez = np.array(byte1_speed[byte1_speed.keys()[0]])

byte1_speed = np.array(byte1_speed[byte1_speed.keys()[1]])
byte2_speed = np.array(byte2_speed[byte2_speed.keys()[1]])

byte1_rpm = np.array(byte1_rpm[byte1_rpm.keys()[1]])
byte2_rpm = np.array(byte2_rpm[byte2_rpm.keys()[1]])

byte1_speed_lf = np.array(byte1_speed_lf[byte1_speed_lf.keys()[1]])
byte2_speed_lf = np.array(byte2_speed_lf[byte2_speed_lf.keys()[1]])

byte1_speed_rf = np.array(byte1_speed_rf[byte1_speed_rf.keys()[1]])
byte2_speed_rf = np.array(byte2_speed_rf[byte2_speed_rf.keys()[1]])

byte1_speed_lr = np.array(byte1_speed_lr[byte1_speed_lr.keys()[1]])
byte2_speed_lr = np.array(byte2_speed_lr[byte2_speed_lr.keys()[1]])

byte1_speed_rr = np.array(byte1_speed_rr[byte1_speed_rr.keys()[1]])
byte2_speed_rr = np.array(byte2_speed_rr[byte2_speed_rr.keys()[1]])

byte_gear = np.array(byte_gear[byte_gear.keys()[1]])

byte_acc = np.array(byte_acc[byte_acc.keys()[1]])

byte_temp = np.array(byte_temp[byte_temp.keys()[1]])


#byte1_fuel = np.array(byte1_fuel[byte1_fuel.keys()[1]])
#byte2_fuel = np.array(byte2_fuel[byte2_fuel.keys()[1]])


orig_stdout = sys.stdout
f = open("/Volumes/SD128/CAN_DATA_ARTICLE/" + dataset + ".csv", 'w')
sys.stdout = f


#first line
print("timestamp,vehicle_speed,lf_wheel_s,rf_wheel_s,lr_wheel_s,rr_wheel_s,vehicle_rpm,gear,accel_pedal,engine_temp")

i_from = 0
i_to = len(byte1_speed)

#because of different number of data lines
K2 = len(byte1_speed) / len (byte1_speed_lf)
K3 = len(byte1_speed) / len (byte1_speed_rf)
K4 = len(byte1_speed) / len (byte1_speed_lr)
K5 = len(byte1_speed) / len (byte1_speed_rr)
K6 = len(byte1_speed) / len (byte1_rpm)
K7 = len(byte1_speed) / len (byte_gear)

K8 = len(byte1_speed) / len (byte_acc)

#K8 = len(byte1_speed) / len (byte1_fuel)

K9 = len(byte1_speed) / len (byte_temp)


#Scale = (X-10000)/100 km/h,
for i in range(i_from, i_to):
    try:
        long_speed = (((byte1_speed[i] * 256) + byte2_speed[i]) - 10000) // 100
        long_speed_lf = (((byte1_speed_lf[int(i // K2)] * 256) + byte2_speed_lf[int(i // K2)]) - 10000) // 100
        long_speed_rf = (((byte1_speed_rf[int(i // K3)] * 256) + byte2_speed_rf[int(i // K3)]) - 10000) // 100
        long_speed_lr = (((byte1_speed_lr[int(i // K4)] * 256) + byte2_speed_lr[int(i // K4)]) - 10000) // 100
        long_speed_rr = (((byte1_speed_rr[int(i // K5)] * 256) + byte2_speed_rr[int(i // K5)]) - 10000) // 100

        long_rpm = int(((byte1_rpm[int(i / K6)] * 256) + byte2_rpm[int(i / K6)]) // 3.6)

        gear = byte_gear[int(i / K7)];
        #not sure for gear select
        long_gear = 0
        if gear >= 16:
            long_gear = 1
        if gear >= 35:
            long_gear = 2
        if gear >= 51:
            long_gear = 3
        if gear >= 67:
            long_gear = 4
        if gear >= 83:
            long_gear = 5

 #   long_fuel = (((byte1_fuel[int(i // K8)] * 256) + byte2_fuel[int(i // K8)])) // 10

        long_acc = int(byte_acc[int(i // K8)] // 2)

        long_temp = int(byte_temp[int(i // K9)]) - 15


        print("\"" + str(timez[i]) + "\"," + str(long_speed) + "," + str(long_speed_lf) + "," + str(long_speed_rf) + ","
              + str(long_speed_lr) + "," + str(long_speed_rr) + "," + str(long_rpm) + "," + str(long_gear) + "," + str(long_acc) + ","
            + str(long_temp))
    except:
        print("baga...", file=sys.stderr)


sys.stdout = orig_stdout
f.close()

print("ok!")
