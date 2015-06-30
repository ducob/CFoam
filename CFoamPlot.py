import matplotlib.pyplot as plt
import scipy
import os.path
import matplotlib.dates as mdates
import time
import datetime
import matplotlib.ticker as mticker
from CFoamFunctions import * #Library containing CFoam related analysis functions
from copy import deepcopy #To copy data sets so variables instead of making references to

execfile('CFoamMap.py')

##########################################################################################
### RANGE FUNCTION
##########################################################################################
def min_max(listOfLists, firstList, lastList):
    returnList=[]
    maxVal = 0
    for i in range(firstList,lastList):
        if  max(listOfLists[i]) > maxVal:
            maxVal = max(listOfLists[i])
    returnList.append(maxVal)

    minVal = maxVal
    for i in range(firstList,lastList):
        if min(listOfLists[i]) < minVal:
            minVal = min(listOfLists[i])
    returnList.append(minVal)

    return returnList

def temp_plot (Temp, wallstreet = True):
    _fontsize = 10
    if len(Temp) != 17:
        Adc, Ps, Temp = Temp
    
    ########## INITIALISE PLOT AND ADD DATA ##########

    fig = plt.figure()

    ax1 = fig.add_subplot(3, 1, 1)
    top_names = ["S4_LC", "S4", "S3", "S2", "S1", "S1_RC"]
    top_colors = [ "#FF00FF", "#FF0000", "#FF9933", "#33CC33", "#0000FF", "#00DEFF" ]
    for i in range(1,7):
        ax1.plot(Temp[0], Temp[i], color = top_colors[i-1], label=top_names[i-1])



    ########## TOP TITLE ##########
    #ax1.set_title("Top Cu Temperature", fontsize=_fontsize, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = _fontsize)
    ########## AXIS INFO ##########
    for tick in ax1.xaxis.get_ticklabels():
        tick.set_fontsize(_fontsize)
    for tick in ax1.yaxis.get_ticklabels():
        tick.set_fontsize(_fontsize)
    if wallstreet == False: ax1.set_yticks(scipy.arange(min_max(Temp, 1, 7)[1]-2, min_max(Temp, 1, 7)[0]+2, 0.5))
    plt.legend(fontsize= 0.5*_fontsize, title='LEGEND')
    plt.grid()

    ax2 = fig.add_subplot(3, 1, 2)
    bot_names = ["S5_RC", "S5", "S6", "S7", "S8", "S8_LC"]
    bot_colors = [ "#00DEFF", "#0000FF", "#33CC33", "#FF9933", "#FF0000", "#FF00FF" ]
    for i in range(7,13):
        ax2.plot(Temp[0], Temp[i], color = bot_colors[i-7], label=bot_names[i-7])

    ########## BOTTOM TITLE ##########
    #ax2.set_title("Bottom Cu Temperature", fontsize=_fontsize, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = _fontsize)
    ########## AXIS INFO ##########
    for tick in ax2.xaxis.get_ticklabels():
        tick.set_fontsize(_fontsize)
    for tick in ax2.yaxis.get_ticklabels():
        tick.set_fontsize(_fontsize)
    if wallstreet == False: ax2.set_yticks(scipy.arange(min_max(Temp, 7, 13)[1]-2, min_max(Temp, 7, 13)[0]+2, 0.5))
    plt.legend(fontsize= 0.5*_fontsize, title='LEGEND')
    plt.grid()

    ax3 = fig.add_subplot(3, 1, 3)
    gas_names = ["gas In", "gas Out", "Box", "Lab"]
    for i in range(13,17):
        ax3.plot(Temp[0], Temp[i], label=gas_names[i-13])

    ########## AMBIENT AND GAS TITLE ##########
    #ax3.set_title("Gas and Ambient CFoam Temperature", fontsize=_fontsize, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = _fontsize)
    plt.xlabel("Time (s)", fontsize = _fontsize)
    ########## AXIS INFO ##########
    for tick in ax3.xaxis.get_ticklabels():
        tick.set_fontsize(_fontsize)
    for tick in ax3.yaxis.get_ticklabels():
        tick.set_fontsize(_fontsize)
    if wallstreet == False: ax3.set_yticks(scipy.arange(min_max(Temp, 13, 17)[1]-2, min_max(Temp, 13, 17)[0]+2, 0.5))
    plt.legend(fontsize= 0.5*_fontsize, title='LEGEND')
    plt.grid()

    i += 1
    ######### DISPLAY ##########
    plt.savefig('Output/temp_plots/plot.pdf', format='pdf', bbox_inches='tight', dpi = 2400)
    plt.show()
    

