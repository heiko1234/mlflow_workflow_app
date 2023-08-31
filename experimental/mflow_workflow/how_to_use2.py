




import os
import json
import mlflow
import pandas as pd
from pathlib import Path


from pathlib import PurePosixPath
from mlflow import MlflowClient


from sklearn.preprocessing import MinMaxScaler


from dotenv import load_dotenv


load_dotenv()




class mlflow_model():
    
    def __init__(self, model_name, staging="Staging"):


        load_dotenv()

        self.model_name = model_name
        self.staging = staging


        self.azure_model_dir = "models:/"

        if self.staging == "Staging":
            self.artifact_path = str(PurePosixPath(self.azure_model_dir).joinpath(self.model_name, "Staging"))
        elif self.staging == "Production":
            self.artifact_path = str(PurePosixPath(self.azure_model_dir).joinpath(self.model_name, "Production"))
        else:
            print("staging must be either 'Staging' or 'Production'")
            raise ValueError

        self.model = mlflow.pyfunc.load_model(self.artifact_path)
        print(f"Model {model_name} loaded")


    def list_registered_models(self):
        client = MlflowClient()
        output = []
        for rm in client.search_registered_models():
            output.append(rm.name)
        return output

    def get_model_version(self):
        client = MlflowClient()
        model_version = client.get_latest_versions(self.model_name, stages=[self.staging])[0].version
        return model_version
    
    def get_model(self):
        return self.model
    
    def get_model_artifact(self, artifact="feature_dtypes.json"):
        
        """
        
        aritfact: feature_names.json, feature_types.json, feature_limits.json, target_limits.json

        Returns:
            dictionary: dictionary with feature names and their data types
        """


        path_to_file = self.artifact_path + "/" + artifact

        path_to_file = path_to_file

        output = mlflow.artifacts.load_dict(path_to_file)

        return output


    def decode_df_mlflow_dtype(self, data, dtype):
        
        mlflow_dtypes = {
            "float": "float32",
            "integer": "int32",
            "boolean": "bool",
            "double": "double",
            "string": "object",
            "binary": "binary",
        }
    
        dtype_dict = self.get_model_artifact(artifact="feature_dtypes.json")
        
        for element in list(dtype_dict.keys()):
            try: 
                data[element] = data[element].astype(mlflow_dtypes[dtype_dict[element]])
            except BaseException:
                pass
        return data

    def make_minmax_df(self, dict):
        df = pd.DataFrame()
        for element in list(dict.keys()):
            df[element] = [dict[element]["max"], dict[element]["min"]]
        return df


    def get_feature_minmaxscaler(self):
        """
        Returns:
            dictionary: dictionary with feature names and their minmaxscaler
        """
        path_to_file = self.artifact_path + "/feature_limits.json"
        
        limits_df = mlflow.artifacts.load_dict(path_to_file)
        
        limits_df = self.make_minmax_df(limits_df)
        
        feature_minmaxscaler = MinMaxScaler()
        
        feature_minmaxscaler.fit(limits_df)
        
        return feature_minmaxscaler


    def get_target_minmaxscaler(self):
        """
        Returns:
            dictionary: dictionary with feature names and their minmaxscaler
        """
        path_to_file = self.artifact_path + "/target_limits.json"
        
        limits_df = mlflow.artifacts.load_dict(path_to_file)
        
        limits_df = self.make_minmax_df(limits_df)
        
        target_minmaxscaler = MinMaxScaler()
        
        target_minmaxscaler.fit(limits_df)
        
        return target_minmaxscaler


    def get_features(self):
        """
        Returns:
            dictionary: dictionary with feature names and their data types
        """
        path_to_file = self.artifact_path + "/feature_limits.json"
        
        features = mlflow.artifacts.load_dict(path_to_file)
        
        features = list(features.keys())
        
        return features
    
    def make_predictions(self, data):
        
        features = self.get_features()
        feature_scaler = self.get_feature_minmaxscaler()
        target_scaler = self.get_target_minmaxscaler()
        feature_dtypes = self.get_model_artifact(artifact="feature_dtypes.json")
        
        print(f"features: {features}")
        
        try:
            scale_data = data[features]
            feature_data_scaled = feature_scaler.transform(scale_data)
            feature_data_scaled_df = pd.DataFrame(feature_data_scaled, columns=features)
            feature_data_scaled_df = self.decode_df_mlflow_dtype(feature_data_scaled_df, dtype=feature_dtypes)
            
            df_predictions = self.model.predict(feature_data_scaled_df)
            
            output = target_scaler.inverse_transform(df_predictions)
            
            output = list(output.flatten())

            return output
        
        except BaseException as e:
            print(e)
            return None








df = pd.DataFrame()

df["Yield"] = [44.0, 43.0, 46.0, 40.1, 42.2]
df["BioMaterial1"]=[5.5, 4.5, 3.5, 1.0, 6.0]
df["BioMaterial2"]=[9.5, 9, 5, 10, 12]
df["ProcessValue1"] = [20, 15, 10, 9, 2]


target = "Yield"

features = ["BioMaterial1", "BioMaterial2", "ProcessValue1"]



df[features]


my_mlflow_model = mlflow_model(model_name="project_name", staging="Staging")



my_mlflow_model.list_registered_models()

my_mlflow_model.get_model_version()

my_mlflow_model.get_model()

my_mlflow_model.get_features()

my_mlflow_model.get_model_artifact(artifact="feature_dtypes.json")

my_mlflow_model.get_model_artifact(artifact="feature_limits.json")

my_mlflow_model.get_model_artifact(artifact="target_limits.json")


my_mlflow_model.get_feature_minmaxscaler()


my_mlflow_model.make_predictions(df)


df["prediction"] = my_mlflow_model.make_predictions(df)

df





df_single = df.iloc[0, :]
df_single = pd.DataFrame(df_single).T
df_single

my_mlflow_model.make_predictions(df_single)[0]


