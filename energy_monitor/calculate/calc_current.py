import statistics 
import math
from calculate.rootmeansquare import rootmeansquare
from calculate.sumsquares import sumsquares


# this would make a great class

def calc_current(values, config):
    A = config["sampler"][0]["A"]
    B = config["sampler"][0]["B"]
    C = config["sampler"][0]["C"]

    n = len(values)
    avg = statistics.mean(values)
    ssq = sumsquares(values)
    bias = -avg
    variance = float(ssq)/n - avg*avg
    # variance = statistics.variance(ssq)
    stdev = math.sqrt(variance)
    # stdev = statistics.stdev(ssq)
    rms = rootmeansquare(values, avg, stdev, bias)

    # Polynomial regression based on experimentation
    temp = A + B*rms + C*rms*rms
    print("A", A)
    print("B", B)
    print("C", C)

    # Round to 2 decimal places
    current = round(temp, 2)
    if current < 0:
        current = 0.00
    print(f'Average Reading in Amps: {current}')

    return current
    