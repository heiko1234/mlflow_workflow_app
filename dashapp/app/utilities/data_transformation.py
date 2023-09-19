

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


def transform_column(df, column, transformation):

    if transformation == "no transformation":
        data = df[column]
    elif transformation == "log":
        data = df[column].apply(lambda x: np.log(x))
    elif transformation == "sqrt":
        data = df[column].apply(lambda x: np.sqrt(x))
    elif transformation == "1/x":
        data = df[column].apply(lambda x: 1/x)
    elif transformation == "x^2":
        data = df[column].apply(lambda x: x**2)
    elif transformation == "x^3":
        data = df[column].apply(lambda x: x**3)
    else:
        data = df[column]

    return data




