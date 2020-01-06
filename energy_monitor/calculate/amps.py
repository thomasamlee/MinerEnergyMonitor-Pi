from statistics import mean, stdev, variance
from calculate.rootmeansquare import rootmeansquare

def amps(values, config):
    A = config["Sampler"][chanid]["A"]
    B = config["Sampler"][chanid]["B"]
    C = config["Sampler"][chanid]["C"]

    n = len(values)
    avg = mean(values)
    ssq = sumsquares(values)
    bias = -avg
    print("ssq ", ssq)
    print("avg", avg)
    print("bias", bias)

    # replace with statistics.variance()
    variance = float(ssq)/n - avg*avg
    print("variance", variance)

    # replace with statistics.stdev()
    stddev = math.sqrt(variance)
    print("stddev", stddev)

    # Calculate the RMS
    rms = rootmeansquare(values, avg, stddev, bias)

    # Polynomial regression to estimate amps
    # Based on experiments from 0 to 13 amps
    # Constants stored in config file.
    temp = A + B*rms + C*rms*rms
    print("A", A)
    print("B", B)
    print("C", C)

    # Round to 2 decimal places
    amps = round(temp, 2)
    if amps < 0:
        amps = 0.00
    print('Average Reading in Amps: {0}'.format(amps))

    return amps
