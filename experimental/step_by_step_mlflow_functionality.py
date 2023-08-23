


import pandas as pd



df = pd.DataFrame()

df["Yield"] = [44.0, 43.0, 46.0, 40.1, 42.2]
df["BioMaterial1"]=[5.5, 4.5, 3.5, 1.0, 6.0]
df["BioMaterial2"]=[9.5, 9, 5, 10, 12]
df["ProcessValue1"] = [20, 15, 10, 9, 2]


df
# >>> df
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   44.0           5.5           9.5             20
# 1   43.0           4.5           9.0             15
# 2   46.0           3.5           5.0             10
# 3   40.1           1.0          10.0              9
# 4   42.2           6.0          12.0              2




dd_list = ["Yield", "BioMaterial1", "BioMaterial2", "ProcessValue1"]

target_and_features = ["Yield", "BioMaterial1", "BioMaterial2", "ProcessValue1"]



df = df[dd_list]


dft=df.describe().reset_index(drop = True).T
dft = dft.reset_index(drop=False)
dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
dft["nan"]=df.isna().sum().values

dft

# >>> dft
#      description  counts   mean       std   min   25%   50%   75%   max  nan
# 0          Yield     5.0  43.06  2.181284  40.1  42.2  43.0  44.0  46.0    0
# 1   BioMaterial1     5.0   4.10  1.981161   1.0   3.5   4.5   5.5   6.0    0
# 2   BioMaterial2     5.0   9.10  2.559297   5.0   9.0   9.5  10.0  12.0    0
# 3  ProcessValue1     5.0  11.20  6.760178   2.0   9.0  10.0  15.0  20.0    0




# Kleinere Tabelle


datatable = pd.DataFrame()

datatable["description"] = ["Yield", "BioMaterial1", "BioMaterial2", "ProcessValue1"]
datatable["usage"] = ["target", "feature", "feature", "feature"]
datatable["max"]= [46.5, 6.0, 10.0, 20]
datatable["min"] = [40, 1.0, 5.0, 1.66]
datatable["std"] = [1, 1.0, 0.5, 5]


datatable

# >>> datatable
#      description    usage   max    min
# 0          Yield   target  46.5  40.00
# 1   BioMaterial1  feature   6.0   1.00
# 2   BioMaterial2  feature  10.0   5.00
# 3  ProcessValue1  feature  20.0   1.66


datatable.loc[0, "description"]



# original use of minmax, with original dataframe

from sklearn.preprocessing import MinMaxScaler

instance_minmaxscaler = MinMaxScaler()


instance_minmaxscaler.fit(df.loc[:,target_and_features])


fitted_df = instance_minmaxscaler.transform(df.loc[:,target_and_features])

fitted_df

# >>> fitted_df
# array([[0.66101695, 0.9       , 0.64285714, 1.        ],
#        [0.49152542, 0.7       , 0.57142857, 0.72222222],
#        [1.        , 0.5       , 0.        , 0.44444444],
#        [0.        , 0.        , 0.71428571, 0.38888889],
#        [0.3559322 , 1.        , 1.        , 0.        ]])


# update


def make_minmaxscalingtable_by_descriptiontable(descriptiontable, expand_by=None):
    
    output_df = pd.DataFrame()
    
    if expand_by is None:
        
        for row_index in range(descriptiontable.shape[0]):
            output_df[descriptiontable.loc[row_index, "description"]] = [descriptiontable.loc[row_index, "max"], descriptiontable.loc[row_index, "min"]]

    elif expand_by is "std":
            
            for row_index in range(descriptiontable.shape[0]):
                output_df[descriptiontable.loc[row_index, "description"]] = [descriptiontable.loc[row_index, "max"]+ descriptiontable.loc[row_index, "std"], descriptiontable.loc[row_index, "min"]- descriptiontable.loc[row_index, "std"]]


    return output_df



new_minmaxscalingdf = make_minmaxscalingtable_by_descriptiontable(descriptiontable=datatable, expand_by="std")
new_minmaxscalingdf

# >>> new_minmaxscalingdf
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   47.5           7.0          10.5          25.00
# 1   39.0           0.0           4.5          -3.34


new_minmaxscalingdf = make_minmaxscalingtable_by_descriptiontable(descriptiontable=datatable, expand_by=None)
new_minmaxscalingdf

# >>> new_minmaxscalingdf
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   46.5           6.0          10.0          20.00
# 1   40.0           1.0           5.0           1.66





def create_data_minmax_dict(data):

    feature_data_minmax = data.describe().loc[["min", "max"], :]

    return feature_data_minmax.to_dict()





data_minmax_dict = create_data_minmax_dict(new_minmaxscalingdf)
data_minmax_dict
# {'Yield': {'min': 40.0, 'max': 46.5}, 'BioMaterial1': {'min': 1.0, 'max': 6.0}, 'BioMaterial2': {'min': 5.0, 'max': 10.0}, 'ProcessValue1': {'min': 1.66, 'max': 20.0}}



from sklearn.preprocessing import MinMaxScaler

instance_minmaxscaler_new = MinMaxScaler()


instance_minmaxscaler_new.fit(new_minmaxscalingdf.loc[:, target_and_features])


