def optStruct(self, instances-1, parallel-False):

I
=
{ 'ModelVars': self.mdlVars, 'SolverOpts': self.slv0pts, 'AnalysisOpts': self.an10pts}
1 & parallel):
self.OptStruct
return
mdl_list
slv_list
anl_list
self.OptStruct
[dp.copy.deepcopy(self.mdlVars) for in range(instances)]
[dp.copy.deepcopy(self.slvOpts) for in range(instances)]
[dp.copy.deepcopy (self.an10pts) for in range(instances)]
-
[{'ModelVars' :mdl_list[x], 'SolverOpts': slv_list[x], 'AnalysisOpts': anl_list [x]} for x in range(instances)]



def resample(self, time, signal):
00000
Resample a signal to have uniform time points.
Parameters
time (numpy.ndarray)
: Time values of the original signal.
signal (numpy.ndarray): Signal values.
Returns:
tuple: Tuple containing the resampled time values and the corresponding resampled signal values.
0000
new_t
0
dp.np.linspace(time.min(), time.max(), len(signal))
new_signal - dp.np.interp(new_t, time, signal)
return new_t,new_signal
def pyFFT(self, signal, fs):
Compute the Fast Fourier Transform (FFT) of a signal and return amplitude, phase, and frequency information.
Parameters
:
I
: Sampling frequency of the signal.
signal (numpy.ndarray) : Input signal.
fs (float)
Returns:
tuple: Tuple containing amplitude, phase, and frequency arrays.
N
44
- len(signal)
dp.fftfreq(N,1/fs)
f[f >= 0]
dp.np.arange(0, len(f)/2, dtype-int)
dp.fft(x-signal, workers-dp.multiprocessing.cpu_count())
dp.np.abs(fft)
useful
O
fft
amplitude
amplitude [0]
O
(1/N) * amplitude[0]
amplitude [1:N]
O
(2/N) * amplitude [1:N]
amplitude
O
pahse
frequency
amplitude [useful]
dp.np.angle(fft [useful], deg-True)
f[useful]
return amplitude, pahse, frequency
#
#
#
# Select useful indices and corresponding frequency values
# Compute FFT
# Calculate magnitude of FFT result
# Scale the magnitude values
# Scale the magnitude values
# Select useful indices and corresponding magnitude values
# Calculate phase angles of the FFT result


SolverOpts
{
}
'Solver'
'StartTime'
'TimeSpan'
'auto'
0.0
simParams['tSim']
'stopTime'
:
simParams['tSim']
0
'Timeout'
'MaxStep'
'FixedStep'
'RelTol'
'Refine'
simParams['Maxstep']
simParams['Fixedstep']
: simParams['RelTol']
simParams['Refine']
00








Icon: circle (-4, 17.5, .5)
Icon:line ({0, 0, -1), (15, 14, 14})
Icon: arc (-1.5, 10.5, 3.5, 3.5, 90, 180) Icon: line ((0, -1), (7, 7})
Icon: arc (-1.5, 3.5, 3.5, 3.5, 90, 180) Icon: line ((0, -1}, {0, 0})
Icon: arc (-1.5, -3.5, 3.5, 3.5, 90, 180) Icon: line ((0, -1}, {-7, -7})
e Icon: arc (-1.5, -10.5, 3.5, 3.5, 90, 180) OIcon: line ((0, 0, -1}, {-15, -14, -14})











line ([0, 0, -10],
line ([0,
0, -10],
line ([0, 0, -10],
line([-10, -10],
[20, 10, 10]) [10, 0, 0])
[-20, -10, -10])
[13, 7])
line ([-10,
-10], [3, -3])
line ([-10, -10],
[-7, -13])
line ([-15,
[10, -10])
line ([-15,
-15], -20], [0, 0])
line ([-4, -8, -4], [2, 0, -2])
line ([12, 12, 0], [6, 14, 14])
line ([5, 19], [-6, -6])
line([0, 12, 12], [-14, -14, -6]) line([12, 19, 5, 12], [-6, 6, 6, -6])












def rms_avg(self, Op, nested list, time_values):
www
Calculate the Root Mean Square (RMS) or Average (AVG) values for nested lists of signal data.
Parameters Op (str)
8
O
: Operation selection 'RMS' for Root Mean Square or 'AVG' for Average.
nested list (list): Nested list containing signal values. time_values (list): List of corresponding time values.
Returns:
www
array List of RMS or AVG values.
result
delta T
dp.np.array([])
time_values[-1] time_values[0]
for sublist in nested list:
O
I
match Op:
case 'RMS':
try:
try:
squared_values O res_value
O
(dp.np.array(sublist))**2
dp.np.sqrt(dp.np.trapz (squared_values, x-time_values) / delta_T)
except ZeroDivisionError:
print("Error: Division by zero is not allowed.")
case 'AVG':
try:
res_value - dp.np.trapz (dp.np.array(sublist), x-time_values) / delta_T except ZeroDivisionError:
print("Error: Division by zero is not allowed.")
result = dp.np.append(result, res_value)
except ValueError:
print("Error: Invalid input. Please enter valid numbers.")
return result





