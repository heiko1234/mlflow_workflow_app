
# TODO



import pandas as pd



data_cleaning_table = pd.DataFrame()




# What should be included in the data cleaning table?


# dft=df.describe().reset_index(drop = True).T
# dft = dft.reset_index(drop=False)
# dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
# dft["nan"]=df.isna().sum().values

# dft = dft.drop(["25%", "50%", "75%"], axis=1)

# dft["rule1"] = "no cleaning"
# dft["rule2"] = "no cleaning"
# dft["rule3"] = "no cleaning"
# dft["rule4"] = "no cleaning"
# dft["rule5"] = "no cleaning"
# dft["rule6"] = "no cleaning"
# dft["rule7"] = "no cleaning"
# dft["rule8"] = "no cleaning"


# dft["transformation"] = "no transformation"


# data_transformations = [
#     {"label": "no transformation", "value": "no transformation"},
#     {"label": "log", "value": "log"},
#     {"label": "sqrt", "value": "sqrt"},
#     {"label": "1/x", "value": "1/x"},
#     {"label": "x^2", "value": "x^2"},
#     {"label": "x^3", "value": "x^3"},



# spc_rules = [
#     {"label": "no cleaning", "value": "no cleaning"},
#     {"label": "remove data", "value": "data"},
# ]



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

# >>> data_cleaning_table
#   description        rule1        rule2        rule3        rule4        rule5        rule6        rule7        rule8
# 0       Yield  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning
# 1    feature1  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning  no cleaning
# 2    Feature2  no cleaning  no cleaning  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning
# 3   featerue3  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning


#               description        rule1        rule2        rule3        rule4        rule5        rule6        rule7        rule8
# 0                   Yield  no cleaning  remove data  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning
# 1    BiologicalMaterial04  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  remove data  no cleaning
# 2  ManufacturingProcess05  no cleaning  no cleaning  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning
# 3               featerue3  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning



def transform_cleaning_table_in_dict(dataframe):
    """ This function gives a dictionary of the usage of the rules for each feature in the data cleaning table

    Args:
        dataframe (_type_): pandas dataframe

    Returns:
        _type_: returns a dictionary with separated rules for each feature
    """
    
    dict = {}
    
    list_of_rules = ["rule1", "rule2", "rule3", "rule4", "rule5", "rule6", "rule7", "rule8"]

    for element_in_description in dataframe["description"].unique():
        dict[element_in_description] = {}
        
        for rule in list_of_rules:
            if rule  in dataframe.columns:
                dict[element_in_description][rule] = dataframe.loc[dataframe["description"]==element_in_description][rule].values[0]
                
    return dict




spc_cleaning_dict=transform_cleaning_table_in_dict(dataframe=data_cleaning_table)
spc_cleaning_dict


# TODO load data, remove data via new function with the dictionary for data clenaing




import pandas as pd

from dashapp.app.utilities.plots import (
    control_chart,
    control_chart_marginal
)


df = pd.read_parquet("data/ChemicalManufacturingProcess.parquet")



limits_table_df =  df.describe().T
limits_table_df

#                         count         mean          std       min        25%       50%        75%       max
# Yield                    86.0    40.429651     2.010721    35.250    39.0275    40.110    41.9450    46.340
# BiologicalMaterial01     86.0     6.613023     0.610227     5.170     6.2725     6.650     6.9400     8.810
# BiologicalMaterial02     86.0    57.094302     3.702737    51.280    54.1400    57.030    60.1675    64.750
# BiologicalMaterial03     86.0    69.384535     3.826193    60.990    66.5000    69.800    72.0075    78.250


control_chart_marginal(data=df, y_name="Yield", show=True)
control_chart_marginal(data=df, y_name="BiologicalMaterial04", show=True)



data=df

data.columns

# Index(['Yield', 'BiologicalMaterial01', 'BiologicalMaterial02',
#        'BiologicalMaterial03', 'BiologicalMaterial04', 'BiologicalMaterial05',
#        'BiologicalMaterial06', 'BiologicalMaterial07', 'BiologicalMaterial08',
#        'BiologicalMaterial09', 'BiologicalMaterial10', 'BiologicalMaterial11',
#        'BiologicalMaterial12', 'ManufacturingProcess01',
#        'ManufacturingProcess02', 'ManufacturingProcess03',
#        'ManufacturingProcess04', 'ManufacturingProcess05',
#        'ManufacturingProcess06', 'ManufacturingProcess07',
#        'ManufacturingProcess08', 'ManufacturingProcess09',
#        'ManufacturingProcess10', 'ManufacturingProcess11',
#        'ManufacturingProcess12', 'ManufacturingProcess13',


from dashapp.app.utilities.nelson import (
    rule1,
    rule2,
    rule3,
    rule4,
    rule5,
    rule6,
    rule7,
    rule8,
)


rule1(original=data["Yield"])
rule2(original=data["Yield"])


y_name="Yield"
data.loc[rule1(original=data[y_name]), y_name]
data.loc[rule2(original=data[y_name]), y_name]

