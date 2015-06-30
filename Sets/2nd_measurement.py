##########################################################################################

from ExtractData import * #Import function to extract and organise data from the raw files
from CFoamPlot import * #Library containing CFoam plot functions
from CFoamFunctions import * #Library containing CFoam analysis functions
from scipy.optimize import curve_fit
import numpy as np

##########################################################################################

data30LPM0_01225wcm2 = import_data("06_05_2015", "11_42_56", "30lpm")   #0.01225
data30LPM0_0245wcm2 = import_data("06_05_2015", "17_07_26", "30lpm")    #0.0245
data30LPM0_049wcm2 = import_data("06_05_2015", "23_30_46", "30lpm")     #0.049
data30LPM0_049wcm2 = import_data("07_05_2015", "08_45_26", "30lpm")     #0.049
data30LPM0_098wcm2 = import_data("07_05_2015", "15_15_06", "30lpm")     #0.098

##########################################################################################
#threeDayPressureData = import_data("08_05_2015", "14_46_20", "pressure_stable", timeBool = True)
##########################################################################################

data35LPM0_0245wcm2 = import_data("03_06_2015", "14_42_42", "35lpm")    #0.0245
data35LPM0_049wcm2 = import_data("03_06_2015", "15_26_44", "35lpm")     #0.0490
data35LPM0_098wcm2 = import_data("03_06_2015", "16_12_52", "35lpm")     #0.0980

##########################################################################################

data40LPM0_0245wcm2 = import_data("03_06_2015", "10_33_27", "40lpm")    #0.0245
data40LPM0_049wcm2 = import_data("03_06_2015", "11_48_51", "40lpm")     #0.0490
data40LPM0_098wcm2 = import_data("03_06_2015", "12_42_14", "40lpm")     #0.0980

##########################################################################################

data45LPM0_0245wcm2 = import_data("04_06_2015", "13_13_16", "45lpm")    #0.0245
data45LPM0_049wcm2 = import_data("04_06_2015", "14_04_29", "45lpm")     #0.0490
data45LPM0_098wcm2 = import_data("04_06_2015", "14_55_07", "45lpm")     #0.0980

##########################################################################################

data50LPM0_0245wcm2 = import_data("12_05_2015", "12_30_39", "50lpm")    #0.0245
data50LPM0_049wcm2 = import_data("13_05_2015", "14_10_45", "50lpm")     #0.0490
data50LPM0_098wcm2 = import_data("18_05_2015", "11_16_44", "50lpm")     #0.0980

##########################################################################################

data55LPM0_0245wcm2 = import_data("04_06_2015", "09_44_14", "55lpm")    #0.0245
data55LPM0_049wcm2 = import_data("04_06_2015", "10_27_17", "55lpm")     #0.0490
data55LPM0_098wcm2 = import_data("04_06_2015", "11_38_16", "55lpm")     #0.0980

##########################################################################################

data60LPM0_0245wcm2 = import_data("20_05_2015", "09_53_38", "60lpm")    #0.0245
data60LPM0_049wcm2 = import_data("20_05_2015", "14_54_15", "60lpm")     #0.0490
data60LPM0_098wcm2 = import_data("22_05_2015", "09_45_09", "60lpm")     #0.0980

##########################################################################################
### settings

##########################################################################################

flows = [30, 35, 40, 45, 50, 55, 60]
powerDensities = [0.0245, 0.0490, 0.0980]
fraction = 0.8
window = 0.1
_corr = labEnv

##########################################################################################

