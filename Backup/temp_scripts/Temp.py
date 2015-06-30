#Packages
import matplotlib.pyplot as plt
import csv
import numpy as np

#File Input
data_file = open("files/Thermocouple_14_16_13_(0).file", "r")

#Carrier lists
temp = []
for i in range(0,17):
    temp.append([])
    
Temp = []
for i in range(0,17):
    Temp.append([])
    
#Fill lists
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

#string to float conversion
if float(temp[0][0])!=0:
    for j in range(0,17):
        for i in range(1,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
else:
    for j in range(0,17):
        for i in range(0,len(temp[j]) ):
            Temp[j].append(float(temp[j][i]))
            
#Desired Output

#Initialize plot and add data
fig = plt.figure()



ax1 = fig.add_subplot(3, 1, 1)
for i in range(1,7):
    ax1.plot(Temp[0], Temp[i], label=i)

#Set top plot title
ax1.set_title("Top CFoam Temperature", fontsize=14, color='black')
#Set Axis info
for tick in ax1.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax1.yaxis.get_ticklabels():
    tick.set_fontsize(16)
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()

ax2 = fig.add_subplot(3, 1, 2)
for i in range(7,13):
    ax2.plot(Temp[0], Temp[i], label=i)

#Set plot title
ax2.set_title("Bottom CFoam Temperature", fontsize=14, color='black')
#Set Axis info
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(16)
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()


ax2 = fig.add_subplot(3, 1, 3)
for i in range(13,17):
    ax2.plot(Temp[0], Temp[i], label=i)

#Set plot title
ax2.set_title("Gas and Ambient CFoam Temperature", fontsize=14, color='black')
#Set Axis info
for tick in ax2.xaxis.get_ticklabels():
    tick.set_fontsize(16)
for tick in ax2.yaxis.get_ticklabels():
    tick.set_fontsize(16)
plt.legend(fontsize= 16, title='LEGEND')
plt.grid()


plt.show()
#fig.savefig('test2.png', dpi=200)
