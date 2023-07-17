


from lib2to3.pytree import Base
from operator import sub
import os
import io
from pathlib import Path

import pandas as pd


from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient


from dotenv import load_dotenv

load_dotenv()



def azurite_resource(init_context):
    storage_account = "devstoreaccount1"
    credential = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
    return AzuriteResource(storage_account, credential)


class AzuriteResource:
    def __init__(self, storage_account, credential):
        connection_string = ";".join(
            [
                "DefaultEndpointsProtocol=http",
                f"AccountName={storage_account}",
                f"AccountKey={credential}",
                f"DefaultEndpointsProtocol=http",
                f"BlobEndpoint=http://127.0.0.1:10000/{storage_account}",
                f"QueueEndpoint=http://127.0.0.1:10001/{storage_account}",
            ]
        )
        self._blob_client = BlobServiceClient.from_connection_string(connection_string)

    @property
    def blob_client(self):
        return self._blob_client


class BlobStorageConnector:
    def __init__(self, container_name):
        self.__container = container_name

        # self._connection_string = None
        connection_string_str = None


        try:
            connection_string_str  = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            account_name = os.getenv("AZURE_STORAGE_NAME")
            account_key = os.getenv("AZURE_STOREAGE_KEY")
        except BaseException:
            connection_string_str  = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
            account_name = os.environ["AZURE_STORAGE_NAME"]
            account_key = os.environ("AZURE_STOREAGE_KEY")

        if connection_string_str is not None:
            self._connection_string = connection_string_str 

        else:
            self._connection_string = ";".join(
                [
                    "DefaultEndpointsProtocol=http",
                    f"AccountName={account_name}",
                    f"AccountKey={account_key}",
                    f"DefaultEndpointsProtocol=http",
                    f"BlobEndpoint=http://127.0.0.1:10000/{account_name}",
                    f"QueueEndpoint=http://127.0.0.1:10001/{account_name}",
                ]
            )

    def get_container_client(self):
        blob_container_client = ContainerClient.from_connection_string(
            self._connection_string, container_name=self.__container
        )
        return blob_container_client

    def list_files_in_subcontainer(self, subcontainer, files_with):
        output = []
        for blob in self.get_container_client().list_blobs():
            if subcontainer in blob.name and files_with in blob.name:
                output.append(blob.name.split("/")[1])
        return output

    def get_parquet_file(self, subcontainer, file):

        blob_str = subcontainer + "/" + file
        bytes = (
            self.get_container_client()
            .get_blob_client(blob=blob_str)
            .download_blob()
            .readall()
        )
        pq_file = io.BytesIO(bytes)
        df = pd.read_parquet(pq_file)
        return df

    def get_csv_file(self, subcontainer, file):

        blob_str = subcontainer + "/" + file
        bytes = (
            self.get_container_client()
            .get_blob_client(blob=blob_str)
            .download_blob()
            .readall()
        )
        pq_file = io.BytesIO(bytes)
        df = pd.read_csv(pq_file, sep=";")
        return df


def get_container_client(container_name="azuriteblob"):
    return BlobStorageConnector(container_name=container_name).get_container_client()


def get_list_files_in_subcontainer(
    container_name="azuriteblob", subcontainer="targetfolder", file=".csv"
):

    output = []

    for blob in get_container_client(container_name=container_name).list_blobs():
        if subcontainer in blob.name and file in blob.name:
            output.append(blob.name.split("/")[1])
    return output


def read_parquet_file(
    container_name="azuriteblob", blob="targetfolder", file=".parquet"
):

    blob_str = blob + "/" + file
    bytes = (
        BlobStorageConnector(container_name=container_name)
        .get_container_client()
        .get_blob_client(blob=blob_str)
        .download_blob()
        .readall()
    )
    pq_file = io.BytesIO(bytes)
    df = pd.read_parquet(pq_file)
    return df


def read_csv_file(container_name="azuriteblob", blob="targetfolder", file=".csv"):

    blob_str = blob + "/" + file
    bytes = (
        BlobStorageConnector(container_name=container_name)
        .get_container_client()
        .get_blob_client(blob=blob_str)
        .download_blob()
        .readall()
    )
    csv_file = io.BytesIO(bytes)
    df = pd.read_csv(csv_file, sep=";")
    return df


def upload_data_to_blob(df, container_name, subcontainer_name, filename, filetype="parquet"):

    relativ_filepath = f"./data/{subcontainer_name}/{filename}.{filetype}"
    file = Path(relativ_filepath)
    file
    dir_to_create = file.parent
    os.makedirs(dir_to_create, exist_ok=True)

    if filetype == "parquet":
        df.to_parquet(relativ_filepath)
    if filetype== "csv":
        df.to_csv(relativ_filepath)

    print(f"Successfully intermediate save {relativ_filepath} locally")

    blob_str = f"{subcontainer_name}/{filename}.{filetype}"

    client = (BlobStorageConnector(container_name=container_name)
        .get_container_client()
        .get_blob_client(blob=blob_str)
        )

    print(os.path.isfile(file))
    
    file.open("rb")
    
    with file.open("rb") as data:
        client.upload_blob(data, overwrite=True)
    
    print(f"successfully written {filename} in blob")

    # remove temporar file path
    Path(relativ_filepath).unlink()
    print(f"successfully deleted local file: {file}")





get_list_files_in_subcontainer(
    container_name="coinbasedata",
    subcontainer="coinbasedata",
    file=".parquet")



get_list_files_in_subcontainer(container_name="coinbasedata", subcontainer="datadownload", file=".parquet")
# ['rawdata.parquet']

get_list_files_in_subcontainer(container_name="coinbasedata", subcontainer="coinbasedata", file=".parquet")
# ['coinbase_data.parquet']