fitted_df_new = instance_minmaxscaler_new.transform(df.loc[:,target_and_features])

fitted_df_new

# >>> new_minmaxscalingdf
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   46.5           6.0          10.0          20.00
# 1   40.0           1.0           5.0           1.66

# >>> fitted_df_new
# array([[0.61538462, 0.9       , 0.9       , 1.        ],
#        [0.46153846, 0.7       , 0.8       , 0.72737186],
#        [0.92307692, 0.5       , 0.        , 0.45474373],
#        [0.01538462, 0.        , 1.        , 0.4002181 ],
#        [0.33846154, 1.        , 1.4       , 0.01853871]])



# >>> dft
#      description  counts   mean       std   min    max  
# 0          Yield     5.0  43.06  2.181284  40.1   46.0
# 1   BioMaterial1     5.0   4.10  1.981161   1.0    6.0
# 2   BioMaterial2     5.0   9.10  2.559297   5.0   12.0
# 3  ProcessValue1     5.0  11.20  6.760178   2.0   20.0



# >>> fitted_df
# array([[0.66101695, 0.9       , 0.64285714, 1.        ],
#        [0.49152542, 0.7       , 0.57142857, 0.72222222],
#        [1.        , 0.5       , 0.        , 0.44444444],
#        [0.        , 0.        , 0.71428571, 0.38888889],
#        [0.3559322 , 1.        , 1.        , 0.        ]])










y_train = fitted_df["Yield"]
x_train = fitted_df.drop("Yield", axis=1)

y_train
x_train


df
y_train = df["Yield"]
x_train = df.drop("Yield", axis=1)

y_train
x_train




from sklearn.model_selection import train_test_split


target_data = y_train
feature_data = x_train


test_size = 0.2  # 20% test data, 80% train data
random_state = 2023  # random seed

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







pandas_dtypes = {
    "float64": "float",
    "int64": "integer",
    "bool": "boolean",
    "double": "double",
    "object": "string",
    "binary": "binary",
}



def create_feature_dtype_dict(data, pandas_dtypes):
    output = {}

    for element in data.columns:
        output[element] = pandas_dtypes[str(data.dtypes[element])]

    return output




feature_dtypes_dict = create_feature_dtype_dict(
    data = feature_data,
    pandas_dtypes = pandas_dtypes)




from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec

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






import mlflow
import mlflow.sklearn

# mlflow.tracking.get_tracking_uri()
# 'file:///home/heiko/Schreibtisch/Repos/dash_apps/mlflow_workflow_app/mlruns'


# mlflow.set_registry_uri("sqlite:///mlflow.db")


MLFlow_Experiment = "Project_name"


# import variables from .env file
import os
from dotenv import load_dotenv


load_dotenv()



local_run = os.getenv("LOCAL_RUN", False)
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("BLOB_MODEL_CONTAINER_NAME")


local_run




mlflow.set_experiment(MLFlow_Experiment)

mlflow.is_tracking_uri_set()




from sklearn.linear_model import LinearRegression

sk_model = LinearRegression()





# from sklearn.pipeline import Pipeline


# instance_minmaxscaler_new   # scaler
# sk_model.fit(features_train, target_train)


# model_pipeline = Pipeline(steps=[("scaler", scaler), ("model", sk_model_out)])



features_train
target_train


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
    
    mlflow.log_dict(
        data_minmax_dict, "model/feature_limits.json"
    )
    
    
    mlflow.log_dict(
        feature_dtypes_dict, "model/feature_dtypes.json"
    )


mlflow.end_run()




# mlflow.sklearn.log_model(
#     model_pipe, "model", signature=signature
# )

# mlflow.set_tag("model_type", model)
# mlflow.set_tag("scaler", scaler)

# mlflow.set_tag("target", configuration["target"])
# mlflow.set_tag("features", configuration["features"])

# mlflow.set_tag("model_parameters", model_parameter_dict)

# mlflow.log_dict(
#     data_minmax_dict, "model/feature_limits.json"
# )
# mlflow.log_dict(
#     model_parameter_dict, "model/model_parameters.json"
# )
# mlflow.log_dict(
#     feature_dtypes_dict, "model/feature_dtypes.json"
# )





# https://mlflow.org/docs/latest/model-registry.html



from pathlib import PurePosixPath


def get_mlflow_model(model_name, azure=True, staging="Staging"):

    if azure:
        azure_model_dir = os.getenv("MLFLOW_MODEL_DIRECTORY", "models:/")
        if staging == "Staging":
            model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
            artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
        elif staging == "Production":
            model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Production")
            artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
        else:
            print("Staging must be either 'Staging' or 'Production'. Default: Staging")
            model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
            artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
        
        artifact_path

        model = mlflow.pyfunc.load_model(str(artifact_path))
        print(f"Model {model_name} loaden from Azure: {artifact_path}")
        
    return model





from mlflow import MlflowClient


client = MlflowClient()
for rm in client.search_registered_models():
    print(rm.name, rm.description, rm.tags)


# >>> for rm in client.search_registered_models():
# ...     print(rm.name, rm.description, rm.tags)
# ... 
# project_name  {}


# after model is registered, it can be loaded from registry





pn_model = get_mlflow_model(model_name= "project_name", azure=True,  staging="Staging")












