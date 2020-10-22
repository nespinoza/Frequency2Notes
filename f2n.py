import numpy as np
import math

# First, copy a table of known notes and frequencies:
names = np.array(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
# Frequency in HZ is just 440 x 2^(n/12), with n = 0 being A (440 HZ):
frequencies = 440. * 2**(np.append(np.arange(-9,0,1),np.arange(0,3,1))/12.)
print(frequencies)
min_f = np.min(frequencies)
max_f = np.max(frequencies)

# Now, ask for a frequency:
input_frequency = np.double(input('\t Input the frequency you want to check (in HZ):'))

# Compute scaling to bring it between the frequencies defined above. We are trying to 
# find the n in (input frequency) x (2^n) = (base frequency), where (base frequency) is 
# any of the frequencies defined in our table above:
n = np.log(frequencies/input_frequency)/np.log(2.)

# We are looking for an integer n; so, take int of the above, substract that to the non-int 
# n's, and get the closest to an int. That would be our best "n":
n_int = np.rint(n)
residuals = np.abs(n - n_int)
idx = np.where(residuals == np.min(residuals))[0]
nfinal = n_int[idx][0]
# Now, it could be that nfinal is an edge case. Check that when multiplying that with the 
# original frequency, it falls within the range of our table. If smaller, multiply by 2 
# again. If larger, divide by 2
scaled_frequency = input_frequency*(2.**nfinal)
if scaled_frequency < min_f:
    candidate_scaled_frequency = input_frequency*(2**(nfinal+1))
    d1 = np.abs(min_f - candidate_scaled_frequency)
    d2 = np.abs(min_f - scaled_frequency)
    if d1 < d2:
        nfinal = nfinal+1
        scaled_frequency = input_frequency*(2**nfinal)
elif scaled_frequency > max_f:
    candidate_scaled_frequency = input_frequency*(2**(nfinal-1))
    d1 = np.abs(max_f - candidate_scaled_frequency)
    d2 = np.abs(max_f - scaled_frequency)
    if d1 < d2:
        nfinal = nfinal-1
        scaled_frequency = input_frequency*(2**nfinal)

# Now, compare with the table:
residuals_f = np.abs(scaled_frequency - frequencies)
idx = np.where(np.min(residuals_f) == residuals_f)[0][0]

# Report closest frequency, name, and scaled frequency:
print('\t Closest frequency is ',frequencies[idx],' Hz, which is an '+names[idx]+'.')
print('\t Input frequency was scaled by 2^('+str(int(nfinal))+'), which corresponds to {0:.4f} Hz.'.format(scaled_frequency))
