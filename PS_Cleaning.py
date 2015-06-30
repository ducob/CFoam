########## IMPORTS ##########
import csv
import os.path
import matplotlib.pyplot as plt
import csv
import numpy as np
import scipy

########## FILE NAME ##########
file_name = "Powersupply_15_55_27_(5mbar).file"
date = "09_03_2015"
file_path = os.path.join("files", date, file_name)
file_path_clean = os.path.join("files/clean", date, file_name)
folder_path_clean = os.path.join("files/clean", date)
if not os.path.exists(folder_path_clean):
    os.makedirs(folder_path_clean)
        
########## REMOVE THE HEADER AND FOOTER ##########
with open(file_path, "rb") as infile, open(file_path_clean, "wb") as outfile:
    reader = csv.reader(infile)
    next(reader, None)
    writer = csv.writer(outfile)
    for row in reader:
        if not row[0].startswith("Measurement"):
            writer.writerow(row)
            
########## OPEN CLEANED FILE ##########
data_file = open(file_path_clean, "r")

########## CARRIER LISTS ########## 
temp = []
for i in range(0,8):
    temp.append([])
    
Temp = []
for i in range(0,8):
    Temp.append([])
    
########## FILL FIRST CARRIER LIST ##########
reader = csv.reader(data_file,delimiter="\t")

for t, tvb, tv, tc, bvb, bv, bc in reader:
    temp[0].append(t)
    temp[1].append(tvb)
    temp[2].append(tv)
    temp[3].append(tc)
    temp[4].append(bvb)
    temp[5].append(bv)
    temp[6].append(bc)
    
data_file.close()

########## CONVERT LIST ##########
c_list = {0,2,3,5,6}

########## CONVERT STR TO FLOAT IN SECOND CARRIER LIST ##########
if float(temp[0][0])!=0:
    for j in c_list:
        for i in range(1,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
else:
    for j in c_list:
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

##########                ##########
########## DESIRED OUTPUT ##########
##########                ##########
top_power = mean(Temp[2])*mean(Temp[3])
bottom_power = mean(Temp[5])*mean(Temp[6])
Ptop = []
Pbot = []
Area = 4 * 18.73

for i in range(0, len(Temp[2]) ):
    Ptop.append(Temp[2][i]*Temp[3][i])
    Pbot.append(Temp[5][i]*Temp[6][i])

print "Power Supply Top Voltage mean:", mean(Temp[2]), "V"
print "Power Supply Top Voltage std deviation:", std_deviation(Temp[2]), "V"
print "Power Supply Top Current mean:", mean(Temp[3]), "A"
print "Power Supply Top Current std deviation:", std_deviation(Temp[3]), "A"
print "-------------"
print "Top power delivered: ", mean(Ptop), u"\u00B1", std_deviation(Ptop), "W"
print " "
print "Power Supply Bottom Voltage mean:", mean(Temp[5]), "V"
print "Power Supply Bottom Voltage std deviation:", std_deviation(Temp[5]), "V"
print "Power Supply Bottom Current mean:", mean(Temp[6]), "A"
print "Power Supply Bottom Current std deviation:", std_deviation(Temp[6]), "A"
print "-------------"
print "Bottom power delivered: ", mean(Pbot), u"\u00B1", std_deviation(Pbot), "W"
print " "
print "True Top Power density: ", mean(Ptop) / Area, "W/cm2"
print "True Bottom Power density: ", mean(Pbot) / Area, "W/cm2"
print "-------------"
print "Average Top Bottom Power Density: ", (mean(Ptop) + mean(Pbot))/(2*Area), "W/cm2"
print "-------------"
print "Total power Delivered: ", mean(Ptop) + mean(Pbot), "W" 


##########           ##########
########## PLOT DATA ##########
##########           ##########

########## INITIALISE PLOT AND ADD DATA ##########
fig = plt.figure()

ax1 = fig.add_subplot(2, 1, 1)
for i in {2, 5}:
    ax1.plot(Temp[0], Temp[i], label=i)

########## TOP TITLE ##########
ax1.set_title("Power Supply Voltage", fontsize=14, color='black')
plt.ylabel("Voltage (V)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontsize(16)
    ax1.set_yticks(scipy.arange(min_max(Temp, 2, 3)[1]-0.05, min_max(Temp, 2, 3)[0]+0.05,0.02))

plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

ax2 = fig.add_subplot(2, 1, 2)
for i in {3,6}:
    ax2.plot(Temp[0], Temp[i], label=i)

########## BOTTOM TITLE ##########
ax2.set_title("Power Supply Current", fontsize=14, color='black')
plt.ylabel("Current (A)", fontsize = 16)
plt.xlabel("Time (s)", fontsize=16)
########## AXIS INFO ##########
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(16)
    ax2.set_yticks(scipy.arange(min_max(Temp, 3, 4)[1]-0.05, min_max(Temp, 3, 4)[0]+0.05,0.02))

plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

########## DISPLAY ##########
plt.show()
