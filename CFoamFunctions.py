from copy import deepcopy #To copy data sets so variables instead of making references to
import time
execfile('CFoamMap.py')
version = '1.0' #Version Info

##########################################################################################
### FUNCTIONS
##########################################################################################

### Return the strip number (string) corresponding to a thermocouple
def strip_name( tcNum ):
    for i in xrange(1,9):
        if tcNum == eval("str"+str(i)):
            return "strip"+str(i)

def avgData(data, correct, point, band):
    adc, ps, temp = data

    if correct != 0:
        corrTemp = correct_for(temp, corr = correct)
    if correct == 0:
        corrTemp = temp

    step = step_size(data)[0]

    #_t = int( fraction*(adc[0][-1]) / step )   #stable point
    _t1 = int( (point - band) * adc[0][-1] / step )
    _t2 = int( (point + band) * adc[0][-1] / step )
    avgAdc = []
    for _p in xrange(0, len(adc)-1):
        avgAdc.append( [] )
    for _p in xrange(0, len(adc)-2):
        avgAdc[_p] = mean_section(adc[_p], _t1, _t2)

    avgPs = []
    _list = {0,2,3,5,6}
    for _p in xrange(0, len(ps)-1):
        avgPs.append( [] )
    for _p in _list:
        avgPs[_p] = mean_section(ps[_p], _t1, _t2)

    avgTemp = []
    for _p in xrange(0, len(corrTemp)):
        avgTemp.append( [] )
    for _p in xrange(0, len(corrTemp)):
        avgTemp[_p] = mean_section(corrTemp[_p], _t1, _t2)

    return avgAdc, avgPs, avgTemp

##########################################################################################
### MATH FUNC
##########################################################################################
def sum(list):
    sum = 0
    for i in range(0, len(list)):
        sum = sum + list[i]
    return sum

def mean(list):
    sum = 0
    for i in range(0, len(list)):
        sum = sum + list[i]
    return sum / len(list)

def mean_section(list, a, b):
    sum = 0
    for i in range(a, b):
        sum = sum + list[i]
    return sum / (b-a)

def variance(list):
    average = mean(list)
    variance = 0
    for i in list:
        variance = variance + ((average - i)**2)
    if len(list) == 1:
        return 0
    else:
        return variance / (len(list) - 1.)

def std_deviation(list):
    return variance(list) ** 0.5

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def RMS (list, baseline):
    n = float( len(list) )
    _squareSum = 0
    for item in list:
        _squareSum += pow(item - baseline,2)
    rms = pow(_squareSum / (n-1), 0.5)
    #print rms
    return rms
    
##########################################################################################
### CFOAM Constants
##########################################################################################
A = 18.73
R_probe_i = [5., 5., 5., 5., 5., 5., 5., 5.]
R_strip_j = [15., 15., 15., 15., 15., 15., 15., 15.]
R_probe_top = [5., 5., 5., 5.]
R_strip_top = [15., 15., 15., 15.]
R_probe_bot = [5., 5., 5., 5.]
R_strip_bot = [15., 15., 15., 15.]

##########################################################################################
###CFOAM FUNC
##########################################################################################

##########################################################################################
### power_correction returns the leaked power as a function of the lab corrected sample temperature
def power_correction(temperature):
    slope = 0.1012 #corrected for lab
    intercept = -0.0142
    
    return slope*temperature + intercept
##########################################################################################


##########################################################################################
### Returns the power per strip, top and bot and both sides per time step
def power ( data ):
    Adc, Ps, Temp = data    #Refering to data parts

    pStripTop = [[] for x in xrange(4)]   #Initialise lists
    pStripBot = [[] for x in xrange(4)]
    pTop = []
    pBot = []
    pTot = []
    pTopStep = 0
    pBotStep = 0

    #Fill strip lists according to model
    for i in range(0,4):    #Loop over strips (1 - 4) and (1+4 - 4+4)
        for j in range(0, len(Adc[0])): #Loop over time steps
            pStripTop[i].append( pow(Adc[i+1][j]/R_probe_top[i], 2)*R_strip_top[i]) #strip 1 -> 4
            pStripBot[i].append( pow(Adc[i+5][j]/R_probe_bot[i], 2)*R_strip_bot[i]) #strip 5 -> 8


    #Total power on the top, bottom and both per time step
    for i in range(0, len(Adc[0])): #Fill top, bot and tot lists
        for j in range(0, 4):
            pTopStep += pStripTop[j][i]
            pBotStep += pStripBot[j][i]
        pTop.append(pTopStep)
        pBot.append(pBotStep)
        pTot.append(pTopStep + pBotStep)
        pTopStep = 0
        pBotStep = 0

    return pStripTop, pStripBot, pTop, pBot, pTot
