import math

# Calculate RMS excluding noisey values more than 3x std dev
def rootmeansquare(values, avg, stddev, bias):
    ssq = 0.0
    sum = 0.0
    n = 0

    for value in values:
        newValue = value + bias
        # Skip values more that 3x stddev
        if abs(value) < avg + 3*stddev:
            ssq = ssq + newValue * newValue
            sum = sum + newValue
            n = n + 1

    # Figure the RMS, which is the square root of the average of the
    # sum of squares figured above
    if n == 0:
        rms = 0.00
    else:
        rms = math.sqrt(float(ssq)/n)
    print('RMS: {0}'.format(rms))
    return rms


# Calculate sum of squares
def sumsquares(values):
    ssq = 0
    for value in values:
        ssq = ssq + value * value

    return ssq


# Calculate the average value
def average(values):
    sum = 0
    for value in values:
        sum = sum + value
    avg = sum/len(values)
    return avg
