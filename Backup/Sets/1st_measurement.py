##########################################################################################

from CFoamPlot import * #Library containing CFoam plot functions

##########################################################################################

data10 = import_data("16_03_2015", "13_02_37", "20mbar")
data11 = import_data("16_03_2015", "23_54_39", "20mbar")
data12 = import_data("17_03_2015", "10_32_49", "20mbar")

#print flow(data10)

#htc_point(data1)
# gas_comparisson( data10, data11, data12)
#htc_plot(data10, data11, data12)

##########################################################################################

data7 = import_data("12_03_2015", "10_28_02", "15mbar")
data8 = import_data("12_03_2015", "15_36_45", "15mbar")
data9 = import_data("13_03_2015", "09_26_17", "15mbar")

# gas_comparisson( data7, data8, data9)
# # htc_plot(data7, data8, data9)

#########################################################################################

data4 = import_data("10_03_2015", "15_26_13", "10mbar")
data5 = import_data("10_03_2015", "21_21_48", "10mbar")
data6 = import_data("11_03_2015", "16_23_09", "10mbar")

# gas_comparisson( data4, data5, data6)
# # htc_plot(data4, data5, data6)

##########################################################################################

data1 = import_data("09_03_2015", "10_32_15", "5mbar")
data2 = import_data("09_03_2015", "15_55_27", "5mbar")
data3 = import_data("10_03_2015", "09_49_04", "5mbar")

# gas_comparisson( data1, data2, data3)
# # htc_plot(data1, data2, data3)

##########################################################################################

# # data_leak = import_data("26_03_2015", "15_04_33", "20mbar")

# # temp_dp_plot(data_leak)

##########################################################################################

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
