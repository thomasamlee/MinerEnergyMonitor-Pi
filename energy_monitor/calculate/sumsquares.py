# Calculate sum of squares
def sumsquares(values):
    ssq = 0
    for value in values:
        ssq = ssq + value * value

    return ssq


def close():
    print("close")