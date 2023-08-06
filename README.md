# mlflow_workflow_app

- link: http://localhost:8050/mlflowapp/landing


# Icons

- free icons: https://www.flaticon.com/de/



## Landing

![landing_content](./assets/landing_page_overview.png)

## Data

![data_overview](./assets/data_page_overview.png)

## Data Preprocessing

### No target selected

![data_selection](./assets/data_select_overview1.png)

### Target selected

![data_selection](./assets/data_select_overview2.png)











It will be neccessary to push your model to this docker compose system. 

## Linux

```

export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;QueueEndpoint=http://localhost:10001/devstoreaccount1"

export MLFLOW_TRACKING_URI="http://localhost:5000"

```

## Windows
```
set AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;QueueEndpoint=http://localhost:10001/devstoreaccount1"


set MLFLOW_TRACKING_URI=http://localhost:5000

```





