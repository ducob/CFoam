from scipy.optimize import curve_fit
from scipy.odr import *
##########################################################################################
### FINDING THE HEAT LEAK OF THE CFOAM SETUP
##########################################################################################

data1 = import_data("25_02_2015", "15_17_38", "0")
data2 = import_data("24_02_2015", "12_00_56", "0")
data3 = import_data("24_02_2015", "20_53_52", "0")
data4 = import_data("26_02_2015", "08_56_00", "0")
data0 = import_data("13_04_2015", "14_53_57", "0")

##########################################################################################
### Printing

# print "Number of points in data 1 (0.0030625 W/cm2):", len(data1[TEMP][0]), "|| stepsize: ", step_size(data1)[0]
# print "Number of points in data 2 (0.006125 W/cm2): ", len(data2[TEMP][0]), "|| stepsize: ", step_size(data2)[0]
# print "Number of points in data 3 (0.0091875 W/cm2):", len(data3[TEMP][0]), "|| stepsize: ", step_size(data3)[0]
# print "Number of points in data 4 (0.01225 W/cm2):  ", len(data4[TEMP][0]), "|| stepsize: ", step_size(data4)[0]
# print "Number of points in data 5 (0.00000 W/cm2):  ", len(data0[TEMP][0]), "|| stepsize: ", step_size(data0)[0]
# print "------"
# print "Power (W) deposited in the resistors in data 1: ", mean(power_ps(data1)[2])
# print "Power (W) deposited in the resistors in data 2: ", mean(power_ps(data2)[2])
# print "Power (W) deposited in the resistors in data 3: ", mean(power_ps(data3)[2])
# print "Power (W) deposited in the resistors in data 4: ", mean(power_ps(data4)[2])
# print "Power (W) deposited in the resistors in data 5: ", mean(power_ps(data0)[2])
# print "------"
# print "Average Lab Environment Temperature (deg C) in data1:", mean(data1[TEMP][labEnv])
# print "Average Lab Environment Temperature (deg C) in data2:", mean(data2[TEMP][labEnv])
# print "Average Lab Environment Temperature (deg C) in data3:", mean(data3[TEMP][labEnv])
# print "Average Lab Environment Temperature (deg C) in data4:", mean(data4[TEMP][labEnv])
# print "Average Lab Environment Temperature (deg C) in data5:", mean(data0[TEMP][labEnv])
# print "------"
# print "Stable point temperature (deg C) data 1 (0.0030625 W/cm2): ", stable_temperature(data1)
# print "Stable point temperature (deg C) data 2 (0.006125 W/cm2):  ", stable_temperature(data2)
# print "Stable point temperature (deg C) data 3 (0.0091875 W/cm2): ", stable_temperature(data3)
# print "Stable point temperature (deg C) data 4 (0.01225 W/cm2):   ", stable_temperature(data4)
# print "Stable point temperature (deg C) data 5 (0.00000 W/cm2):   ", stable_temperature(data0)
# print "------"

##########################################################################################

temperature = [ stable_temperature(data0), stable_temperature(data1), stable_temperature(data2), stable_temperature(data3), stable_temperature(data4) ]
power = [ mean(power_ps(data0)[2]), mean(power_ps(data1)[2]), mean(power_ps(data2)[2]), mean(power_ps(data3)[2]), mean(power_ps(data4)[2]) ]
fit_x = [a for a in range(-5,30)]

##########################################################################################
### Fitting

tempError = 1.
powerError = 0.1

print "\n===DEMING REGRESSION===\n"
#initial guess
b00, b01 = np.polyfit(temperature, power, 1)
print "===\nInitial guess:"
print "slope:", b00
print "translation:", b01, "\n===\n"

def fit_func(B, x):
	return B[0]*x + B[1]

linear = Model(fit_func)
mydata = Data(temperature, power, wd = 1./pow(tempError,2), we = 1./pow(powerError,2))
myodr = ODR(mydata, linear, beta0=[b00, 0], ifixb=[1,0])
myoutput = myodr.run()
myoutput.pprint()
redChi = myoutput.res_var
print "Reduced Chi Squared:", redChi
print "\nComparission:"
print "Initial guess: a =", b00
print "Deming regression: a =", pow(myoutput.beta[0],2)

print "\n With Optimized Errors:"
tempError = tempError*pow(redChi,0.5)
powerError = powerError*pow(redChi,0.5)
print "Temperature Error:", tempError
print "Power Error:", powerError

mydata = Data(temperature, power, wd = 1./pow(tempError,2), we = 1./pow(powerError,2))
myodr = ODR(mydata, linear, beta0=[b00, 0], ifixb=[1,0])
myoutput = myodr.run()
myoutput.pprint()
redChi = myoutput.res_var
print "Reduced Chi Squared:", redChi

fit_temp = [a for a in drange(-5, 25, 0.1)]
demingFit = []
for temps in fit_temp:
	demingFit.append( myoutput.beta[0] * temps )

print "\nComparission:"
print "Initial guess: a =", b00
print "Deming regression: a =", pow(myoutput.beta[0],2)




##########################################################################################
### Plotting
if plotting == True:

	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)
	ax1.set_title("Heat Leak", fontsize=16.)
	plt.ylabel("Power (W)", fontsize = 16.)
	plt.xlabel("Avg. Cupper Temperature (lab corrected) ("u"\u00b0""C)", fontsize = 16.)

	ax1.errorbar(temperature, power, xerr = tempError, yerr = powerError, fmt = 'o', label='Measurement')
	ax1.plot(fit_temp, demingFit,lw=1., color = 'red', label = 'Deming Fit')
	plt.ylim(-0.5, 2.5)
	plt.xlim(-1, 20)
	ax1.set_xticks(np.arange(-1, 20, 1.0))
	ax1.set_yticks(np.arange(-0.5, 2.5, 0.25))
	ax1.legend(loc=0, numpoints = 1)
	plt.grid()
	#plt.show()
	plt.savefig("heat_leak.pdf", format="pdf", dpi=2400)
