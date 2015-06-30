########## IMPORTS ##########
import csv
import os.path
import matplotlib.pyplot as plt
import csv
import numpy as np

########## FILE NAME ##########
file_name = "Thermocouple_12_58_37_(20mbar)_0.735wcm.file"
date = "09_02_2015"
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
for i in range(0,17):
    temp.append([])
    
Temp = []
for i in range(0,17):
    Temp.append([])
    
########## FILL FIRST CARRIER LIST ##########
reader = csv.reader(data_file,delimiter="\t")

for t, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16 in reader:
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
    
data_file.close()

########## CONVERT STR TO FLOAT IN SECOND CARRIER LIST ##########
if float(temp[0][0])!=0:
    for j in range(0,17):
        for i in range(1,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
else:
    for j in range(0,17):
        for i in range(0,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))

##########                ##########                 
########## DESIRED OUTPUT ##########
##########                ##########

ts = 7

########## INITIALISE PLOT AND ADD DATA ##########
fig = plt.figure()

ax1 = fig.add_subplot(3, 1, 1)
for i in range(1,7):
    ax1.plot(Temp[0], Temp[i], label=i)

########## TOP TITLE ##########
ax1.set_title("Top CFoam Temperature", fontsize=1.1*ts, color='black')
plt.ylabel("Temperature (deg C)", fontsize = 1.3*ts)
########## AXIS INFO ##########
for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontsize(ts)
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontsize(ts)
plt.legend(fontsize= ts, title='Legend')
plt.grid()

ax2 = fig.add_subplot(3, 1, 2)
for i in range(7,13):
    ax2.plot(Temp[0], Temp[i], label=i)

########## BOTTOM TITLE ##########
ax2.set_title("Bottom CFoam Temperature", fontsize=1.1*ts, color='black')
plt.ylabel("Temperature (deg C)", fontsize = 1.3*ts)
########## AXIS INFO ##########
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(ts)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(ts)
plt.legend(fontsize= ts, title='Legend')
plt.grid()

ax2 = fig.add_subplot(3, 1, 3)
for i in range(13,17):
    ax2.plot(Temp[0], Temp[i], label=i)

########## AMBIENT AND GAS TITLE ##########
ax2.set_title("Gas and Ambient CFoam Temperature", fontsize=1.1*ts, color='black')
plt.ylabel("Temperature (deg C)", fontsize = 1.3*ts)
plt.xlabel("Time (s)", fontsize = 1.3*ts)
########## AXIS INFO ##########
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(ts)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(ts)
plt.legend(fontsize= ts, title='Legend')
plt.grid()

########## DISPLAY ##########
#plt.show()

fig_name = file_name.replace(".file","")
fig_format = ".png"
fig_path = os.path.join("Output", date)
fig_file_path = os.path.join(fig_path, fig_name + fig_format)
print " "
print fig_path
print fig_file_path

if not os.path.exists(fig_path):
    os.makedirs(fig_path)

plt.savefig(fig_file_path, dpi = 900)


########## CALCULATIONS ##########

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

# step = int(1)
# dif = []
# for i in range( 0, len(Temp[13])-step ):
#     dif.append( (Temp[13][i+step] - Temp[13][i])/step )
    
# for i in range(10000, len(Temp[2]) - 360 ):
#     diff = abs(Temp[2][i] - Temp[2][i+360])
#     if diff < 0.02:
#         print i, diff
