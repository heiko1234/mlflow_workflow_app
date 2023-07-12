

from upath import UPath



path = UPath("az://coinbasedata/",
        account_name="local_azurite", anon=False)


path = UPath("az://coinbasedata/coinbasedata/",
        account_name="local_azurite", anon=False)

[p for p in path.iterdir()]



from azure.identity import DefaultAzureCredential


credential = DefaultAzureCredential(exclude_environment_credential=True)


path = UPath("az://coinbasedata/coinbasedata/", account_name="local_azurite", anon=False, credential=credential)

[p for p in path.iterdir()]




