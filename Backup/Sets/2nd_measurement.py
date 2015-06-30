##########################################################################################

from ExtractData import * #Import function to extract and organise data from the raw files
from CFoamPlot import * #Library containing CFoam plot functions
from CFoamFunctions import * #Library containing CFoam analysis functions

##########################################################################################

data30LPM0_01225wcm2 = import_data("06_05_2015", "11_42_56", "30lpm")    #0.01225
data30LPM0_0245wcm2 = import_data("06_05_2015", "17_07_26", "30lpm")    #0.0245
data30LPM0_049wcm2 = import_data("06_05_2015", "23_30_46", "30lpm")    #0.049
data30LPM0_049wcm2 = import_data("07_05_2015", "08_45_26", "30lpm")    #0.049
data30LPM0_098wcm2 = import_data("07_05_2015", "15_15_06", "30lpm")    #0.098

##########################################################################################
#threeDayPressureData = import_data("08_05_2015", "14_46_20", "pressure_stable", timeBool = True)
##########################################################################################

data50LPM0_0245wcm2 = import_data("12_05_2015", "12_30_39", "50lpm")    #0.0245
data50LPM0_049wcm2 = import_data("13_05_2015", "14_10_45", "50lpm")    #0.0490
data50LPM0_098wcm2 = import_data("18_05_2015", "11_16_44", "50lpm")    #0.0980

##########################################################################################

data60LPM0_0245wcm2 = import_data("20_05_2015", "09_53_38", "60lpm")  #0.0245
data60LPM0_049wcm2 = import_data("20_05_2015", "14_54_15", "60lpm") #0.0490
data60LPM0_098wcm2 = import_data("22_05_2015", "09_45_09", "60lpm") #0.0980

##########################################################################################
printing = False

### settings
flows = [30, 50, 60]
powerDensities = [0.0245, 0.0490, 0.0980]
fraction = 0.8
window = 4000
decimals = 4

for _flow in flows:
    for _powerDensity in powerDensities:
        globals()['htc%sLPM%swcm2' % (str(_flow), str(_powerDensity).replace('.',
        '_'))] = avgHtcFunction(eval('data%sLPM%swcm2' % (str(_flow), str(_powerDensity).replace('.',
        '_'))), labEnv, fraction, window )

def htcSpreadSheet ( flows, powerDensities ):
    file=open('Heat_Transfer_Coefficient.txt', 'w')
    
    file.write('Heat Transfer Coefficient Data\n')
    file.write('\n')

    file.write('Strip Area\t %s \t cm2\n' % A)
    file.write('Power Correction Slope \t %s \t W/deg C(lab)\n' % 0.1022)
    file.write('\n')
    
    file.write('Case \t Flow \t Strip Power \t Temperatures \t \t \t \t T_lab \t T_gasIn \t T_gasOut \t HTC \t \t \t \n')

    for _flow in flows:
        for _pd in powerDensities:
            _flow = str(_flow)
            _pd = str(_pd).replace('.','_')
            HTC = eval('htc%sLPM%swcm2' %(_flow, _pd))
            adc, ps, temp = avgData(eval('data%sLPM%swcm2'%(_flow,_pd)), labEnv, fraction, window)
            
            file.write('%sLPM@%s\t' %(_flow, _pd))
            file.write('%s \t' % _flow)
            
            power = pow(adc[1]/5., 2)*15.
            file.write('%s \t' % power)
            
            file.write('%s \t %s \t %s \t %s \t' % (temp[str1], temp[str2], temp[str3], temp[str4]))
            file.write('%s \t %s \t %s \t' % (temp[labEnv], temp[gasIn], temp[gasOut]))
            file.write('%s \t %s \t %s \t %s \n' % (HTC[0], HTC[1], HTC[2], HTC[3]))
            
            file.write('\t \t \t %s \t %s \t %s \t %s \t' % (temp[str5], temp[str6], temp[str7], temp[str8]))
            file.write('\t \t \t %s \t %s \t %s \t %s \n' % (HTC[4], HTC[5], HTC[6], HTC[7]))
            file.write('\n')
    
    file.close()

    
htcSpreadSheet(flows, powerDensities)

# for i in xrange(1,12):
#     print "Data%s, has length %s corresponding to %s seconds" %(i, len( eval("data"+str(i))[ADC][TIME] ), eval("data"+str(i))[ADC][TIME][-1])
def htc_plot ( data1, data2, data3 ):
    powerArray = []
    for i in range(0,8):
        powerArray.append( mean(power_density(data1)[2]) )
    for i in range(0,8):
        powerArray.append( mean(power_density(data2)[2]) )
    for i in range(0,8):
        powerArray.append( mean(power_density(data3)[2]) )

    htcArray = []
    first = htc_point(data1)
    print first
    for i in range(0,8):
        htcArray.append( first[i] )
    print "Part 1: Done"
    print " "

    second = htc_point(data2)
    print second
    for i in range(0,8):
        htcArray.append( second[i] )
    print "Part 2: Done"
    print " "

    third = htc_point(data3)
    print third
    for i in range(0,8):
        htcArray.append( third[i] )
    print "Part 3: Done"
    print " "

    colors = ["#0000FF", "#33CC33", "#FF9933", "#FF0000"]
    for j in range(0, 3):
        for i in range(0, 4):
            top = plt.scatter(powerArray[(8*j)+i], htcArray[(8*j)+i], marker="^", c = colors[i], s=50)
        for i in range(4, 8):
            bot = plt.scatter(powerArray[(8*j)+i], htcArray[(8*j)+i], marker="s", c = colors[i-4], s=50)

    plt.legend((top, bot), ["Top Strips", "Bot Strips"], scatterpoints=1)
    plt.grid()
    plt.xlabel("Power Density ( W/cm2 )", fontsize = 16)
    plt.ylabel("HTC ( W/(m"u'\u00B2'"K) )", fontsize = 16)
    plt.show()
