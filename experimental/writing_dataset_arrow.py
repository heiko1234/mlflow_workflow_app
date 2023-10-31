




import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pyarrow.compute as pc


import os
import pyarrow.parquet as pq
import pyarrow.fs as fs
from adlfs import AzureBlobFileSystem


from azure.identity import DefaultAzureCredential

from azure.identity.aio import AzureCliCredential



# 


def get_az_account():

    actual_deployment = os.getenv("DEPLOYMENT_ENVIRONMENT", "local")
    if actual_deployment == "local":
        return "local_azurite"
    elif actual_deployment == "dev":
        return "azdev"
    elif actual_deployment == "prod":
        return "azprod"


get_credential = DefaultAzureCredential(exclude_environment_credential=True)

get_credential = AzureCliCredential()


abfs = AzureBlobFileSystem(
    account_name=get_az_account,
    anon=False,
    credential=get_credential
)


file_system = fs.PyFileSystem(fs.FSSpecHandler(abfs))





# load data with dataset 

dataset = ds.dataset('data/ChemicalManufcturingProcess.parquet', format='parquet', partitioning='hive')




ds.write_dataset(dataset, "./data/testdata", format="parquet")








