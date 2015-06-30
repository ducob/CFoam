########## IMPORTS ##########
import csv
import os.path
import matplotlib.pyplot as plt
import csv
import numpy as np
import scipy

########## FILE NAMES AND PATHS ##########

date = "16_03_2015"
file_time = "_23_54_39"
file_extension = "_(20mbar).file"

volt = "Voltage"
ps = "Powersupply"
tem = "Thermocouple"

file_name_V = os.path.join(volt+file_time+file_extension)
file_name_PS = os.path.join(ps+file_time+file_extension)
file_name_TC = os.path.join(tem+file_time+file_extension)

file_path_V = os.path.join("files", date, volt+file_time+file_extension)
file_path_PS = os.path.join("files", date, ps+file_time+file_extension)
file_path_TC = os.path.join("files", date, tem+file_time+file_extension)

file_path_clean_V = os.path.join("files/clean", date, file_name_V)
file_path_clean_PS = os.path.join("files/clean", date, file_name_PS)
file_path_clean_TC = os.path.join("files/clean", date, file_name_TC)

folder_path_clean = os.path.join("files/clean", date)

if not os.path.exists(folder_path_clean):
    os.makedirs(folder_path_clean)

########## REMOVE THE HEADER AND FOOTER ##########
with open(file_path_V, "rb") as infile, open(file_path_clean_V, "wb") as outfile:
    reader = csv.reader(infile)
    next(reader, None)
    writer = csv.writer(outfile)
    for row in reader:
        if not row[0].startswith("Measurement"):
            writer.writerow(row)

with open(file_path_PS, "rb") as infile, open(file_path_clean_PS, "wb") as outfile:
    reader = csv.reader(infile)
    next(reader, None)
    writer = csv.writer(outfile)
    for row in reader:
        if not row[0].startswith("Measurement"):
            writer.writerow(row)

with open(file_path_TC, "rb") as infile, open(file_path_clean_TC, "wb") as outfile:
    reader = csv.reader(infile)
    next(reader, None)
    writer = csv.writer(outfile)
    for row in reader:
        if not row[0].startswith("Measurement"):
            writer.writerow(row)
            
########## OPEN CLEANED FILE ##########
data_file_V = open(file_path_clean_V, "r")
data_file_PS = open(file_path_clean_PS, "r")
data_file_TC = open(file_path_clean_TC, "r")

########## CARRIER LISTS ##########
adc = []   #Voltage probe string list
for i in range(0,12):
    adc.append([])
Adc = []   #Voltage probe float list
for i in range(0,12):
    Adc.append([])

ps = []  #Power Supply probe string list
for i in range(0,8):
    ps.append([])
Ps = []  #Power supply probe float list
for i in range(0,8):
    Ps.append([])
    
temp = []  #Thermocouple probe string list
for i in range(0,17):
    temp.append([])
Temp = []  #Thermoucouple probe float list
for i in range(0,17):
    Temp.append([])

########## FILL FIRST CARRIER LIST ##########
reader = csv.reader(data_file_V,delimiter="\t")
for t, v1, v2, v3, v4, v5, v6, v7, v8, p, pp in reader:
    adc[0].append(t)
    adc[1].append(v1)
    adc[2].append(v2)
    adc[3].append(v3)
    adc[4].append(v4)
    adc[5].append(v5)
    adc[6].append(v6)
    adc[7].append(v7)
    adc[8].append(v8)
    adc[9].append(p)
    adc[10].append(pp)

reader2 = csv.reader(data_file_PS,delimiter="\t")
for t, tvb, tv, tc, bvb, bv, bc in reader2:
    ps[0].append(t)
    ps[1].append(tvb)
    ps[2].append(tv)
    ps[3].append(tc)
    ps[4].append(bvb)
    ps[5].append(bv)
    ps[6].append(bc)

reader3 = csv.reader(data_file_TC,delimiter="\t")
for t, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16 in reader3:
    temp[0].append(t)
    temp[1].append(s1)
    temp[2].append(s2)
    temp[3].append(s3)
    temp[4].append(s4)
    temp[5].append(s5)
    temp[6].append(s6)
    temp[7].append(s7)
    temp[8].append(s8)
    temp[9].append(s9)
    temp[10].append(s10)
    temp[11].append(s11)
    temp[12].append(s12)
    temp[13].append(s13)
    temp[14].append(s14)
    temp[15].append(s15)
    temp[16].append(s16)
    