for _flow in flows:
    for _pd in powerDensities:
        _flow = str(_flow)
        _pd = str(_pd).replace('.','_')
        
        globals()['htc%sLPM%swcm2' % (_flow, _pd)] = avgHtcFunction(eval('data%sLPM%swcm2' % (_flow, _pd)), _corr, fraction, window )
        #globals()['htc%sLPM%swcm2_2' % (_flow, _pd)] = avgHtcFunction2(eval('data%sLPM%swcm2' % (_flow, _pd)), _corr, fraction, window )
        globals()['htc%sLPM%swcm2_3' % (_flow, _pd)] = avgHtcFunction3(eval('data%sLPM%swcm2' % (_flow, _pd)), _corr, fraction, window )
        
        _mean = mean( eval('htc%sLPM%swcm2' % (_flow, _pd)) )
        globals()['meanHTC%sLPM%scm2' % (_flow, _pd)] = _mean
        #_mean2 = mean( eval('htc%sLPM%swcm2_2' % (_flow, _pd)) )
        #globals()['meanHTC%sLPM%scm2_2' % (_flow, _pd)] = _mean2
        #_mean3 = mean( eval('htc%sLPM%swcm2_3' % (_flow, _pd)) )
        #globals()['meanHTC%sLPM%scm2_3' % (_flow, _pd)] = _mean3
        
        globals()['errorMeanHTC%sLPM%scm2' % (_flow, _pd)] = RMS( eval('htc%sLPM%swcm2' % (_flow, _pd)), _mean )
        
        print '%sLPM%swcm2\tprocessed to\thtc%sLPM%swcm2' %(_flow, _pd, _flow, _pd)
        print '\tMean stored in meanHTC%sLPM%scm2 = %s' %(_flow, _pd, round(_mean, 4))
        #print '\tCorrected Mean stored in meanHTC%sLPM%scm2_3 = %s' %(_flow, _pd, round(_mean3, 4))
        print '\t Error on the mean (RMS) = %s \n' % eval('errorMeanHTC%sLPM%scm2' % (_flow, _pd))
            
##########################################################################################

def htcSpreadSheet ( flows, powerDensities, fileName ):
    outputName = 'Output/htc/'+fileName
    file=open(outputName, 'w')

    file.write('Heat Transfer Coefficient Data\n')
    file.write('\n')

    file.write('Strip Area\t %s \t cm2\n' % A)
    file.write('Power Correction Slope \t %s \t W/deg C(lab)\n' % 0.1022)
    file.write('\n')

    file.write('Case \t Flow \t Strip Power \t \t \t \t Power Correction \t Temperatures \t \t \t \t T_lab \t T_gasIn \t T_gasOut \t Delta T \t HTC \t \t \t \t Mean HTC \t Error on HTC\n')

    for _flow in flows:
        for _pd in powerDensities:
            _flow = str(_flow)
            _pd = str(_pd).replace('.','_')
            HTC = eval('htc%sLPM%swcm2' %(_flow, _pd))
            ADC, PS, TEMP = avgData(eval('data%sLPM%swcm2'%(_flow,_pd)), 0, fraction, window)
            adc, ps, temp = avgData(eval('data%sLPM%swcm2'%(_flow,_pd)), labEnv, fraction, window)
        
            file.write('%sLPM@%s\t' %(_flow, _pd))
            file.write('%s \t' % _flow)
            
            pc = power_correction( mean_section(temp, 1, 13) )
            htcError = eval('errorMeanHTC%sLPM%scm2' % (_flow, _pd))
            print htcError
            
            for i in xrange(1,9):
                globals()['p%s' % i] = pow(adc[i]/5., 2)*15.
            
            file.write('%s \t %s \t %s \t %s \t %s \t' % (p1, p2, p3, p4, pc) )
        
            file.write('%s \t %s \t %s \t %s \t' % (temp[str1], temp[str2], temp[str3], temp[str4]) )
            file.write('%s \t %s \t %s \t %s \t' % (TEMP[labEnv], temp[gasIn], temp[gasOut], temp[gasOut]-temp[gasIn]) )
            file.write('%s \t %s \t %s \t %s \t %s \t %s \n' % (HTC[0], HTC[1], HTC[2], HTC[3], mean(HTC), htcError) )
        
            file.write('\t \t %s \t %s \t %s \t %s \t \t' % (p5, p6, p7, p8) )
            file.write('%s \t %s \t %s \t %s \t' % (temp[str5], temp[str6], temp[str7], temp[str8]) )
            file.write('\t \t \t \t %s \t %s \t %s \t %s \t \n' % (HTC[4], HTC[5], HTC[6], HTC[7]))
            file.write('\n')
            print 'htc%sLPM%swcm2\twritten to file' %(_flow, _pd)

    print 'Writing spreadsheet: %s to %s done.\n' %(fileName, outputName)
    file.close()

