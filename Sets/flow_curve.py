from scipy.optimize import curve_fit
from scipy.odr import *

##########################################################################################
### FINDING THE FLOW CURVE OF THE CFOAM SETUP
##########################################################################################
flow = [0., 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
flow = np.asarray(flow) #Array conversion

### Set 1 (Integrated DP)
# dp1 = [ 1.1, 1.8, 2.5, 3.5, 4.8, 6.4, 8.4, 10.8, 13.7, 17.0, 20.6, 23.2, 24.8 ]
# dp2 = [ 1.0, 1.8, 2.6, 3.4, 4.7, 6.4, 8.6, 11.0, 13.7, 16.7, 21.2, 23.0, 24.7 ]
# dp3 = [ 1.0, 1.8, 2.5, 3.4, 4.6, 6.3, 8.4, 10.4, 13.7, 16.8, 21.0, 23.1, 24.9 ]

### Set 2 (Integrated DP)
# dp1 = [ 1.0, 1.7, 2.4, 3.3, 4.7, 6.4, 8.3, 10.7, 13.7, 17.0, 20.8, 22.7, 25.1 ]
# dp2 = [ 1.0, 1.7, 2.4, 3.3, 4.6, 6.3, 8.3, 10.8, 13.7, 16.9, 20.9, 23.1, 25.0 ]
# dp3 = [ 1.0, 1.7, 2.4, 3.3, 4.5, 6.3, 8.2, 10.7, 13.7, 17.0, 20.8, 22.8, 24.9 ]

### Set 3 (Handheld DP)
dp1 = [ 0, 0.6, 1.3, 2.2, 3.3, 4.8, 6.9, 8.9, 12.1, 15.0, 18.2, 21.6, 23.8 ]
dp2 = [ 0, 0.6, 1.3, 2.3, 3.6, 5.2, 6.9, 9.3, 12.1, 15.5, 18.3, 21.4, 23.8 ]
dp3 = [ 0, 0.6, 1.3, 2.3, 3.5, 5.1, 6.9, 9.3, 11.9, 14.8, 18.4, 21.2, 23.9 ]

### Set 4 (Handheld DP)
dp4 = [ 0, 0.6, 1.4, 2.4, 3.5, 5.1, 7.3, 9.5, 12.3, 15.0, 18.3, 21.4, 24.1 ]
dp5 = [ 0, 0.6, 1.3, 2.3, 3.5, 5.1, 7.1, 9.1, 12.1, 15.2, 18.9, 21.4, 23.6 ]
dp6 = [ 0, 0.6, 1.3, 2.2, 3.5, 5.1, 7.1, 9.5, 12.4, 15.2, 19.2, 21.0, 23.9 ]

### Fit Arrays
fit_flow = [a for a in drange(0.0, 100, 0.1)]
fit_dp = [x for x in drange(0.0, 30, 0.01)]

##########################################################################################
### Avg Values

avgDp = []
for i in range(0, len(dp1)):
	sumTotal = 0
	for j in range(1,4):
		sumTotal += eval("dp"+str(j))[i]
	avgDp.append(sumTotal/3.)
avgDp = np.asarray(avgDp) #Array conversion

##########################################################################################
### ERROR IN MEASUREMENT
##########################################################################################
flowError = 0.5 # [0.05*F for F in flow]

dpSpread40 = [9.554, 9.705, 9.705, 9.699, 9.705, 9.474]
dpSpread50 = [16.095, 16.158, 16.106, 16.150, 15.900, 16.143]

dpError = (std_deviation(dpSpread40)  + std_deviation(dpSpread50)) / 2.

print "\n===\nUsed Error in Flow", flowError
print "Used Error in DP", dpError, "\n===\n"

fractionFlowError = [100*flowError/flowvalue if flowvalue > 0 else 0 for flowvalue in flow]
print fractionFlowError
fractionDpError = [100*dpError/dpvalue if dpvalue > 0 else 0 for dpvalue in avgDp]
print fractionDpError
# if plotting == True:
# 	fig = plt.figure()
# 	ax1 = fig.add_subplot(2,1,1)
# 	ax1.set_title("Fraction Error Flow", fontsize = 16.)
# 	plt.xlabel("Flow of Air (LPM)", fontsize = 16.)
# 	plt.ylabel("Fractional Error", fontsize = 16.)
# 	ax1.scatter(flow, fractionFlowError, s= 50)
# 	plt.grid()
#
# 	ax2 = fig.add_subplot(2,1,2)
# 	ax2.set_title("Fraction Error Dp", fontsize = 16.)
# 	plt.xlabel("Differential Pressure (mbar)", fontsize = 16.)
# 	plt.ylabel("Fractional Error", fontsize = 16.)
# 	ax2.scatter(avgDp, fractionDpError, s= 50)
# 	plt.grid()
#
# 	plt.show()

##########################################################################################
### Fitting

def fitParabola(x, a):
	return a*x*x
fitParamsPara, fitCovariancesPara = curve_fit(fitParabola, flow, avgDp)
fitted_dp_flow = []
for F in fit_flow:
	fitted_dp_flow.append( fitParabola(F, fitParamsPara[0]) )
print "Parabola Fit Results: "
print fitParamsPara
print fitCovariancesPara
print " "

def fitSqrt(x, a):
	return a*x**0.5
fitParamsSqrt, fitCovariancesSqrt = curve_fit(fitSqrt, avgDp, flow)
fitted_flow_dp = []
for dp in fit_dp:
	fitted_flow_dp.append( fitSqrt(dp, fitParamsSqrt[0]) )
print "Square Root Fit Results: "
print fitParamsSqrt
print fitCovariancesSqrt
print " "

### RESIDUALS
residualsParabola = []
for i, j in zip(avgDp, flow):
	residualsParabola.append( i - fitParabola(j, fitParamsPara[0]) )

residualsSqrt = []
for i, j in zip(flow, avgDp):
	residualsSqrt.append( i - fitSqrt(j, fitParamsSqrt[0]) )

print "Residuals for Parabola:"
print residualsParabola
print "Residuals for Square Root:"
print residualsSqrt

print "\n===DEMING REGRESSION===\n"

avgDp = [dp**0.5 for dp in avgDp] #Linear line
#initial guess:
b00, b01 = np.polyfit(flow, avgDp, 1)
print "===\nInitial guess:"
print "slope:", b00
print "translation:", b01, "\n===\n"

def fit_func(B, x):
	return B[0]*x + B[1]

linear = Model(fit_func)
mydata = Data(flow, avgDp, wd = 1./pow(flowError,2), we = 1./pow(dpError/2.,2))
myodr = ODR(mydata, linear, beta0=[b00, 0], ifixb=[1,0])
myoutput = myodr.run()
myoutput.pprint()
redChi = myoutput.res_var
print "Reduced Chi Squared:", redChi
print "\nComparission:"
print "Parabole optimazation: a =", fitParamsPara[0]
print "Deming regression: a =", pow(myoutput.beta[0],2)

print "\n With Optimized Errors:"
flowError = flowError*pow(redChi,0.5)
dpError = dpError*pow(redChi,0.5)
print "Flow Error:", flowError
print "Dp Error:", dpError

mydata = Data(flow, avgDp, wd = 1./pow(flowError,2), we = 1./pow(dpError/2.,2))
myodr = ODR(mydata, linear, beta0=[b00, 0], ifixb=[1,0])
myoutput = myodr.run()
myoutput.pprint()
redChi = myoutput.res_var
print "Reduced Chi Squared:", redChi


avgDp = [dp**2 for dp in avgDp] #And back to original

demingFit = []
for flows in fit_flow:
	demingFit.append(pow(myoutput.beta[0],2)*pow(flows,2))

print "\nComparission:"
print "Parabole optimazation: a =", fitParamsPara[0]
print "Deming regression: a =", pow(myoutput.beta[0],2)


##########################################################################################
## Plotting (flow vs dp(flow))
# if plotting == True:
#     fig = plt.figure()
#     ax1 = fig.add_subplot(1, 1, 1)
#     ax1.set_title("Flow Curve", fontsize=16.)
#     plt.xlabel("Flow of Air (LPM)", fontsize = 16.)
#     plt.ylabel("Differential Pressure (mbar)", fontsize = 16.)
#
#     ax1.errorbar(flow, dp1, xerr = flowError, yerr = dpError, fmt = 'o', color = 'Magenta', label="Measurement 1", markersize='1')
#     ax1.errorbar(flow, dp2, yerr = dpError, xerr = flowError, fmt = 'o', color = 'DarkGreen', label="Measurement 2", markersize='1')
#     ax1.errorbar(flow, dp3, yerr = dpError, xerr = flowError, fmt = 'o', color = 'SteelBlue', label="Measurement 3", markersize='1')
#     ax1.errorbar(flow, avgDp, xerr = flowError, yerr = dpError, fmt = 'o', color = 'Crimson', label="Average", markersize='1')
#     #ax1.plot(fit_flow, fitted_dp_flow, color = 'Darkred', label="Fitted Model")
#     ax1.plot(fit_flow, demingFit, color = 'Darkred', label = 'Deming Fit')
#     plt.ylim(0, 26)
#     plt.xlim(0, 70)
#     ax1.set_xticks(np.arange(0, 70, 5))
#     ax1.set_yticks(np.arange(0, 30, 1))
#     ax1.legend(loc=0, numpoints = 1)
#     plt.grid()
#     #plt.show()
#     plt.savefig('flow_curve.pdf', format='pdf', dpi=2400)

if plotting == True:
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title("Flow Curve", fontsize=16.)
    plt.xlabel("Flow of Air (LPM)", fontsize = 16.)
    plt.ylabel("Differential Pressure (mbar)", fontsize = 16.)

    ax1.errorbar(flow, dp1, xerr = flowError, yerr = dpError, fmt = 'o', color = 'Magenta', label="Measurement 1", markersize='1')
    ax1.errorbar(flow, dp2, yerr = dpError, xerr = flowError, fmt = 'o', color = 'DarkGreen', label="Measurement 2", markersize='1')
    ax1.errorbar(flow, dp3, yerr = dpError, xerr = flowError, fmt = 'o', color = 'SteelBlue', label="Measurement 3", markersize='1')
    ax1.errorbar(flow, avgDp, xerr = flowError, yerr = dpError, fmt = 'o', color = 'Crimson', label="Average", markersize='1')
    #ax1.plot(fit_flow, fitted_dp_flow, color = 'Darkred', label="Fitted Model")
    ax1.plot(fit_flow, demingFit, color = 'Darkred', label = 'Deming Fit')
    plt.ylim(0, 26)
    plt.xlim(0, 70)
    ax1.set_xticks(np.arange(0, 70, 5))
    ax1.set_yticks(np.arange(0, 30, 1))
    ax1.legend(loc=0, numpoints = 1)
    plt.grid()
    #plt.show()
    outputName = 'Output/flow_curve/flow_curve.pdf'
    plt.savefig(outputName, format='pdf', bbox_inches='tight', dpi=1200)

	# ### Plotting (dp vs flow(dp))
	#
	# fig = plt.figure()
	# ax2 = fig.add_subplot(1, 1, 1)
	# ax2.set_title("Flow Curve", fontsize=16.)
	# plt.ylabel("Flow of Air (LPM)", fontsize = 16.)
	# plt.xlabel("Differential Pressure (mbar)", fontsize = 16.)
	#
	# # ax2.errorbar(dp1, flow, yerr = 1, xerr = [0.05*F for F in flow], fmt = 'o', color = 'Magenta', label="Measurement 1")
	# # ax2.errorbar(dp2, flow, yerr = 1, xerr = [0.05*F for F in flow], fmt = 'o', color = 'DarkGreen', label="Measurement 2")
	# # ax2.errorbar(dp3, flow, yerr = 1, xerr = [0.05*F for F in flow], fmt = 'o', color = 'SteelBlue', label="Measurement 3")
	# #ax2.errorbar(avgDp, flow, xerr = dpError, yerr = flowError, fmt = 'o', color = 'Crimson', label="Average")
	# #ax2.plot(fit_dp, fitted_flow_dp, color = 'DarkRed', label="Fitted Model")
	#
	# plt.xlim(0, 26)
	# plt.ylim(0, 70)
	# plt.yticks(np.arange(0, 70, 5))
	# plt.xticks(np.arange(0, 30, 1))
	# ax2.legend(loc=0, numpoints = 1)
	# plt.grid()
	# plt.show()
	# # #plt.savefig("flow_curve.pdf", format="pdf", dpi=1200)