df_d = pd.DataFrame(data.loc[rule2(original=data[y_name]), y_name])
df_d.index


spc_cleaning_dict.keys()
spc_cleaning_dict["Yield"]




def use_spc_cleaning_dict(dataframe, spc_cleaning_dict):

    list_all_indexes = []

    for any_column in spc_cleaning_dict.keys():
        try:
            if any_column in dataframe.columns:
                for any_rule in spc_cleaning_dict[any_column].keys():
                    if spc_cleaning_dict[any_column][any_rule] != "no cleaning":
                        try:
                            
                            print(f"any_column: {any_column}")
                            print(f"any_rule: {any_rule}")
                            # print(dataframe.loc[eval(any_rule+"(original=dataframe[any_column])"), any_column])
                            # list_all_indexes.append(dataframe.loc[eval(any_rule+"(original=dataframe[any_column])"), any_column].index)
                            index_list_rule = dataframe.loc[eval(any_rule+"(original=dataframe[any_column])"), any_column].index
                            if len(index_list_rule) > 0:
                                list_all_indexes.extend(index_list_rule)

                        except BaseException as be:
                            print(be)
                            pass
        except Exception as e:
            print(e)
            pass


    unique_list_all_indexes = list(set(list_all_indexes))

    dataframe_output = dataframe.drop(index=unique_list_all_indexes, axis=0)

    return dataframe_output





data.head()
spc_cleaning_dict.keys()
spc_cleaning_dict["Yield"]
spc_cleaning_dict["Yield"]["rule1"]
spc_cleaning_dict["BiologicalMaterial04"]
spc_cleaning_dict["ManufacturingProcess05"]
spc_cleaning_dict["featerue3"]


# using this function


# dropping_indexes = use_spc_cleaning_dict(dataframe=data, spc_cleaning_dict=spc_cleaning_dict)
# dropping_indexes
# list(dropping_indexes)

# list(set(dropping_indexes))

# transform a list of index into a list of values



output_df = use_spc_cleaning_dict(dataframe=data, spc_cleaning_dict=spc_cleaning_dict)
output_df


data.shape  # 86, 58
data.index  # RangeIndex(start=0, stop=86, step=1)  



control_chart_marginal(data=output_df.reset_index(drop = True), y_name="Yield", show=True)










limits_table_df



# >>> limits_table_df
#                         count         mean          std       min        25%       50%        75%       max
# Yield                    86.0    40.429651     2.010721    35.250    39.0275    40.110    41.9450    46.340
# BiologicalMaterial01     86.0     6.613023     0.610227     5.170     6.2725     6.650     6.9400     8.810
# BiologicalMaterial02     86.0    57.094302     3.702737    51.280    54.1400    57.030    60.1675    64.750
# BiologicalMaterial03     86.0    69.384535     3.826193    60.990    66.5000    69.800    72.0075    78.250
# BiologicalMaterial04     86.0    12.893721     1.854061     9.990    11.9550    12.590    13.4275    23.090
# BiologicalMaterial05     86.0    18.790116     1.924213    15.460    17.2275    18.660    20.2800    24.850





# create function to create a dictionary of mean, std, min and max limits for each row based on the limits_table_df

def create_limits_dict(limits_table_df):
    limits_dict = {}

    for each_row in limits_table_df.index:
        limits_dict[each_row] = {
            "mean": limits_table_df.loc[each_row, "mean"],
            "std": limits_table_df.loc[each_row, "std"],
            "min": limits_table_df.loc[each_row, "min"],
            "max": limits_table_df.loc[each_row, "max"],
        }
        
    return limits_dict



limits_dict = create_limits_dict(limits_table_df=limits_table_df)
limits_dict



# create funciton that filter a dataframe by using the min and max values for each column based on the entries of the limits_dict

def filter_dataframe_by_limits(dataframe, limits_dict):
    filtered_dataframe = dataframe.copy()
    for each_column in dataframe.columns:
        if each_column in limits_dict.keys():
            filtered_dataframe = filtered_dataframe.loc[(filtered_dataframe[each_column] >= limits_dict[each_column]["min"]) & (filtered_dataframe[each_column] <= limits_dict[each_column]["max"]), :]
        else:
            print(f"column {each_column} not in limits_dict.keys()")
            pass
    return filtered_dataframe 



# function to updated nested dictionaries


import collections

def update_nested_dict(original_dict, overwrite_dict):
    
    
    for k, v in overwrite_dict.items():
        if isinstance(v, collections.abc.Mapping):
            original_dict[k] = update_nested_dict(original_dict.get(k, {}), v)
        else:
            original_dict[k] = v
            
    return original_dict



limits_dict

update_limits_dict = {
    "Yield": {
        "min": 40,
        "max": 43,
    },
}

limits_dict["Yield"]

limits_dict_new = update_nested_dict(original_dict=limits_dict, overwrite_dict=update_limits_dict)

limits_dict_new
limits_dict_new["Yield"]



output_df


output_df_filtered_limits = filter_dataframe_by_limits(dataframe=output_df, limits_dict=limits_dict_new)

output_df_filtered_limits












