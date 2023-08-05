
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



data_cleaning_table["description"] = ["Yield", "feature1", "Feature2", "featerue3"]

data_cleaning_table["rule1"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule2"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule3"]=["no cleaning", "remove data", "no cleaning", "no cleaning"]
data_cleaning_table["rule4"]=["remove data", "no cleaning", "no cleaning", "remove data"]
data_cleaning_table["rule5"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule6"]=["no cleaning", "no cleaning", "remove data", "no cleaning"]
data_cleaning_table["rule7"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]
data_cleaning_table["rule8"]=["no cleaning", "no cleaning", "no cleaning", "no cleaning"]



data_cleaning_table

# >>> data_cleaning_table
#   description        rule1        rule2        rule3        rule4        rule5        rule6        rule7        rule8
# 0       Yield  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning
# 1    feature1  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning  no cleaning
# 2    Feature2  no cleaning  no cleaning  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning
# 3   featerue3  no cleaning  no cleaning  no cleaning  remove data  no cleaning  no cleaning  no cleaning  no cleaning





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




transform_cleaning_table_in_dict(dataframe=data_cleaning_table)



# TODO load data, remove data via new function with the dictionary for data clenaing







