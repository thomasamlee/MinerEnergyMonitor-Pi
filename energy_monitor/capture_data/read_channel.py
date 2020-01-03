import time


def read_channel(adc, chan, g):
    values = []
    adc.start_adc(chan, gain=g, data_rate=860)

    # Sample for one second

    # does this need to be made?
    start = time.time()
    while (time.time() - start) <= 1.0:
        # Read the last ADC conversion value and print it out.
        value = float(adc.get_last_result())
        values.append(value)
        # print('Channel {0}: {1}'.format(chan,value))

    # Stop continuous conversion.
    adc.stop_adc()

    return values