### SHOWS THE FIRST 4 STRIPS
def temp_plot2 (Temp, wallstreet = True):
    if len(Temp) != 17:
        Adc, Ps, Temp = Temp
    
    ########## INITIALISE PLOT AND ADD DATA ##########

    fig = plt.figure()

    ax1 = fig.add_subplot(1, 1, 1)
    top_names = ["S4_LC", "S4", "S3", "S2", "S1", "S1_RC"]
    top_colors = [ "#FF00FF", "#FF0000", "#FF9933", "#33CC33", "#0000FF", "#00DEFF" ]
    for i in range(1,7):
        ax1.plot(Temp[0], Temp[i], color = top_colors[i-1], label=top_names[i-1])
    ########## TOP TITLE ##########
    ax1.set_title("Top Cu Temperature", fontsize=14, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = 16)
    plt.xlabel('Time (s)', fontsize=16)
    plt.grid()
    ######### DISPLAY ##########
    plt.savefig('Output/temp_plots/plot.pdf', format='pdf', bbox_inches='tight', dpi = 2400)
    plt.show()    

def adc_plot ( Temp ):
    ########## INITIALISE PLOT AND ADD DATA ##########
    fig = plt.figure()

    ax1 = fig.add_subplot(3, 1, 1)
    top_names = ["S1", "S2", "S3", "S4"]
    for i in range(1,5):
        ax1.plot(Temp[0], Temp[i], label=top_names[i-1])

    ########## TOP TITLE ##########
    ax1.set_title("Top Voltage", fontsize=14, color='black')
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
    bot_names = ["S5", "S6", "S7", "S8"]
    for i in range(5,9):
        ax2.plot(Temp[0], Temp[i], label=bot_names[i-5])

    ########## BOTTOM TITLE ##########
    ax2.set_title("Bottom Voltage", fontsize=14, color='black')
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
    p_names = ["DP"]
    for i in range(9,10):
        ax3.plot(Temp[0], Temp[i], label=p_names[i-9])

    ########## Differential Pressure Title ##########
    ax3.set_title("Differential Pressure", fontsize=14, color='black')
    plt.ylabel("Delta P (mbar)", fontsize = 16)
    plt.xlabel("Time (s)", fontsize = 16)
    ########## AXIS INFO ##########
    for tick in ax3.xaxis.get_ticklabels():
        tick.set_fontsize(16)
    for tick in ax3.yaxis.get_ticklabels():
        tick.set_fontsize(16)
        ax3.set_yticks(scipy.arange(min_max(Temp, 9, 10)[1]-0.05, min_max(Temp, 9, 10)[0]+0.1,0.1))

    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()


    ########## DISPLAY ##########
    plt.show()

def ps_plot ( Temp ):
    ########## INITIALISE PLOT AND ADD DATA ##########
    fig = plt.figure()

    ax1 = fig.add_subplot(2, 1, 1)
    vol_names = ["Top", "","", "Bottom"]
    for i in {2, 5}:
        ax1.plot(Temp[0], Temp[i], label=vol_names[i-2])

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
    cur_names = ["Top", "","", "Bottom"]
    for i in {3,6}:
        ax2.plot(Temp[0], Temp[i], label=cur_names[i-3])

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

def temp_plot_jan (Temp):
    if len(Temp) != 17:
        Adc, Ps, Temp = Temp
    ########## INITIALISE PLOT AND ADD DATA ##########
    _fontsize = 16.
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title('Temperature Diagram', fontsize = _fontsize)
    plt.ylabel('Temperature ('u'\u00B0''C)', fontsize = _fontsize)
    plt.xlabel('Time (s)', fontsize= _fontsize)
    ax1.plot(Temp[0][:500], Temp[str4][:500], color = 'magenta', label='strip 4', lw=2)
    ax1.plot(Temp[0][:500], Temp[str1][:500], color = 'navy', label='strip 1', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasIn][:500], color = 'green', label='Gas In', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasOut][:500], color = 'crimson', label='Gas Out', lw=2)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()
    plt.savefig('Output/temp_plots/Jan_STR1_STR4_GasIn_GasOut.pdf', format='pdf', dpi=2400)

    Temp = correct_for(Temp, gasIn)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title('Temperature Diagram', fontsize = _fontsize)
    plt.ylabel('Temperature ('u'\u00B0''C)', fontsize = _fontsize)
    plt.xlabel('Time (s)', fontsize= _fontsize)
    ax1.plot(Temp[0][:500], Temp[str4][:500], color = 'magenta', label='strip 4', lw=2)
    ax1.plot(Temp[0][:500], Temp[str1][:500], color = 'navy', label='strip 1', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasIn][:500], color = 'green', label='Gas In', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasOut][:500], color = 'crimson', label='Gas Out', lw=2)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()
    plt.savefig('Output/temp_plots/Jan_STR1_STR4_GasIn_GasOut_CORRECTED.pdf', format='pdf', dpi=2400)
    
