







import pandas as pd






df = pd.DataFrame()

df["Yield"] = [44.0, 43.0, 46.0, 40.1, 42.2]
df["BioMaterial1"]=[5.5, 4.5, 3.5, 1.0, 6.0]
df["BioMaterial2"]=[9.5, 9, 5, 10, 12]
df["ProcessValue1"] = [20, 15, 10, 9, 2]


target = "Yield"

features = ["BioMaterial1", "BioMaterial2", "ProcessValue1"]


target_and_fetures = [target] + features


df




pandas_dtypes = {
    "float64": "float",
    "int64": "integer",
    "bool": "boolean",
    "double": "double",
    "object": "string",
    "binary": "binary",
}




import mlflow
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
import os
from dotenv import load_dotenv


load_dotenv()


client = MlflowClient()


for rm in client.search_registered_models():
    print(rm.name)
    print(rm.name, rm.description, rm.tags)



# project_name



mlflow_model = get_mlflow_model(model_name="project_name", azure=True, staging="Staging")
mlflow_model

mlflow_model
# >>> mlflow_model
# mlflow.pyfunc.loaded_model:
#   artifact_path: model
#   flavor: mlflow.sklearn
#   run_id: bf9ef49af857426c81fc82fce0bbd2c9



# model_uuid: fd115ef2870d4518ac977bd00b5360e7
# run_id: 2791a41295c94ae29b7e37efbb60c2d9





mlflow_model.metadata.artifact_path
# model
mlflow_model.metadata.run_id
# 'bf9ef49af857426c81fc82fce0bbd2c9'

mlflow_model.metadata.get_input_schema()
# >>> mlflow_model.metadata.get_input_schema()
# ['BioMaterial1': float, 'BioMaterial2': float, 'ProcessValue1': integer]




mlflow_model.metadata.get_output_schema()
# [float]



# load dictionary artifact from mlflow model
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path


# import importlib.util
# spec = importlib.util.spec_from_file_location("feature_limits.json", "models:/project_name/Staging/1/MLmodel")
# spec
# foo = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(foo)
# foo.__dict__
# # foo.__dict__["signature"]
# # foo.__dict__["signature"].inputs
# # foo.__dict__["signature"].outputs
# # foo.__dict__["signature"].inputs[0].type
# # foo.__dict__["signature"].inputs[0].name
# # foo.__dict__["signature"].inputs[0].type
# # foo.__dict__["signature"].inputs[0].type_string
# # foo.__dict__["signature"].inputs[0].type_string == "float"
# # foo.__dict__["signature"].inputs[0].type_string == "integer"
# # foo.__dict__["signature"].inputs[0].type_string == "string"
# # foo.__dict__["signature"].inputs[0].type_string == "binary"
# # foo.__dict__["signature"].inputs[0].type_string == "double"
# # foo.__dict__["signature"].inputs[0].type_string == "boolean"
# # foo.__dict__["signature"].inputs[0].type_string == "long"
# # foo.__dict__["signature"].inputs[0].type_string == "vector"
# # foo.__dict__["signature"].inputs[0].type_string == "tensor"
# # foo.__dict__["signature"].inputs[0].type_string == "ndarray"
# # foo.__dict__["signature"].inputs[0].type_string == "sparse_vector"
# # foo.__dict__["signature"].inputs[0].type_string == "unknown"
# # foo.__dict__["signature"].inputs[0].type_string == "map"



# feature_limits.json
# feature_dtypes.json




import os
import json
from pathlib import Path


from azure.storage.blob import BlobServiceClient


# mlflow.artifacts.load_dict("feature_limits.json")   # nope


model_dir="models:"
model_name="project_name"
model_stage="Staging"
artifact_path = PurePosixPath(model_dir).joinpath(model_name, model_stage)
artifact_path
artifact_path = str(artifact_path)
artifact_path = artifact_path+"/feature_dtypes.json"
artifact_path
mlflow.artifacts.load_dict(artifact_path)



def read_model_json_from_blob(connection_string, container_name, model_name, filename):
    # get mlflow model directory in blob: "models:/""
    model_dir = os.getenv("MLFLOW_MODEL_DIRECTORY", "models:")
    # get stage: "Staging"
    model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
    # get artifact path of mode with model_name on Stage: "Staging"
    artifact_path = PurePosixPath(model_dir).joinpath(model_name, model_stage)
    # load that model
    model = mlflow.pyfunc.load_model(str(artifact_path))
    # get the loaded model runid
    model_id=model.metadata.run_id
    
    client = BlobServiceClient.from_connection_string(
        connection_string
    )
    # container blob client to container of mlflow
    container_client = client.get_container_client(container_name)

    # create file client for blob with a specific filename, of staged model

    for blob in container_client.list_blobs():
        if model_id in blob.name and filename in blob.name:
            # print(blob.name)

            f_client = client.get_blob_client(
                container=container_name, blob=blob.name
            )
    
            tempfile = os.path.join("temp.json")
            # dir_to_create = "".join(tempfile.split("/")[0:-1])
            # make folder path if it does not exist
            # os.makedirs(dir_to_create, exist_ok=True)

            with open(tempfile, "wb") as file:
                blob_data = f_client.download_blob()
                blob_data.readinto(file)

            try: 
                return json.loads(open(tempfile, "r").read())
            # except BaseException:
            #    print(f"seem to be no file: {filename} in blob: {container_name} available")
            finally:
                # finally remove temporary file
                Path(tempfile).unlink()


