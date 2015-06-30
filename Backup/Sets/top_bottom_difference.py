from CFoamPlot import temp_dp_plot #Library containing CFoam plot functions

##########################################################################################

# data_normal = import_data("27_03_2015", "11_41_15", "17mbar") #With leak: normal position
# data_inverted = import_data("30_03_2015", "15_12_27", "17mbar") #With leak: inverted position

# power_print(data_normal)
#temp_dp_plot(data_normal)
#temp_plot( correct_for(data_inverted[TEMP], gasIn) )

# temp_dp_plot(data_inverted)
# power_print(data_inverted)

# point = int(7000 / step_size(data_normal)[0])
# print "Top Power: ", data_normal[PS][topVoltage][point] * data_normal[PS][topCurrent][point]
# print "Bot Power: ", data_normal[PS][botVoltage][point] * data_normal[PS][botCurrent][point]

##########################################################################################

data_normal2 = import_data("31_03_2015", "09_50_06", "17mbar") #With leak: normal position SECOND RUN
data_inverted2 = import_data("31_03_2015", "12_34_38", "17mbar") #With leak: inverted position SECOND RUN

# temp_dp_plot(data_normal2)
# temp_dp_plot(data_inverted2)
temp_plot( correct_for(data_inverted2[TEMP], gasIn) ) 

##########################################################################################