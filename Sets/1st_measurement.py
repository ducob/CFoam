##########################################################################################

from CFoamPlot import * #Library containing CFoam plot functions

##########################################################################################

data20MBAR0_0245wcm2 = import_data("16_03_2015", "13_02_37", "20mbar")
data20MBAR0_049wcm2 = import_data("16_03_2015", "23_54_39", "20mbar")
data20MBAR0_098wcm2 = import_data("17_03_2015", "10_32_49", "20mbar")

##########################################################################################

data15MBAR0_0245wcm2 = import_data("12_03_2015", "10_28_02", "15mbar")
data15MBAR0_049wcm2 = import_data("12_03_2015", "15_36_45", "15mbar")
data15MBAR0_098wcm2 = import_data("13_03_2015", "09_26_17", "15mbar")

#########################################################################################

data10MBAR0_0245wcm2 = import_data("10_03_2015", "15_26_13", "10mbar")
data10MBAR0_049wcm2 = import_data("10_03_2015", "21_21_48", "10mbar")
data10MBAR0_098wcm2 = import_data("11_03_2015", "16_23_09", "10mbar")

##########################################################################################

data5MBAR0_0245wcm2 = import_data("09_03_2015", "10_32_15", "5mbar")
data5MBAR0_049wcm2 = import_data("09_03_2015", "15_55_27", "5mbar")
data5MBAR0_098wcm2 = import_data("10_03_2015", "09_49_04", "5mbar")

##########################################################################################

### settings
flows = [5, 10, 15, 20]
powerDensities = [0.0245, 0.0490, 0.0980]
fraction = 0.8
window = 4000
decimals = 4

for _flow in flows:
    for _powerDensity in powerDensities:
        globals()['htc%sMBAR%swcm2' % (str(_flow), str(_powerDensity).replace('.',
        '_'))] = avgHtcFunction(eval('data%sMBAR%swcm2' % (str(_flow), str(_powerDensity).replace('.',
        '_'))), labEnv, fraction, window )

##########################################################################################

def htcSpreadSheet ( flows, powerDensities ):
    file=open('Heat_Transfer_Coefficient_FIRST.txt', 'w')
    
    file.write('Heat Transfer Coefficient Data\n')
    file.write('\n')

    file.write('Strip Area\t %s \t cm2\n' % A)
    file.write('Power Correction Slope \t %s \t W/deg C(lab)\n' % 0.1022)
    file.write('\n')
    
    file.write('Case \t Flow \t Strip Power \t \t \t \t Temperatures \t \t \t \t T_lab \t T_gasIn \t T_gasOut \t HTC \t \t \t \t Mean HTC\n')

    for _flow in flows:
        for _pd in powerDensities:
            _flow = str(_flow)
            _pd = str(_pd).replace('.','_')
            HTC = eval('htc%sMBAR%swcm2' %(_flow, _pd))
            ADC, PS, TEMP = avgData(eval('data%sMBAR%swcm2'%(_flow,_pd)), 0, fraction, window)
            adc, ps, temp = avgData(eval('data%sMBAR%swcm2'%(_flow,_pd)), labEnv, fraction, window)
            
            file.write('%sMBAR@%s\t' %(_flow, _pd))
            file.write('%s \t' % _flow)
            
            for i in xrange(1,9):
                globals()['p%s' % i] = pow(adc[i]/5., 2)*15.
            file.write('%s \t %s \t %s \t %s \t' % (p1, p2, p3, p4) )
            
            file.write('%s \t %s \t %s \t %s \t' % (temp[str1], temp[str2], temp[str3], temp[str4]) )
            file.write('%s \t %s \t %s \t' % (TEMP[labEnv], temp[gasIn], temp[gasOut]))
            file.write('%s \t %s \t %s \t %s \t %s \n' % (HTC[0], HTC[1], HTC[2], HTC[3], mean(HTC)) )
            
            file.write('\t \t %s \t %s \t %s \t %s \t' % (p5, p6, p7, p8) )
            file.write('%s \t %s \t %s \t %s \t' % (temp[str5], temp[str6], temp[str7], temp[str8]) )
            file.write('\t \t \t %s \t %s \t %s \t %s \n' % (HTC[4], HTC[5], HTC[6], HTC[7]))
            file.write('\n')
    
    file.close()

    
htcSpreadSheet(flows, powerDensities)




# pdArray = []
# for i in range(1,13):
# 	pdArray.append( mean( power_density( eval("data"+str(i)) )[2] ) )
# stArray = []
# for i in range(1,13):
# 	stArray.append( stable_temperature( eval("data"+str(i)) ) )
# markerArray = []
# colorArray = []
# labelCounter = []
# for i in range(0, 12):
# 	if i<3:
# 		markerArray.append("o")
# 		colorArray.append("#0000FF")
# 		labelCounter.append(1)
# 	if i>=3 and i<6:
# 		markerArray.append("s")
# 		colorArray.append("#33CC33")
# 		labelCounter.append(2)
# 	if i>=6 and i<9:
# 		markerArray.append("x")
# 		colorArray.append("#FF9933")
# 		labelCounter.append(3)
# 	if i>=9 and i<12:
# 		markerArray.append("h")
# 		colorArray.append("#FF0000")
# 		labelCounter.append(4)

