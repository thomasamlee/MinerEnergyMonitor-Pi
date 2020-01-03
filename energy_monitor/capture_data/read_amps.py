# use absolute imports here
from calc import average, rootmeansquare, sumsquares
import read_channel

# Read and compute the amperage on the specified channel


def readAmps(adc, chan, config):

    # Channel A
    chanid = "A{}".format(chan)
    print("Sampling " + chanid)
    GAIN = config["Sampler"][chanid]["gain"]
    A = config["Sampler"][chanid]["A"]
    B = config["Sampler"][chanid]["B"]
    C = config["Sampler"][chanid]["C"]

    n = 0
    sum = 0.0
    ssq = 0
    rms = 0
    max = 0
    min = 0
    amps = 0
    values = []

    # The inductive sensor returns an AC voltage. Sample at the
    # maximum rate for 1 second.  Then calculate the RMS of
    # the sampled readings
    # what is the max rate?
    print("Sampling started.")

    try:
        values = read_channel(adc, chan, GAIN)
        n = len(values)
        print("Sampling stopped")
    except ValueError as e:
        print("ADC configuration error: ", e)
        exit()
    except Exception as e:
        print("Unexpected ADC error: ", e)
        exit()

    # Calculate basic stats on the raw data
    avg = average(values)
    ssq = sumsquares(values)
    bias = -avg
    print("ssq ", ssq)
    print("avg", avg)
    print("bias", bias)

    variance = float(ssq)/n - avg*avg
    print("variance", variance)
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
