

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
get_account


# credentials: choose one

get_credential = DefaultAzureCredential(exclude_environment_credential=True)

get_credential = AzureCliCredential()


abfs = AzureBlobFileSystem(
    account_name=get_account,
    anon=False,
    credential=get_credential
)


file_system = fs.PyFileSystem(fs.FSSpecHandler(abfs))


container_name = "coinbasedata"
subcontainer_name = "coinbasedata"
file_name = "coinbase_data.parquet"


file_path = f"{container_name}/{subcontainer_name}/{file_name}"



df = pq.ParquetDataset(file_path, filesystem=file_system).read_pandas().to_pandas()
df




