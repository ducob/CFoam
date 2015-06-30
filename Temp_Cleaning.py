########## IMPORTS ##########
import csv
import os.path
import matplotlib.pyplot as plt
import csv
import numpy as np

########## FILE NAME ##########
#Thermocouple_10_11_50_(NOFLOW).file
#Powersupply_10_22_07_(max20mbar).file
file_name = "Thermocouple_10_28_02_(15mbar).file"
date = "12_03_2015"
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

start_point = 0
endpoint = 0
if float(temp[0][0])!=0:
    for j in range(0,17):
        for i in range(start_point + 1,len(temp[j]) - endpoint ):
            Temp[j].append(float(temp[j][i]))
else:
    for j in range(0,17):
        for i in range(start_point,len(temp[j]) - endpoint):
            Temp[j].append(float(temp[j][i]))

stepsize = Temp[0][1] - Temp[0][0]
print "Plotting from:", min(Temp[0]), " to:", max(Temp[0]), "with stepsize:", stepsize

##########                       ##########                 
########## Time array conversion ##########
##########                       ##########

# Time_array = []
# for i in range(0, len(Temp[0])):
#     Time_array.append(Temp[0][i]/3600)
    
##########           ##########
########## FUNCTIONS ##########
##########           ##########
def sum(list, a, b):
    sum = 0
    for i in range(a, b):
        sum = sum + list[i]
    return sum

def mean(list, a, b):
    sum = 0
    for i in range(a, b):
        sum = sum + list[i]
    return sum / (b-a)

##########                ##########                 
########## DESIRED OUTPUT ##########
##########                ##########

# dev_T = []
# dev_t = []
# for i in range(0, len(Temp[1])-5):
#     tempp=0
#     tempt=0
#     for j in range(0, 5):
#         tempp = tempp + Temp[1][i+j]
#         tempt = tempt + Temp[0][i+j]
#     dev_T.append(tempp/5)
#     dev_t.append(tempt/5)
#
# print dev_T

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
########## CALCULATIONS ##########