def get_model_json_artifact(
    azure=True,
    path=None,
    model_name=None,
    features="feature_dtypes.json",
):
    """This function loads json file form a dumped mlflow model or
    temporary dumps it to load it directly from azure / azurite

    Args:
        azure (bool, optional): [description]. Defaults to True.
        path ([type], optional): in docker: "/model/", else folder where models are saved.
        model_path (str, optional): [description]. Defaults to "models".
        model_name ([type], optional): [sklearn model name]. Defaults to None.
        features (str, optional): feature_dtypes.json/ feature_limits.json

    Returns:
        [type]: [json file]
    """

    if not azure:
        # Access the artifacts to "/model/model_name/file" for the docker.

        path_load = os.path.join(path, model_name, features)

        return json.loads(open(path_load, "r").read())
    
    if azure:
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_MODEL_CONTAINER_NAME")

        file = read_model_json_from_blob(connection_string=connection_string, 
                        container_name=container_name, 
                        model_name=model_name, 
                        filename=features)
        if file: 
            return file
        else: 
            print(f"Warning: seem to be no file: {features} in blob: {container_name} available")





def get_model_json_artifact_by_model(model_name, stage="Staging", features="feature_dtypes.json"):
    
    model_dir="models:"
    
    artifact_path = PurePosixPath(model_dir).joinpath(model_name, model_stage)
    
    path_to_file = str(artifact_path)+"/"+features
    
    output = mlflow.artifacts.load_dict(path_to_file)
    
    return output



feature_dtypes=get_model_json_artifact_by_model(
    model_name="project_name",
    stage="Staging",
    features="feature_dtypes.json",
)
feature_dtypes



feature_limits=get_model_json_artifact_by_model(
    model_name="project_name",
    stage="Staging",
    features="feature_limits.json",
)
feature_limits



target_limits=get_model_json_artifact_by_model(
    model_name="project_name",
    stage="Staging",
    features="target_limits.json",
)
target_limits



# ################### #

feature_dtypes=get_model_json_artifact(
    azure=True,
    model_name="project_name",
    features="feature_dtypes.json",
)
feature_dtypes
# {'BioMaterial1': 'float', 'BioMaterial2': 'float', 'ProcessValue1': 'integer'}


feature_limits=get_model_json_artifact(
    azure=True,
    model_name="project_name",
    features="feature_limits.json",
)
feature_limits
# {'BioMaterial1': {'min': 1.0, 'max': 6.0}, 'BioMaterial2': {'min': 5.0, 'max': 10.0}, 'ProcessValue1': {'min': 1.66, 'max': 20.0}}



target_limits=get_model_json_artifact(
    azure=True,
    model_name="project_name",
    features="target_limits.json",
)
target_limits
# >>> target_limits
# {'Yield': {'min': 40.1, 'max': 46.0}}



def decode_df_mlflow_dtype(data, dtype_dict):

    mlflow_dtypes = {
        "float": "float32",
        "integer": "int32",
        "boolean": "bool",
        "double": "double",
        "string": "object",
        "binary": "binary",
    }

    for element in list(dtype_dict.keys()):
        try:
            data[element] = data[element].astype(
                mlflow_dtypes[dtype_dict[element]]
            )
        except BaseException:
            continue
    return data





df
feature_dtypes

# >>> df
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   44.0           5.5           9.5             20
# 1   43.0           4.5           9.0             15
# 2   46.0           3.5           5.0             10
# 3   40.1           1.0          10.0              9
# 4   42.2           6.0          12.0              2
# >>> feature_dtypes
# {'BioMaterial1': 'float', 'BioMaterial2': 'float', 'ProcessValue1': 'integer'}


data = decode_df_mlflow_dtype(data = df, dtype_dict=feature_dtypes)

data

# >>> data
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   44.0           5.5           9.5             20
# 1   43.0           4.5           9.0             15
# 2   46.0           3.5           5.0             10
# 3   40.1           1.0          10.0              9
# 4   42.2           6.0          12.0              2



