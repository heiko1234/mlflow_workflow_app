



import os
import pyarrow.parquet as pq
import pyarrow.fs as fs
from adlfs import AzureBlobFileSystem


from azure.identity import DefaultAzureCredential

from azure.identity.aio import AzureCliCredential





def get_az_account():

    actual_deployment = os.getenv("DEPLOYMENT_ENVIRONMENT", "local")
    if actual_deployment == "local":
        return "local_azurite"
    elif actual_deployment == "dev":
        return "azdev"
    elif actual_deployment == "prod":
        return "azprod"


get_account = get_az_account()
get_account    #  local_azurte


# credentials: choose one

# get_credential = DefaultAzureCredential(exclude_environment_credential=True)

get_credential = AzureCliCredential()


# get azure credential from azure connection string
from azure.storage.blob import BlobServiceClient
account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

connection_string = ";".join(
            [
                "DefaultEndpointsProtocol=http",
                f"AccountName={account_name}",
                f"AccountKey={account_key}",
                f"DefaultEndpointsProtocol=http",
                f"BlobEndpoint=http://127.0.0.1:10000/{account_name}",
                f"QueueEndpoint=http://127.0.0.1:10001/{account_name}",
            ]
        )
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
get_credential = blob_service_client.credential




get_credential

# abfs = AzureBlobFileSystem(
#     account_name=get_account,
#     anon=False,
#     credential=get_credential
# )


# file_system = fs.PyFileSystem(fs.FSSpecHandler(abfs))



#univeral pahlib
from upath import UPath

path = UPath("az://", account_name = get_account, credential = get_credential)


[str(p) for p in path.iterdir()]