##########################################################################################

##########################################################################################
### power_ps, returns the power delivered by the power supply ###
def power_ps( data ):
    Adc, Ps, Temp = data
    pTop = []
    pBot = []
    pTot = []

    for i in range(0, len(Adc[0])):
        pTop.append(Ps[topVoltage][i]*Ps[topCurrent][i])
        pBot.append(Ps[botVoltage][i]*Ps[botCurrent][i])
        pTot.append(pTop[i] + pBot[i])

    return pTop, pBot, pTot
##########################################################################################

##########################################################################################
### power_density, returns the power density of the 8 strips ###
def power_density( data ):
    Adc, Ps, Temp = data
    pStripTop, pStripBot, pTop, pBot, pTot = power(data)

    pdTop = []
    pdBot = []
    pdTot = []
    for i in range(0, len(pTop)):
        pdTop.append(pTop[i]/(4.*A))
        pdBot.append(pBot[i]/(4.*A))
        pdTot.append( (pTop[i]+pBot[i])/(8.*A) )

    return pdTop, pdBot, pdTot
##########################################################################################

##########################################################################################
def power_density_strip ( data ):
    Adc, Ps, Temp = data
    pStripTop, pStripBot, pTop, pBot, pTot = power(data)

    topStripPd = [[] for x in xrange(4)]
    botStripPd = [[] for x in xrange(4)]
    for i in range(0, 4):
        for j in range(0, len(Adc[0])):
            topStripPd[i].append( pStripTop[i][j]/A )
            botStripPd[i].append( pStripBot[i][j]/A )
    return topStripPd, botStripPd
##########################################################################################

##########################################################################################
### Power_print, prints the power and power density of the 8 strips ###
def power_print ( data ):
    Adc, Ps, Temp = data
    pStripTop, pStripBot, pTop, pBot, pTot = power(data)

    # Fill and Print out of Power per strip (calculated with voltage probe data)
    print " "
    print "-------------"
    print " "
    for i in range(0,4):
        print "Power in strip", i+1, ": ", mean(pStripTop[i]), " W"
    for i in range(0,4):
        print "Power in strip", i+5, ": ", mean(pStripBot[i]), " W"
    print "===="

    # Calculation of total power and Print Out
    total_pow = mean(pTop) + mean(pBot)
    print "Total power on top: ", mean(pTop), " W"
    print "Total power on bottom: ", mean(pBot), " W"
    print "Total power on CFOAM device: ", total_pow, " W"
    print "Total power by PS: ", mean(Ps[2])*mean(Ps[3]) + mean(Ps[5])*mean(Ps[6])
    print " "
    print "-------------"
    print " "

    pdTop = mean(pTop)/(4.*A)
    pdBot = mean(pBot)/(4.*A)
    pdAvg = (pdTop + pdBot)/2.
    # Power density calculation
    for i in range(0,4):
        print "Power density in strip", i+1, ": ", mean(pStripTop[i])/A, " W/cm2"
    for i in range(0,4):
        print "Power density in strip", i+5, ": ", mean(pStripBot[i])/A, " W/cm2"
    print "===="
    print "Power density on top: ", pdTop, " W/cm2"
    print "Power density on bottom: ", pdBot, " W/cm2"
    print "Average power density on CFOAM device: ", pdAvg, " W/cm2"
    print ""
    print "-------------"
    print ""
    return None
##########################################################################################

##########################################################################################
def avg_temp ( Temp ):

    tTopAvg = []
    tBotAvg = []
    tAvg = []
    for i in range(0, len(Temp[0])):
        tTopAvg.append( (Temp[1][i] + Temp[2][i] + Temp[3][i] + Temp[4][i] + Temp[5][i] + Temp[6][i])/6. )
        tBotAvg.append( (Temp[7][i] + Temp[8][i] + Temp[9][i] + Temp[10][i] + Temp[11][i] + Temp[12][i])/6. )
        tAvg.append( (tTopAvg[i] + tBotAvg[i]) / 2. )

    return tTopAvg, tBotAvg, tAvg
##########################################################################################

##########################################################################################
def flow_func(power, foamTemperature, gasIn, gasOut):
    rho_gas = 1.1839        #in g/L @ 25 deg C
    c_v_gas = 1.012         #in J/(g*K)
    deltaT = gasOut - gasIn

    LPS = (power - power_correction(foamTemperature))/(rho_gas * c_v_gas * deltaT)    #Litre per second
    LPM = LPS * 60  #Litre per minute
    return LPM