def simple_plot ( xarray, yarray ):
    ########## INITIALISE PLOT AND ADD DATA ##########
    fig = plt.figure()

    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(xarray, yarray)
    plt.grid
    plt.show()

##########################################################################################
##### Plots GasIn(triangle), GasOut(square), avg copper(cirlce) and lab(cross) temperature, aswell as their lab environment corrected values  ####
def gas_comparisson( data1, data2, data3 ):
    i = int(16000 / step_size(data1)[0])

    ##########################################################################################

    tGasIn = [data1[2][gasIn][i], data1[2][gasIn][i], data1[2][gasIn][i]]
    tGasInCor = [[data1[2][13][i] - data1[2][16][i], data2[2][13][i] - data2[2][16][i], data3[2][13][i] - data3[2][13][i]]]
    tGasOut = [data1[2][14][i], data2[2][14][i], data3[2][14][i]]
    tGasOutCor = [data1[2][14][i] - data1[2][16][i], data2[2][14][i] - data2[2][16][i], data3[2][14][i] - data3[2][16][i]]
    meanCu = [avg_temp(data1)[2][i], avg_temp(data2)[2][i], avg_temp(data3)[2][i]]
    Lab = [data1[2][16][i], data2[2][16][i], data3[2][16][i]]

    ##########################################################################################

    pdArray = [mean(power_density(data1)[2]), mean(power_density(data2)[2]), mean(power_density(data3)[2])]

    gi = plt.scatter(pdArray, tGasIn, marker = "^", s=60)
    go = plt.scatter(pdArray, tGasOut, marker = "s", s=60)
    mcu = plt.scatter(pdArray, meanCu, marker = "o", s=60)
    labe = plt.scatter(pdArray, Lab, marker = "x", s=60)
    plt.legend((gi, go, mcu, labe), ["Gas In", "Gas Out", "Mean Cu", "Lab"], scatterpoints=1)
    plt.grid()
    plt.xlabel("Power Density ( W/cm2 )", fontsize = 16)
    plt.ylabel("Temperature ( "u'\u00b0'"C )", fontsize = 16)
    plt.show()

    gic = plt.scatter(pdArray, tGasInCor, marker = "^", s=60)
    goc = plt.scatter(pdArray, tGasOutCor, marker = "s", s=60)
    plt.legend((gic, goc), ["Gas In cor", "Gas Out cor"], scatterpoints=1)
    plt.grid()
    plt.xlabel("Power Density ( W/cm2 )", fontsize = 16)
    plt.ylabel(u'\u0394'"T (wrt Lab Environmen) ( "u'\u00b0'"C )", fontsize = 16)
    plt.show()