htcSpreadSheet(flows, powerDensities, 'RMS2_Heat_Transfer_Coefficient_corrected_for_tc_%s.txt'%str(_corr))

##########################################################################################

def HTCplots( fileName1, fileName2 ):
    _fontsize = 10.
    _dpi = 2400
    
################## Plot 1
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    title = plt.title('HTC Measurement', fontsize = 1.2*_fontsize, y=1.08)
    ax1.set_xlabel('Flow of Air (LPM)', fontsize = _fontsize)
    ax1.set_ylabel('<HTC> ( W/(m'u'\u00B2''K) )', fontsize = _fontsize)
    ax2 = ax1.twiny()
    ax2.set_xlabel('Velocity of Air (m/s)', fontsize= _fontsize)

    colorList = ['Crimson', 'SteelBlue', 'DarkGreen']
    fit_data = [] # To be used for the error band
    for _pd, _c in zip(powerDensities, colorList):
        counter = 0
        for _flow in flows:
            _flowS = str(_flow)
            _pdS = str(_pd).replace('.','_')
            htcError = eval('errorMeanHTC%sLPM%scm2' % (_flowS, _pdS)) * pow(10,4)
            htcMean = eval('meanHTC%sLPM%scm2' % (_flowS, _pdS)) * pow(10,4)
            #print htcError
            #print eval('errorMeanHTC%sLPM%scm2' % (_flowS, _pdS)) * pow(10,4)
            if counter == 0:
                ax1.errorbar(_flow, htcMean, xerr = 1., yerr = htcError, fmt = 'o', color = _c, label = str(_pd)+'(W/cm'u'\u00B2'')')
                ax2.errorbar(_flow/(6*(2.15 * 8.71)), htcMean, xerr = 1., yerr = 0., alpha = 0)   #Invisible for second axis
            else:
                ax1.errorbar(_flow, htcMean, xerr = 1., yerr = htcError, fmt = 'o', color = _c)
                ax2.errorbar( _flow/(6*(2.15 * 8.71)), htcMean, xerr = 1., yerr = 0., alpha = 0)  #Invisible for second axis
            print 'Added: meanHTC%sLPM%scm2 to plot' % (_flowS, _pdS)
            counter += 1 # So that only one pd appears in the legend
            # if _pd == 0.0490: #Include only 0.049 htc values for fitting
#                 fit_data.append( float(eval('meanHTC%sLPM%scm2' % (_flowS, '0_049'))) )

    ### FIT SQUARE ROOT FOT SYSTEMATIC ERROR BAND
    # def func(x, a, b):
#         return a * np.sqrt(x) + b
#     popt, pcov = curve_fit(func, flows, fit_data)
#     fit_x = [x for x in drange(25, 70, 0.1)]
#     fitYupper = []
#     fitYlower = []
#     for _x in fit_x:
#         fitYupper.append( 1.22*func(_x, popt[0], popt[1]) )
#         fitYlower.append( 0.78*func(_x, popt[0], popt[1]) )
#
#     ax1.fill_between(fit_x, fitYupper, fitYlower, color='grey', alpha='0.5')
#     ### END OF ERROR BAND INPUT

    def toV (lpm):
        return lpm/(6*(2.15 * 8.71))

    ax1.set_xticks(np.arange(30, 65 , 5))
    ax1.set_xlim(25, 65)
    ax2.set_xlim( toV(25), toV(65) )
    ax2.set_xticks( np.arange(toV(30), toV(62), toV(5)) )


    ax1.legend(loc=0, numpoints = 1, fontsize = _fontsize)
    ax1.grid(True)

    ### Output options
    outputName1 = 'Output/htc/'+fileName1
    plt.savefig(outputName1, format='pdf', bbox_inches='tight', dpi = _dpi)
    print '%s saved to: %s \n' %(fileName1, outputName1)
    #plt.show()
    