##########################################################################################

##########################################################################################
def flow( data ):
    Adc, Ps, Temp = data
    pStripTop, pStripBot, pTop, pBot, pTot = power(data)
    tTopAvg, tBotAvg, tAvg = avg_temp(data)


    flowI = []
    for i in range(0, len(Temp[0])):
        flowI.append( flow_func(pTot[i], tAvg[i]-Temp[labEnv][i], Temp[gasIn][i], Temp[gasOut][i]) )
    return flowI
##########################################################################################

##########################################################################################
### step_size, returns the increments of the array for all steps ###
def step_size( data ):
    Adc, Ps, Temp = data
    stepSize = []
    for i in range(0, len(Temp[0])-1):
        stepSize.append(Temp[0][i+1] - Temp[0][i])
    return stepSize
##########################################################################################

##########################################################################################
### step_size, changes the values of the temperature array for all steps  ###
def correct_for ( Temp, corr = 13 ):
    tempRaw = deepcopy(Temp)
    temp = deepcopy(Temp)

    for j in range(1, 17):
        for i in range(0, len(temp[0])):
            temp[j][i] = tempRaw[j][i] - tempRaw[corr][i]
    #print "Corrected for thermocouple:", corr
    return temp
##########################################################################################

##########################################################################################
### htc_point, returns the htc of a data set for all strips calculated at one sample point ###
### units are in W(cm^-2K^-1) [multiply by 10^4 to obtain W(m^-2K^-1)]  ###
def avgHtcFunction(data, correct, fraction, band):
    adc, ps, temp = avgData(data, correct, fraction, band)
    delTgas = temp[gasOut] - temp[gasIn]
    gasInTemp = temp[gasIn]

    areaStrip = 2.15 * 8.71         #strip area
    #areaTotal = 2 * (9.71 * 10.2)   #total cfoam area
    areaTotal = 8 * areaStrip
    
    powerCorrection = power_correction( mean_section(temp, 1, 13) )
    powerCorrectionFactor = (areaStrip/areaTotal) * powerCorrection #heat leak per strip. Area comparison used.

    HTC = []
    for strip in (str1, str2, str3, str4, str5, str6, str7, str8):
        if strip == str1:
            delT = temp[strip] - ((1./8.)*delTgas + gasInTemp)     #difference strip temp and increments of delta T gas
            powerStrip = pow(adc[1]/5., 2)*15.
        if strip == str2:
            delT = temp[strip] - ((3./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[2]/5., 2)*15.
        if strip == str3:
            delT = temp[strip] - ((5./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[3]/5., 2)*15.
        if strip == str4:
            delT = temp[strip] - ((7./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[4]/5., 2)*15.

        if strip == str5:
            delT = temp[strip] - ((1./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[5]/5., 2)*15.
        if strip == str6:
            delT = temp[strip] - ((3./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[6]/5., 2)*15.
        if strip == str7:
            delT = temp[strip] - ((5./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[7]/5., 2)*15.
        if strip == str8:
            delT = temp[strip] - ((7./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[8]/5., 2)*15.

        powerGas = powerStrip - powerCorrectionFactor
        HTC.append( powerGas / (areaStrip*delT) )
    return HTC
##########################################################################################

##########################################################################################
### htc_point, returns the htc of a data set for all strips calculated at one sample point ###
### units are in W(cm^-2K^-1) [multiply by 10^4 to obtain W(m^-2K^-1)]  ###
### DIFFERS FROM avgHtcFunction, BY CALCULATING THE HEAT LEAK PER STRIP
def avgHtcFunction2(data, correct, fraction, band):
    adc, ps, temp = avgData(data, correct, fraction, band)
    delTgas = temp[gasOut] - temp[gasIn]
    gasInTemp = temp[gasIn]

    areaStrip = 2.15 * 8.71         #strip area
    #areaTotal = 2 * (9.71 * 10.2)   #total cfoam area
    areaTotal = 8 * areaStrip
    
    #powerCorrection = power_correction( mean_section(temp, 1, 13) )
    #powerCorrectionFactor = (areaStrip/areaTotal) * powerCorrection #heat leak per strip. Area comparison used.

    HTC = []
    for strip in (str1, str2, str3, str4, str5, str6, str7, str8):
        if strip == str1:
            delT = temp[strip] - ((1./8.)*delTgas + gasInTemp)     #difference strip temp and increments of delta T gas
            powerStrip = pow(adc[1]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )
        if strip == str2:
            delT = temp[strip] - ((3./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[2]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )
        if strip == str3:
            delT = temp[strip] - ((5./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[3]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )
        if strip == str4:
            delT = temp[strip] - ((7./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[4]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )

        if strip == str5:
            delT = temp[strip] - ((1./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[5]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )
        if strip == str6:
            delT = temp[strip] - ((3./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[6]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )
        if strip == str7:
            delT = temp[strip] - ((5./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[7]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )
        if strip == str8:
            delT = temp[strip] - ((7./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[8]/5., 2)*15.
            powerCorrectionFactor = (1./8.)*power_correction( temp[strip] )

        powerGas = powerStrip - powerCorrectionFactor
        HTC.append( powerGas / (areaStrip*delT) )
    return HTC
##########################################################################################

### htc_point, returns the htc of a data set for all strips calculated at one sample point ###
### units are in W(cm^-2K^-1) [multiply by 10^4 to obtain W(m^-2K^-1)]  ###
### DIFFERS FROM avgHtcFunction, BY TAKING THE TEMPERATURE DROP IN THE KAPTON AND GLUE 
### INTO ACCOUNT
def avgHtcFunction3(data, correct, fraction, band):
    adc, ps, temp = avgData(data, correct, fraction, band)
    delTgas = temp[gasOut] - temp[gasIn]
    gasInTemp = temp[gasIn]

    areaStrip = 2.15 * 8.71         #strip area
    #areaTotal = 2 * (9.71 * 10.2)   #total cfoam area
    areaTotal = 8 * areaStrip
    
    powerCorrection = power_correction( mean_section(temp, 1, 13) )
    powerCorrectionFactor = (areaStrip/areaTotal) * powerCorrection #heat leak per strip. Area comparison used.

    def tempDrop(powerStrip):
        drop = (powerStrip/18.73e-4)*( (60e-6/0.22) + (20e-6/0.46) )
        return drop

    HTC = []
    for strip in (str1, str2, str3, str4, str5, str6, str7, str8):
        if strip == str1:
            delT = temp[strip] - ((1./8.)*delTgas + gasInTemp)     #difference strip temp and increments of delta T gas
            powerStrip = pow(adc[1]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)
        if strip == str2:
            delT = temp[strip] - ((3./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[2]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)
        if strip == str3:
            delT = temp[strip] - ((5./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[3]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)
        if strip == str4:
            delT = temp[strip] - ((7./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[4]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)

        if strip == str5:
            delT = temp[strip] - ((1./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[5]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)
        if strip == str6:
            delT = temp[strip] - ((3./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[6]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)
        if strip == str7:
            delT = temp[strip] - ((5./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[7]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)
        if strip == str8:
            delT = temp[strip] - ((7./8.)*delTgas + gasInTemp)
            powerStrip = pow(adc[8]/5., 2)*15.
            delT = delT - tempDrop(powerStrip)

        powerGas = powerStrip - powerCorrectionFactor
        HTC.append( powerGas / (areaStrip*delT) )
    return HTC
##########################################################################################

def avgTaboveGas(data, correct, fraction, band):
    adc, ps, temp = avgData(data, correct, fraction, band)
    delTgas = temp[gasOut] - temp[gasIn]
    gasInTemp = temp[gasIn]
 
    avgTabove = []
    for strip in (str1, str2, str3, str4, str5, str6, str7, str8):
        if strip == str1:
            delT = temp[strip] - gasInTemp     #difference strip temp and increments of delta T gas
        if strip == str2:
            delT = temp[strip] - gasInTemp
  
        if strip == str3:
            delT = temp[strip] - gasInTemp
        if strip == str4:
            delT = temp[strip] - gasInTemp

        if strip == str5:
            delT = temp[strip] - gasInTemp
        if strip == str6:
            delT = temp[strip] - gasInTemp
        if strip == str7:
            delT = temp[strip] - gasInTemp
        if strip == str8:
            delT = temp[strip] - gasInTemp
        
        avgTabove.append(delT)
            
    return avgTabove


##########################################################################################
### stable_temperature, returns the average temperature of all strips over a specific time range ###
### Standard temperature is normalised with respect to the lab temperature and averaged over 0.8 and 0.9* total length ###
def stable_temperature(data, correction = True, startprcnt = 0.8, endprcnt = 0.9):
    adc, ps, temp = data
    stepSize = step_size(data)[0]
    length = len(data[TEMP][0])
    start = int(startprcnt * length)
    end = int(endprcnt * length)

    if correction == True: temp = correct_for(temp, labEnv)

    cuTemp = 0
    for i in range(1,13):
        cuTemp += mean_section(temp[i], start, end)

    return cuTemp/12.
##########################################################################################
