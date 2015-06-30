########## IMPORTS ##########
import csv
import os.path
import matplotlib.pyplot as plt
import csv
import numpy as np
import scipy

########## FILE NAME ##########
file_name = "Voltage_15_55_27_(5mbar).file"
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
for i in range(0,12):
    temp.append([])
    
Temp = []
for i in range(0,12):
    Temp.append([])
    
########## FILL FIRST CARRIER LIST ##########
reader = csv.reader(data_file,delimiter="\t")

for t, v1, v2, v3, v4, v5, v6, v7, v8, p, pp in reader:
    temp[0].append(t)
    temp[1].append(v1)
    temp[2].append(v2)
    temp[3].append(v3)
    temp[4].append(v4)
    temp[5].append(v5)
    temp[6].append(v6)
    temp[7].append(v7)
    temp[8].append(v8)
    temp[9].append(p)
    temp[10].append(pp)
    
data_file.close()

########## CONVERT STR TO FLOAT IN SECOND CARRIER LIST ##########
if float(temp[0][0])!=0:
    for j in range(0,10):
        for i in range(1,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
else:
    for j in range(0,10):
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


print "Pressure mean:", mean(Temp[9])
print "Pressure std deviation:", std_deviation(Temp[9])
print "-------------"
for i in range(1,5):
    print "Top voltage %i mean: " %i, mean(Temp[i])
    print "Top voltage %i std deviation: " %i, std_deviation(Temp[i])
print "-------------"
for i in range(5,9):
    print "Bottom voltage %i mean: " %i, mean(Temp[i])
    print "Bottom voltage %i std deviation: " %i, std_deviation(Temp[i])
    



##########           ##########
########## PLOT DATA ##########
##########           ##########

########## INITIALISE PLOT AND ADD DATA ##########
fig = plt.figure()

ax1 = fig.add_subplot(3, 1, 1)
for i in range(1,5):
    ax1.plot(Temp[0], Temp[i], label=i)

########## TOP TITLE ##########
ax1.set_title("Top CFoam Voltage", fontsize=14, color='black')
plt.ylabel("Voltage (V)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontsize(16)
    ax1.set_yticks(scipy.arange(min_max(Temp, 1, 5)[1]-0.05, min_max(Temp, 1, 5)[0]+0.05,0.02))
    
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

ax2 = fig.add_subplot(3, 1, 2)
for i in range(5,9):
    ax2.plot(Temp[0], Temp[i], label=i)

########## BOTTOM TITLE ##########
ax2.set_title("Bottom CFoam Voltage", fontsize=14, color='black')
plt.ylabel("Voltage (V)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(16)
    ax2.set_yticks(scipy.arange(min_max(Temp, 5, 9)[1]-0.05, min_max(Temp, 5, 9)[0]+0.05,0.02))
    
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

ax3 = fig.add_subplot(3, 1, 3)
for i in range(9,10):
    ax3.plot(Temp[0], Temp[i], label=i)

########## AMBIENT AND GAS TITLE ##########
ax3.set_title("Gas and Ambient CFoam Temperature", fontsize=14, color='black')
plt.ylabel("Delta P (mbar)", fontsize = 16)
plt.xlabel("Time (s)", fontsize = 16)
########## AXIS INFO ##########
for tick in ax3.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax3.yaxis.get_ticklabels():
    tick.set_fontsize(16)
    ax3.set_yticks(scipy.arange(min_max(Temp, 9, 10)[1]-0.05, min_max(Temp, 9, 10)[0]+0.1,0.04))
    
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()


########## DISPLAY ##########
plt.show()


