

import numpy as np


def transform_datapoint(datapoint, transformation=None):

    if transformation == "no transformation":
        data = datapoint
    elif transformation == "log":
        data = np.log(datapoint)
    elif transformation == "sqrt":
        data = np.sqrt(datapoint)
    elif transformation == "1/x":
        data = 1/datapoint
    elif transformation == "x^2":
        data = datapoint**2
    elif transformation == "x^3":
        data = datapoint**3
    else:
        data = datapoint

    return data