###### temp_dp_plot, plots temp_plot + the differential pressure #########################
def temp_dp_plot ( data ):
    Adc, Ps, Temp = data

    ########## INITIALISE PLOT AND ADD DATA ##########
    fig = plt.figure()

    ax1 = fig.add_subplot(4, 1, 1)
    top_names = ["S4_LC", "S4", "S3", "S2", "S1", "S1_RC"]
    top_colors = [ "#FF00FF", "#FF0000", "#FF9933", "#33CC33", "#0000FF", "#00DEFF" ]
    for i in range(1,7):
        ax1.plot(Temp[0], Temp[i], color = top_colors[i-1], label=top_names[i-1])

    ########## TOP TITLE ##########
    ax1.set_title("Top Cu Temperature", fontsize=14, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = 16)
    ########## AXIS INFO ##########
    for tick in ax1.xaxis.get_ticklabels():
        tick.set_fontsize(16)
    for tick in ax1.yaxis.get_ticklabels():
        tick.set_fontsize(16)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()

    ax2 = fig.add_subplot(4, 1, 2)
    bot_names = ["S5_RC", "S5", "S6", "S7", "S8", "S8_LC"]
    bot_colors = [ "#00DEFF", "#0000FF", "#33CC33", "#FF9933", "#FF0000", "#FF00FF"  ]
    for i in range(7,13):
        ax2.plot(Temp[0], Temp[i], color = bot_colors[i-7], label=bot_names[i-7])

    ########## BOTTOM TITLE ##########
    ax2.set_title("Bottom Cu Temperature", fontsize=14, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = 16)
    ########## AXIS INFO ##########
    for tick in ax2.xaxis.get_ticklabels():
        tick.set_fontsize(16)
    for tick in ax2.yaxis.get_ticklabels():
        tick.set_fontsize(16)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()

    ax3 = fig.add_subplot(4, 1, 3)
    gas_names = ["gas In", "gas Out", "Box", "Lab"]
    for i in range(13,17):
        ax3.plot(Temp[0], Temp[i], label=gas_names[i-13])

    ########## AMBIENT AND GAS TITLE ##########
    ax3.set_title("Gas and Ambient CFoam Temperature", fontsize=14, color='black')
    plt.ylabel("Temperature (deg C)", fontsize = 16)
    #plt.xlabel("Time (s)", fontsize = 16)
    ########## AXIS INFO ##########
    for tick in ax3.xaxis.get_ticklabels():
        tick.set_fontsize(16)
    for tick in ax3.yaxis.get_ticklabels():
        tick.set_fontsize(16)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()

    ax4 = fig.add_subplot(4, 1, 4)
    p_names = ["DP"]
    for i in range(9,10):
        ax4.plot(Temp[0], Adc[i], label=p_names[i-9])

    ########## Differential Pressure Title ##########
    ax4.set_title("Differential Pressure", fontsize=14, color='black')
    plt.ylabel("Delta P (mbar)", fontsize = 16)
    plt.xlabel("Time (s)", fontsize = 16)
    ########## AXIS INFO ##########
    for tick in ax4.xaxis.get_ticklabels():
        tick.set_fontsize(16)
    for tick in ax4.yaxis.get_ticklabels():
        tick.set_fontsize(16)
        #ax4.set_yticks(scipy.arange(min_max(Adc, 9, 10)[1]-0.05, min_max(Adc, 9, 10)[0]+0.1, 0.5))

    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()

    ######### DISPLAY ##########
    plt.show()

###### temp_comparison, plots temp_plot + the differential pressure #########################
def temp_comparison ( data, ttime ):
    Adc, Ps, Temp = data
    point = int(ttime / step_size(data)[0])

    delT = Temp[gasOut][point] - Temp[gasIn][point]

    ##########################################################################################

    topTemp = [ Temp[str1_RC][point], Temp[str1][point], Temp[str2][point], Temp[str3][point], Temp[str4][point], Temp[str4_LC][point] ]
    botTemp = [ Temp[str5_RC][point], Temp[str5][point], Temp[str6][point], Temp[str7][point], Temp[str8][point], Temp[str8_LC][point] ]
    gasTemp = [ Temp[gasIn][point], Temp[gasOut][point], Temp[boxEnv][point], Temp[labEnv][point] ]
    incrTemp = [ Temp[gasIn][point] + (1./8.)*delT, Temp[gasIn][point] + (3./8.)*delT, Temp[gasIn][point] + (5./8.)*delT, Temp[gasIn][point] + (7./8.)*delT ]

    topXarray = [2 for i in range(6)]
    botXarray = [4 for i in range(6)]
    gasXarray = [8 for i in range(4)]
    incrXarray = [10 for i in range(4)]
    _x_ = [2,4,8,10]
    ##########################################################################################

    cuMarkerlist = ["o", "x", "x", "x", "x", "o"]
    cuColorlist = ["#0000FF", "#0000FF", "#33CC33", "#FF9933", "#FF0000", "#FF0000"]
    cuTopnameList = ["S1", "", "S2", "S3", "", "S4"]
    cuBotnameList = ["S5", "", "S6", "S7", "", "S8"]
    for _x, _y, _m, _c, _n in zip(topXarray, topTemp, cuMarkerlist, cuColorlist, cuTopnameList):
        toptemp = plt.scatter(_x, _y, marker = _m, color = _c, s = 60)
        plt.annotate(_n, (_x,_y))

    for _x, _y, _m, _c, _n in zip(botXarray, botTemp, cuMarkerlist, cuColorlist, cuBotnameList):
        bottemp = plt.scatter(_x, _y, marker = _m, color = _c, s = 60)
        plt.annotate(_n, (_x,_y))

    gasColorlist = ["#0000FF", "#FF0000", "#FF00FF", "#FF00FF"]
    gasNames = ["Gas In", "Gas Out", "Box Env", "Lab Env"]
    for _x, _y, _c, _n in zip(gasXarray, gasTemp, gasColorlist, gasNames):
        gastemp = plt.scatter(_x, _y, marker = "H", color = _c, s = 60)
        plt.annotate(_n, (_x,_y))

    incrColorlist = ["#0000FF", "#33CC33", "#FF9933", "#FF0000"]
    incrNames = ["1/8", "3/8", "5/8", "7/8"]
    for _x, _y, _c, _n in zip(incrXarray, incrTemp, incrColorlist, incrNames):
        incrtemp = plt.scatter(_x, _y, marker = "H", color = _c,  s=60)
        plt.annotate(_n, (_x,_y))

    my_xticks = ["Top", "Bot", "Gas", "Incr"]
    plt.xticks(_x_, my_xticks)
    plt.grid()
    plt.show()

