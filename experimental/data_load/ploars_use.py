




import polars as pl
import os



from dotenv import load_dotenv


load_dotenv()



account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
account_key = os.getenv("AZURE_ACCOUNT_KEY")

account_name
account_key




url = f"https://{account_name}.blob.core.windows.net"

# load data from azurite blobcontainer "chemical-data" via polars


df = pl.read_parquet("https://{account_name}.blob.core.windows.net/chemical-data/chemical-data/ChemicalManufacturingData.parquet")





from azure.identity import DefaultAzureCredential


credential = DefaultAzureCredential(exclude_environment_credential=True)
credential




# ###################


from upath import UPath

from azure.identity import DefaultAzureCredential


credential = DefaultAzureCredential(exclude_environment_credential=True)


path = UPath("az://chemical-data/chemical-data/", account_name="devstoreaccount1", anon=True, credential=credential)


[p for p in path.iterdir()]