####################
    for _flow in flows:
        for _pd in powerDensities:
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            title = plt.title('HTC Measurement (per Strip)', fontsize = 1.2*_fontsize)
            ax1.set_xlabel('Strip Number (1->4 Cold->Hot || 5->8 Cold->Hot)', fontsize = _fontsize)
            ax1.set_ylabel('<HTC> ( W/(m'u'\u00B2''K) )', fontsize = _fontsize)

            _flowS = str(_flow)
            _pdS = str(_pd).replace('.','_')
            htc = eval('htc%sLPM%swcm2' % (_flowS, _pdS))
            #htc_2 = eval('htc%sLPM%swcm2_2' % (_flowS, _pdS))

            counter = 0
            for strip in xrange(1, 9):
                if counter == 0:
                    ax1.scatter(strip, htc[strip-1]*float(pow(10,4)), color = 'blue', label='HTC')
                    #ax1.scatter(strip, htc_2[strip-1]*float(10^4), color = 'red', label='Pc: Tstrip')
                if counter != 0:
                    ax1.scatter(strip, htc[strip-1]*float(pow(10,4)), color = 'blue')
                    #ax1.scatter(strip, htc_2[strip-1]*float(10^4), color = 'red')
                counter += 1
            ax1.axhline(eval('meanHTC%sLPM%scm2' % (_flowS, _pdS))*float(pow(10,4)), color = 'blue')
            #ax1.axhline(eval('meanHTC%sLPM%scm2_2' % (_flowS, _pdS)), color = 'red')

            ax1.set_xticks(np.arange(1,9,1))
            plt.legend(loc = 0, scatterpoints = 1, fontsize = _fontsize)
            plt.grid()
            plt.savefig('Output/htc/strip/strip_'+_flowS+'_'+_pdS+'.pdf', bbox_inches='tight', format = 'pdf', dpi = _dpi)
            plt.close()
####################
    
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title('HTC Measurement', fontsize = _fontsize)
    plt.xlabel('Power Density (W/cm'u'\u00B2'')', fontsize = _fontsize)
    plt.ylabel('<HTC> ( W/(m'u'\u00B2''K) )', fontsize= _fontsize)

    colorList = ['navy', 'darkcyan', 'green', 'orange', 'darkslategrey', 'magenta', 'crimson']
    #colorList = ['Aqua', 'Turquiose', 'Teal', 'LimeGreen', 'Goldenrod']
    for _flow, _c in zip(flows, colorList):
        counter = 0
        for _pd in powerDensities:
            _flowS = str(_flow)
            _pdS = str(_pd).replace('.','_')
            htcError = eval('errorMeanHTC%sLPM%scm2' % (_flowS, _pdS)) * pow(10,4)
            htcMean = eval('meanHTC%sLPM%scm2' % (_flowS, _pdS)) * pow(10,4)
            if counter == 0:
                ax1.errorbar(_pd, htcMean, xerr = 0.002, yerr = htcError, fmt = 'o', color = _c, label = str(_flow)+'LPM')
            else:
                ax1.errorbar(_pd, htcMean, xerr = 0.002, yerr = htcError, fmt = 'o', color = _c)
            print 'Added: meanHTC%sLPM%scm2 to plot' % (_flowS, _pdS)
            counter += 1
    ax1.legend(loc=0, numpoints = 1, fontsize = _fontsize)
    plt.xticks(np.arange(0, 0.1225 , 0.0245))
    plt.grid()
    outputName2 = 'Output/htc/'+fileName2
    plt.savefig(outputName2, format='pdf', bbox_inches='tight', dpi = _dpi)
    print '%s saved to: %s \n' %(fileName2, outputName2)
    #plt.show()
    

#HTCplots('meanHtc_flow_corrected_for_tc_%s.pdf'%str(_corr), 'meanHtc_pd_corrected_for_tc_%s.pdf'%str(_corr))

##########################################################################################