def make_minmax_df(dict):
    df = pd.DataFrame()
    for element in list(dict.keys()):
        df[element] = [dict[element]["max"], dict[element]["min"]]
    return df



limits_df = make_minmax_df(dict=feature_limits)
limits_df



from sklearn.preprocessing import MinMaxScaler

feature_minmaxscaler = MinMaxScaler()


feature_minmaxscaler.fit(limits_df)


features = list(feature_limits.keys())
features


data.loc[:, features]
# >>> data.loc[:, features]
#    BioMaterial1  BioMaterial2  ProcessValue1
# 0           5.5           9.5             20
# 1           4.5           9.0             15
# 2           3.5           5.0             10
# 3           1.0          10.0              9
# 4           6.0          12.0              2




features_data_scaled = feature_minmaxscaler.transform(data.loc[:,features])
features_data_scaled
# >>> features_data_scaled
# array([[0.9       , 0.64285714, 1.        ],
#        [0.7       , 0.57142857, 0.72222222],
#        [0.5       , 0.        , 0.44444444],
#        [0.        , 0.71428571, 0.38888889],
#        [1.        , 1.        , 0.        ]])



features_data_scaled

features_data_scaled_df = pd.DataFrame(features_data_scaled, columns = features)

features_data_scaled_df
# >>> features_data_scaled_df
#    BioMaterial1  BioMaterial2  ProcessValue1
# 0           0.9      0.642857       1.000000
# 1           0.7      0.571429       0.722222
# 2           0.5      0.000000       0.444444
# 3           0.0      0.714286       0.388889
# 4           1.0      1.000000       0.000000


features_data_scaled_df = decode_df_mlflow_dtype(data = features_data_scaled_df, dtype_dict=feature_dtypes)

features_data_scaled_df
# >>> features_data_scaled_df
#    BioMaterial1  BioMaterial2  ProcessValue1
# 0           0.9      0.642857              1
# 1           0.7      0.571429              0
# 2           0.5      0.000000              0
# 3           0.0      0.714286              0
# 4           1.0      1.000000              0



df_predictions = mlflow_model.predict(features_data_scaled_df)
df_predictions
# >>> df_predictions
# array([[ 0.66101693],
#        [ 0.52069918],
#        [ 1.01795311],
#        [-0.64448121],
#        [ 0.3559322 ]])



target_limits
target_minmaxscaler = MinMaxScaler()
target_minmaxscaler.fit(make_minmax_df(dict=target_limits))

output = target_minmaxscaler.inverse_transform(df_predictions.reshape(-1, 1))

output


df



# >>> output
# array([[43.99999987],
#        [43.17212513],
#        [46.10592334],
#        [36.29756084],
#        [42.2       ]])
# >>> df
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   44.0           5.5           9.5             20
# 1   43.0           4.5           9.0             15
# 2   46.0           3.5           5.0             10
# 3   40.1           1.0          10.0              9
# 4   42.2           6.0          12.0              2




output = pd.DataFrame(output, columns = [target])
output


# >>> output
#        Yield
# 0  44.000000
# 1  43.172125
# 2  46.105923
# 3  36.297561
# 4  42.200000








data.loc[0,features]
# >>> data.loc[0,features]
# BioMaterial1      5.5
# BioMaterial2      9.5
# ProcessValue1    20.0
# Name: 0, dtype: float64


data = data.loc[0,features]
data = pd.DataFrame(data).T
data


features_data_scaled = feature_minmaxscaler.transform(data)
features_data_scaled
# >>> features_data_scaled
# array([[0.9       , 0.64285714, 1.        ]])



features_data_scaled

features_data_scaled_df = pd.DataFrame(features_data_scaled, columns = features)

features_data_scaled_df
# >>> features_data_scaled_df
#    BioMaterial1  BioMaterial2  ProcessValue1
# 0           0.9      0.642857       1.000000


features_data_scaled_df = decode_df_mlflow_dtype(data = features_data_scaled_df, dtype_dict=feature_dtypes)

features_data_scaled_df
# >>> features_data_scaled_df
#    BioMaterial1  BioMaterial2  ProcessValue1
# 0           0.9      0.642857              1




df_predictions = mlflow_model.predict(features_data_scaled_df)
df_predictions

output = target_minmaxscaler.inverse_transform(df_predictions.reshape(-1, 1))

output



output[0][0]
# >>> output[0][0]
# 43.999999872898805



output = pd.DataFrame(output, columns = [target])
output


# >>> output
# array([[43.99999987]])
# >>> output = pd.DataFrame(output, columns = [target])
# >>> output
#    Yield
# 0   44.0






output.iloc[0,0]
# >>> output.iloc[0,0]
# 43.999999872898805


















