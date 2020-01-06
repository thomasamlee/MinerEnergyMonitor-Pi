from calculate.sumsquares import sumsquares
from read.sample_channel import sample_channel

# Read and compute the amperage on the specified channel

def read_amps(adc, chan, config):

    
    chanid = f"A{chan}"
    print("Sampling " + chanid)
    GAIN = config["Sampler"][chanid]["gain"]
   
    # The inductive sensor returns an AC voltage. Sample at the
    # maximum rate for 1 second.  Then calculate the RMS of
    print("Sampling started.")

    # read_adc
    try:
        values = sample_channel(adc, chan, GAIN)
       
        print("Sampling stopped")
    except ValueError as e:
        print("ADC configuration error: ", e)
        exit()
    except Exception as e:
        print("Unexpected ADC error: ", e)
        exit()


    return values



