########## IMPORTS ##########
import csv
import os.path
import matplotlib.pyplot as plt
import csv
import numpy as np
import matplotlib.dates as mdates
import scipy
import datetime
import sys

execfile('CFoamMap.py')

##########################################################################################
### Return the size (in MBs rounded to 3 decimals) of the CFAOM data object
def memory_size(data):
    size = 0
    #TEMP
    for thermocouple in range(0,17):
        size += sys.getsizeof(data[TEMP][thermocouple])
    #ADC
    for adcChannel in range(0, 11):
        size += sys.getsizeof(data[ADC][adcChannel])
    #PS
    for psChannel in range(0, 7):
        size += sys.getsizeof(data[ADC][psChannel])
    return round(size/1048576.,3)


def import_data ( date, file_time, file_extension, timeBool = False ):
    ########## FILE NAMES AND PATHS ##########
    file_time = "_"+file_time
    file_extension = "_("+file_extension+").file"

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
    if not os.path.exists(file_path_clean_V):
        with open(file_path_V, "rb") as infile, open(file_path_clean_V, "wb") as outfile:
            reader = csv.reader(infile)
            next(reader, None)
            writer = csv.writer(outfile)
            for row in reader:
                if not row[0].startswith("Measurement"):
                    writer.writerow(row)

    if not os.path.exists(file_path_clean_PS):
        with open(file_path_PS, "rb") as infile, open(file_path_clean_PS, "wb") as outfile:
            reader = csv.reader(infile)
            next(reader, None)
            writer = csv.writer(outfile)
            for row in reader:
                if not row[0].startswith("Measurement"):
                    writer.writerow(row)

    if not os.path.exists(file_path_clean_TC):
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
    data = Adc, Ps, Temp
    print date+file_time+file_extension+': Cleaned and Initialized'
    print '\t Has size: %s mb\n' %memory_size(data)
    if timeBool == False:
        return Adc, Ps, Temp
        print ''

    ########## Include time information in return ##########
    if timeBool == True:

        dateArray = date.split("_")
        file_time = file_time[1:]
        timeArray = file_time.split("_")
        dateArray = map(int, dateArray)
        timeArray = map(int, timeArray)
        startTime = datetime.datetime(dateArray[2], dateArray[1], dateArray[0], timeArray[0], timeArray[1], int(round(timeArray[2],1)))

        realTimeArray = []
        for time in Adc[0]:
            timeStep = startTime + datetime.timedelta(seconds=time)
            realTimeArray.append( timeStep )

        print "\t Option: time information added\n"
        return Adc, Ps, Temp, realTimeArray
    
    