# for _x, _y, _m, _c, _l in zip(pdArray, stArray, markerArray, colorArray, labelCounter):
# 	if _l == 1:
# 		dp5 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))
# 	if _l == 2:
# 		dp10 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))
# 	if _l == 3:
# 		dp15 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))
# 	if _l == 4:
# 		dp20 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))

# plt.legend( (dp5, dp10, dp15, dp20), ("5mbar", "10mbar", "15mbar", "20mbar"), scatterpoints=1)
# plt.ylabel("Avg. Cupper Temperature (lab corrected) ("u"\u00b0""C)", fontsize = 16.)
# plt.xlabel("Power Density (W/cm"u'\u00B2'")", fontsize = 16.)
# plt.xticks(np.arange(0, 0.12, 0.02))
# plt.yticks(np.arange(0, 20, 1))
# plt.grid()
# pd_st = plt.show()

# ##########################################################################################

# pcArray = []
# for T in stArray:
# 	pcArray.append( power_correction(T) )

# for _x, _y, _m, _c, _l in zip(stArray, pcArray, markerArray, colorArray, labelCounter):
# 	if _l == 1:
# 		dp5 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))
# 	if _l == 2:
# 		dp10 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))
# 	if _l == 3:
# 		dp15 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))
# 	if _l == 4:
# 		dp20 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate(round(_x,5), (_x,_y))

# plt.legend( (dp5, dp10, dp15, dp20), ("5mbar", "10mbar", "15mbar", "20mbar"), scatterpoints=1)
# plt.xlabel("Avg. Cupper Temperature (lab corrected) ("u"\u00b0""C)", fontsize = 16.)
# plt.ylabel("Power Correction (W)", fontsize = 16.)
# plt.yticks(np.arange(0, 3, 0.2))
# plt.xticks(np.arange(0, 20, 1))
# plt.grid()
# st_pc = plt.show()

# ##########################################################################################

# pArray = []
# for i in range(1,13):
# 	pArray.append( mean( power( eval("data"+str(i)) )[4] ) )

# for _x, _y, _m, _c, _l, _T in zip(pArray, pcArray, markerArray, colorArray, labelCounter, stArray):
# 	if _l == 1:
# 		dp5 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))
# 	if _l == 2:
# 		dp10 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))
# 	if _l == 3:
# 		dp15 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))
# 	if _l == 4:
# 		dp20 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))

# plt.legend( (dp5, dp10, dp15, dp20), ("5mbar", "10mbar", "15mbar", "20mbar"), scatterpoints=1)
# plt.xlabel("Power Deposited in Resistors (W)", fontsize = 16.)
# plt.ylabel("Power Correction (W)", fontsize = 16.)
# plt.yticks(np.arange(0, 3, 0.2))
# plt.xticks(np.arange(0, 20, 1))
# plt.grid()
# p_pc = plt.show()

# ##########################################################################################

# ratioArray = []
# for _T, _P in zip(stArray, pArray):
# 	ratioArray.append( (power_correction(_T) / _P)*100 )

# for _x, _y, _m, _c, _l, _T in zip(pdArray, ratioArray, markerArray, colorArray, labelCounter, stArray):
# 	if _l == 1:
# 		dp5 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))
# 	if _l == 2:
# 		dp10 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))
# 	if _l == 3:
# 		dp15 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))
# 	if _l == 4:
# 		dp20 = plt.scatter(_x, _y, marker = _m, color = _c, s=60)
# 		plt.annotate("T="+str(round(_T,5)), (_x,_y))

# plt.legend( (dp5, dp10, dp15, dp20), ("5mbar", "10mbar", "15mbar", "20mbar"), scatterpoints=1)
# plt.xlabel("Power Density (W/cm"u'\u00B2'")", fontsize = 16.)
# plt.ylabel("Ratio Power Correction to Deposited Power", fontsize = 16.)
# plt.yticks(np.arange(0, 15, 1))
# plt.xticks(np.arange(0, 0.12, 0.02))
# plt.grid()
# pd_ratio = plt.show()

#########################################################################################

# def htc_avg(data):
# 	adc, ps, temp = data

# 	avg_cu_temp = stable_temperature(data, correction=False)
# 	avg_cu_temp_labcorr = stable_temperature(data)
# 	p = mean(power(data)[4])
# 	print "Mean power: ", p
# 	print "Power correction at T = ", avg_cu_temp, " | T_lab = ", avg_cu_temp_labcorr, " : ", power_correction(avg_cu_temp_labcorr)
# 	p = p  -  power_correction( avg_cu_temp_labcorr )
# 	print "Power in cfoam: ", p
# 	print "mean gas out T: ", mean(temp[gasOut])
# 	print "mean gas out T_lab: ", mean(correct_for(temp, corr = labEnv)[gasOut])
# 	htc = p / (18.73*4 * ( avg_cu_temp_labcorr - (mean(correct_for(temp, corr = labEnv)[gasOut])-mean(correct_for(temp, corr = labEnv)[gasIn])) ))
# 	temp_plot(temp)
# 	return 0


# htc_avg(data1)