###### temp_comparison, plots temp_plot + the differential pressure #########################
def pd_comparison ( data ):
    adc, ps, temp = data
    pdTop, pdBot = power_density_strip(data)

    PD_top, PD_bot, PD_tot = power_density(data)
    low = mean(PD_tot) - (mean(PD_tot)/2.)
    high = mean(PD_tot) + (mean(PD_tot)/2.)
    ##########################################################################################

    def pd_strips ( i, data ):
        pdTop, pdBot = power_density_strip(data)
        topPD = [ pdTop[0][i], pdTop[1][i], pdTop[2][i], pdTop[3][i] ]
        botPD = [ pdBot[0][i], pdBot[1][i], pdBot[2][i], pdBot[3][i] ]
        return topPD, botPD

    ##########################################################################################

    step_list = [ a for a in range(0, int(max(adc[0])), 1000) ]
    stepsize = step_size(data)[0]

    ##########################################################################################

    for i in step_list:
        topPD, botPD = pd_strips( int(i/stepsize), data )
        for _y in topPD:
            plt.scatter(i, _y, marker = "^", s=50)
        for _y in botPD:
            plt.scatter(i, _y, marker = "s", s=50)

    plt.xlabel("Seconds (S)", fontsize = 16.)
    plt.ylabel("Power Density (W/cm"u'\u00B2'")", fontsize = 16.)
    plt.ylim(low, high)
    plt.xlim(-1000, int(max(adc[0]))+1000)
    plt.xticks(range(0, int(max(adc[0])), 1000))
    plt.grid()
    plt.show()

def dp_time_plot ( data ):
    Adc, Ps, Temp, realTimeArray = data

    fig = plt.figure()
    ax1 = plt.subplot(1,1,1)
    ax1.plot(realTimeArray, Adc[9])

    ymdhFmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(20))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d | %H:%M:%S'))

    for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(30)


    plt.grid()
    plt.show()
    

    
def temp_plot_jan (Temp):
    if len(Temp) != 17:
        Adc, Ps, Temp = Temp
    ########## INITIALISE PLOT AND ADD DATA ##########
    _fontsize = 16.
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title('Temperature Diagram', fontsize = _fontsize)
    plt.ylabel('Temperature ('u'\u00B0''C)', fontsize = _fontsize)
    plt.xlabel('Time (s)', fontsize= _fontsize)
    ax1.plot(Temp[0][:500], Temp[str4][:500], color = 'magenta', label='strip 4', lw=2)
    ax1.plot(Temp[0][:500], Temp[str1][:500], color = 'navy', label='strip 1', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasIn][:500], color = 'green', label='Gas In', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasOut][:500], color = 'crimson', label='Gas Out', lw=2)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()
    plt.savefig('Output/temp_plots/Jan_STR1_STR4_GasIn_GasOut.pdf', format='pdf', dpi=2400)

    Temp = correct_for(Temp, gasIn)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title('Temperature Diagram', fontsize = _fontsize)
    plt.ylabel('Temperature ('u'\u00B0''C)', fontsize = _fontsize)
    plt.xlabel('Time (s)', fontsize= _fontsize)
    ax1.plot(Temp[0][:500], Temp[str4][:500], color = 'magenta', label='strip 4', lw=2)
    ax1.plot(Temp[0][:500], Temp[str1][:500], color = 'navy', label='strip 1', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasIn][:500], color = 'green', label='Gas In', lw=2)
    ax1.plot(Temp[0][:500], Temp[gasOut][:500], color = 'crimson', label='Gas Out', lw=2)
    plt.legend(fontsize= 16, title='LEGEND')
    plt.grid()
    plt.savefig('Output/temp_plots/Jan_STR1_STR4_GasIn_GasOut_CORRECTED.pdf', format='pdf', dpi=2400)