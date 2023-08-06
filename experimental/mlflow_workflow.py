

import numpy as np
import pandas as pd



import mlflow
import mlflow.sklearn

from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.model_selection import cross_val_score

# from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold

# Load Models from sklearn
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import AdaBoostRegressor




def replace_infs(df, with_value=np.nan):

    to_replace = [np.inf, -np.inf]

    return df.replace(to_replace, with_value)


def drop_nans(df: pd.DataFrame, axis=0):
    
    return df.dropna(axis)



def reset_index_train_test_split(
    feature_data, target_data, test_size=0.1, random_state=2021
):
    (
        features_train,
        features_test,
        target_train,
        target_test,
    ) = train_test_split(
        feature_data,
        target_data,
        test_size=test_size,
        random_state=random_state,
    )

    features_train = features_train.reset_index(drop=True)
    features_test = features_test.reset_index(drop=True)
    target_train = target_train.reset_index(drop=True)
    target_test = target_test.reset_index(drop=True)

    return features_train, features_test, target_train, target_test







def create_data_dict(data):

    feature_data_minmax = data.describe().loc[["min", "max"], :]

    return feature_data_minmax.to_dict()


def create_feature_dtype_dict(data, pandas_dtypes):
    output = {}

    for element in data.columns:
        output[element] = pandas_dtypes[str(data.dtypes[element])]

    return output




def reset_index_train_test_split(
    feature_data, target_data, test_size=0.1, random_state=2021
):
    (
        features_train,
        features_test,
        target_train,
        target_test,
    ) = train_test_split(
        feature_data,
        target_data,
        test_size=test_size,
        random_state=random_state,
    )

    features_train = features_train.reset_index(drop=True)
    features_test = features_test.reset_index(drop=True)
    target_train = target_train.reset_index(drop=True)
    target_test = target_test.reset_index(drop=True)

    return features_train, features_test, target_train, target_test





pandas_dtypes = {
    "float64": "float",
    "int64": "integer",
    "bool": "boolean",
    "double": "double",
    "object": "string",
    "binary": "binary",
}





MLFlow = True

MLFlow_Experiment = "Project_name"

sk_model = LinearRegression()
sk_model = DecisionTreeRegressor()
sk_model = RandomForestRegressor()


#  scaler
"MinMax": MinMaxScaler()
"Standard": StandardScaler()
"None": None



x_train
y_train




if MLFlow:
    # prework
    
    input_schema = Schema(
        [
            ColSpec(
                pandas_dtypes[str(feature_data.dtypes[element])], element
            )
            for element in feature_data.columns
        ]
    )
    output_schema = Schema(
        [ColSpec(pandas_dtypes[str(target_data.dtypes)])]
    )
    signature = ModelSignature(inputs=input_schema, outputs=output_schema)

    data_minmax_dict = create_data_dict(data)

    feature_dtypes_dict = create_feature_dtype_dict(data = feature_data,
                                    pandas_dtypes = pandas_dtypes)





if MLFlow:

    mlflow.set_experiment(MLFlow_Experiment)

    with mlflow.start_run():

        print("Model run: ", mlflow.active_run().info.run_uuid)

        print("Training and Evaluation for MLFlow started.")


    sk_model = sk_model.fit(x_train, y_train)
    train_score = round(sk_model.score(x_train, y_train), 4)
    print(f"Training Score: {train_score}")

    if MLFlow:
        mlflow.log_params(sk_model.get_params())
        mlflow.log_metric("train_score", train_score)


        mlflow.sklearn.log_model(
            model_pipe, "model", signature=signature
        )

        mlflow.set_tag("model_type", model)
        mlflow.set_tag("scaler", scaler)

        mlflow.set_tag("target", configuration["target"])
        mlflow.set_tag("features", configuration["features"])

        mlflow.set_tag("model_parameters", model_parameter_dict)

        mlflow.log_dict(
            data_minmax_dict, "model/feature_limits.json"
        )
        mlflow.log_dict(
            model_parameter_dict, "model/model_parameters.json"
        )
        mlflow.log_dict(
            feature_dtypes_dict, "model/feature_dtypes.json"
        )

    mlflow.end_run()

