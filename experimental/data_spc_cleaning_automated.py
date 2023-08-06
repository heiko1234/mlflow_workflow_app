




import pandas as pd

from dashapp.app.utilities.spc import (
    transform_cleaning_table_in_dict,
    use_spc_cleaning_dict,
    create_limits_dict,
    update_nested_dict,
    filter_dataframe_by_limits
)



data_cleaning_table = pd.DataFrame()






data_cleaning_table["description"] = ["Yield", "BiologicalMaterial04", "ManufacturingProcess05", "featerue3"]

data_cleaning_table["rule1"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule2"]=["remove data", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule3"]=["no cleaning", "remove data", "no cleaning", "no cleaning"]
data_cleaning_table["rule4"]=["remove data", "no cleaning", "remove data", "remove data"]
data_cleaning_table["rule5"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule6"]=["no cleaning", "no cleaning", "remove data", "no cleaning"]
data_cleaning_table["rule7"]=["no cleaning", "remove data", "no cleaning", "no cleaning"]
data_cleaning_table["rule8"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]



data_cleaning_table


spc_cleaning_dict=transform_cleaning_table_in_dict(dataframe=data_cleaning_table)
spc_cleaning_dict



df = pd.read_parquet("data/ChemicalManufacturingProcess.parquet")



limits_table_df =  df.describe().T
limits_table_df



data = df


output_df = use_spc_cleaning_dict(dataframe=data, spc_cleaning_dict=spc_cleaning_dict)
output_df




limits_dict = create_limits_dict(limits_table_df=limits_table_df)
limits_dict

limits_dict

update_limits_dict = {
    "Yield": {
        "min": 40,
        "max": 43,
    },
}

limits_dict["Yield"]
# >>> limits_dict["Yield"]
# {'mean': 40.4296511627907, 'std': 2.0107209404615047, 'min': 40, 'max': 43}


limits_dict_new = update_nested_dict(original_dict=limits_dict, overwrite_dict=update_limits_dict)

limits_dict_new
limits_dict_new["Yield"]

# >>> limits_dict_new["Yield"]
# {'mean': 40.4296511627907, 'std': 2.0107209404615047, 'min': 40, 'max': 43}




# raw data
data
# data.shape  # 86, 58


# prefiltered data
output_df
output_df.shape  # 23, 58


output_df_filtered_limits = filter_dataframe_by_limits(dataframe=output_df, limits_dict=limits_dict_new)

output_df_filtered_limits
output_df_filtered_limits.shape  # 11, 58




