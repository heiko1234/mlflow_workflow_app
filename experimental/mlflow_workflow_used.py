

import numpy as np
import pandas as pd


import Setuptools

import azureml
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



from dashapp.app.utilities.spc import (
    transform_cleaning_table_in_dict,
    use_spc_cleaning_dict,
    create_limits_dict,
    update_nested_dict,
    filter_dataframe_by_limits
)


# https://github.com/heiko1234/dash_app_with_mlflow/blob/main/dashapp/app/app_utility.py

import os
from dotenv import load_dotenv

load_dotenv()

local_run = os.getenv("LOCAL_RUN", False)
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("BLOB_MODEL_CONTAINER_NAME")


df = pd.read_parquet("data/ChemicalManufacturingProcess.parquet")





pandas_dtypes = {
    "float64": "float",
    "int64": "integer",
    "bool": "boolean",
    "double": "double",
    "object": "string",
    "binary": "binary",
}


sk_model = DecisionTreeRegressor()



instance_minmaxscaler = MinMaxScaler()






limits_table_df =  df.describe().T
limits_table_df

limits_table_df["description"]=limits_table_df.index
limits_table_df = limits_table_df.reset_index(drop=True)
limits_table_df


limits_dict = create_limits_dict(limits_table_df=limits_table_df)
limits_dict

target_and_fetures = ["Yield", "BiologicalMaterial04", "ManufacturingProcess05"]

min_max_fitting_table = limits_table_df[limits_table_df["description"].isin(target_and_fetures)]

# how to fit minmaxscaler with a dictionary that contains min, max and description?
# https://stackoverflow.com/questions/55696209/how-to-fit-minmaxscaler-with-a-dictionary-that-contains-min-max-and-description
instance_minmaxscaler = MinMaxScaler()


instance_minmaxscaler.fit(df.loc[:,target_and_fetures])



fitted_df = instance_minmaxscaler.transform(df.loc[:,target_and_fetures])
fitted_df = pd.DataFrame(fitted_df, columns=target_and_fetures)
fitted_df

y_train = fitted_df["Yield"]
x_train = fitted_df.drop("Yield", axis=1)

y_train
x_train


sk_model.fit(x_train, y_train)

train_score = round(sk_model.score(x_train, y_train), 4)
train_score

sk_model.get_params()

sk_model.get_depth()

sk_model.predict(x_train)






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



features_train, features_test, target_train, target_test = reset_index_train_test_split(
    feature_data=x_train, target_data=y_train, test_size=0.2, random_state=2021
)



target_data = fitted_df["Yield"]
feature_data = fitted_df.drop("Yield", axis=1)



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




input_schema
output_schema

signature





MLFlow_Experiment = "Project_name"

mlflow.set_experiment(MLFlow_Experiment)

mlflow.is_tracking_uri_set()

# mlflow.tracking.get_tracking_uri()
# 'file:///home/heiko/Schreibtisch/Repos/dash_apps/mlflow_workflow_app/mlruns'


# mlflow.set_registry_uri("sqlite:///mlflow.db")







with mlflow.start_run():

    sk_model.fit(features_train, target_train)

    train_score = round(sk_model.score(features_train, target_train), 4)
    train_score


    mlflow.log_params(sk_model.get_params())
    mlflow.log_metric("train_score", train_score)

    round(sk_model.score(features_test, target_test), 4)

    mlflow.sklearn.log_model(
        sk_model, "model", signature=signature
    )

mlflow.end_run()