data_file_V.close()
data_file_PS.close()
data_file_TC.close()

########## CONVERT STR TO FLOAT IN SECOND CARRIER LIST ##########
if float(adc[0][0])!=0:
    for j in range(0,10):
        for i in range(1,len(adc[j]) ):
            Adc[j].append(float(adc[j][i]))
else:
    for j in range(0,10):
        for i in range(0,len(adc[j]) ):
            Adc[j].append(float(adc[j][i]))

c_list = {0,2,3,5,6}
if float(ps[0][0])!=0:
    for j in c_list:
        for i in range(1,len(ps[j]) ):
            Ps[j].append(float(ps[j][i]))
else:
    for j in c_list:
        for i in range(0,len(ps[j]) ):
            Ps[j].append(float(ps[j][i]))

if float(temp[0][0])!=0:
    for j in range(0,17):
        for i in range(1,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
else:
    for j in range(0,17):
        for i in range(0,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
            

########## RANGE FUNCTION ##########
def min_max(list, first, last):
    return_list=[]
    max_val = 0
    for i in range(first,last):
        if  max(Temp[i]) > max_val:
            max_val = max(Temp[i])
    return_list.append(max_val)

    min_val = max_val
    for i in range(first,last):
        if min(Temp[i]) < min_val:
            min_val = min(Temp[i])
    return_list.append(min_val)

    return return_list

##########           ##########
########## FUNCTIONS ##########
##########           ##########
def sum(list):
    sum = 0
    for i in range(0, len(list)):
        sum = sum + list[i]
    return sum

def mean(list):
    sum = 0
    for i in range(0, len(list)):
        sum = sum + list[i]
    return sum / len(list)

def variance(list):
    average = mean(list)
    variance = 0
    for i in list:
        variance = variance + ((average - i)**2)
    return variance / len(list)

def std_deviation(list):
    return variance(list) ** 0.5
    
def power_correction(temperature):
    #slope = 0.097 #Frist correction measurement
    slope = 0.105 #second correction measurement
    #intercept = -2.28 #First correction measurement
    intercept = -2.524 #second correction measurement 
    return slope*temperature + intercept

def Flow(Power, foam_temperature, gas_in, gas_out):
    rho_gas = 1.1839        #in g/L @ 25 deg C
    c_v_gas = 1.012         #in J/(g*K)
    delta_T = gas_out - gas_in
    
    LPS = (Power - power_correction(foam_temperature))/(rho_gas * c_v_gas * delta_T)    #Litre per second
    LPM = LPS * 60  #Litre per minute
    return LPM
    
def Flow_Equal(list):
        return float(np.array(list)[np.diff(list, axis=0)==min(abs(np.diff(list, axis=0)))])
        
stepsize = [] 
for i in range(0, len(Temp[0])-1):
    stepsize.append(Temp[0][i+1] - Temp[0][i])

##########                ##########
########## DESIRED OUTPUT ##########
##########                ##########

# Strip data
A = 18.73
R_probe_top_i = [5.3, 5.3, 5.3, 5.3]
R_strip_top_j = [15.3, 15.3, 15.3, 15.4]
R_probe_bot_i = [5.3, 5.3, 5.2, 5.3]
R_strip_bot_j = [15.3, 15.3, 15.3, 15.3]
Partial_P_top = []  # Power in Top per strip
Partial_P_bot = []  # Power in Bottom per strip
    
# Fill and Print out of Power per strip (calculated with voltage probe data)
print "date: ", date
print "Time: ", file_time
print "Pressure: ", file_extension
print "Time of measurement: ", Temp[0][len(Temp[0])-1]
print " "
print "-------------"
print " "
for i in range(0,4):
    Partial_P_top.append(pow(mean(Adc[i+1])/R_probe_top_i[i],2)*R_strip_top_j[i])
    print "Power in strip", i, ": ", Partial_P_top[i], " W"
for i in range(0,4):
    Partial_P_bot.append(pow(mean(Adc[i+5])/R_probe_bot_i[i],2)*R_strip_bot_j[i])
    print "Power in strip", i+5, ": ", Partial_P_bot[i], " W"
print "===="
# Calculation of total power and Print Out
total_pow = sum(Partial_P_top) + sum(Partial_P_bot)
print "Total power on top: ", sum(Partial_P_top), " W"    
print "Total power on bottom: ", sum(Partial_P_bot), " W"
print "Total power on CFOAM device: ", total_pow, " W"
print " "
print "-------------"
print " "
# Power density calculation 
for i in range(0,4):
    print "Power density in strip", i, ": ", Partial_P_top[i]/A, " W/cm2"
    print "Power density in strip", i+5, ": ", Partial_P_bot[i]/A, " W/cm2"
print "===="
print "Power density on top: ", sum(Partial_P_top)/(4*A), " W/cm2"
print "Power density on bottom: ", sum(Partial_P_bot)/(4*A), " W/cm2"
print "Average power density on CFOAM device: ", (sum(Partial_P_top) + sum(Partial_P_bot))/(8*A), " W/cm2"
print ""
print "-------------"
print ""

# Power in top and bottom per sample (calculated from power supply data)
pow_top = []
pow_bot = []
for i in range(0, len(Temp[0])):
    pow_top.append(Ps[2][i]*Ps[3][i])
    pow_bot.append(Ps[5][i]*Ps[6][i])

# # Temperature Equalibrium finding
# equa_temp = []
# high = 5
# for i in range(0, len(Top_Avg)-high):
#     temp_temp = 0
#     for j in range(0, high):
#         temp_temp += Top_Avg[i+j]
#     equa_temp.append(temp_temp/high)
#     print equa_temp[i]
# print "==="
# print "Max avg Temp: ", max(equa_temp)


# Top Avg Temp (all strips)
Top_Avg = []
for i in range(0, len(Temp[0])):
    Top_Avg.append( (Temp[1][i] + Temp[2][i] + Temp[3][i] + Temp[4][i] + Temp[5][i] + Temp[6][i])/6 )
    
# Bottom Avg Temp (all strips)
Bot_Avg = []
for i in range(0, len(Temp[0])):
    Bot_Avg.append( (Temp[7][i] + Temp[8][i] + Temp[9][i] + Temp[10][i] + Temp[11][i] + Temp[12][i])/6 )

Flow_calc = []
for i in range(0, len(Temp[0])):
    Flow_calc.append( Flow(total_pow, (Top_Avg[i]+Bot_Avg[i])/2, Temp[13][i], Temp[14][i]) )
    # print "Estimated Flow (time = ",i*mean(stepsize),", dp = ", adc[9][i], ":)", Flow_calc[i]
    
########## INITIALISE PLOT AND ADD DATA ##########
fig = plt.figure()

ax1 = fig.add_subplot(3, 1, 1)
#top_names = ["strip 1 corner", "strip 1 center", "strip 2", "strip 3", "strip 4", "strip 5", "strip 6 center", "strip 6 corner"]
for i in range(1,7):
    ax1.plot(Temp[0], Temp[i], label=i)
    
########## TOP TITLE ##########
ax1.set_title("Top CFoam Temperature", fontsize=14, color='black')
plt.ylabel("Temperature (deg C)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontsize(16)
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

ax2 = fig.add_subplot(3, 1, 2)
for i in range(7,13):
    ax2.plot(Temp[0], Temp[i], label=i)

########## BOTTOM TITLE ##########
ax2.set_title("Bottom CFoam Temperature", fontsize=14, color='black')
plt.ylabel("Temperature (deg C)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(16)
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

ax2 = fig.add_subplot(3, 1, 3)
for i in range(13,17):
    ax2.plot(Temp[0], Temp[i], label=i)

########## AMBIENT AND GAS TITLE ##########
ax2.set_title("Gas and Ambient CFoam Temperature", fontsize=14, color='black')
plt.ylabel("Temperature (deg C)", fontsize = 16)
plt.xlabel("Time (s)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(16)
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

######### DISPLAY ##########
plt.show()
