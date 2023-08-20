


import pandas as pd



df = pd.DataFrame()

df["Yield"] = [44.0, 43.0, 46.0, 40.1, 42.2]
df["BioMaterial1"]=[5.5, 4.5, 3.5, 1.0, 6.0]
df["BioMaterial2"]=[9.5, 9, 5, 10, 12]
df["ProcessValue1"] = [20, 15, 10, 9, 2]


df
# >>> df
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   44.0           5.5           9.5             20
# 1   43.0           4.5           9.0             15
# 2   46.0           3.5           5.0             10
# 3   40.1           1.0          10.0              9
# 4   42.2           6.0          12.0              2




dd_list = ["Yield", "BioMaterial1", "BioMaterial2", "ProcessValue1"]

target_and_features = ["Yield", "BioMaterial1", "BioMaterial2", "ProcessValue1"]



df = df[dd_list]


dft=df.describe().reset_index(drop = True).T
dft = dft.reset_index(drop=False)
dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
dft["nan"]=df.isna().sum().values

dft

# >>> dft
#      description  counts   mean       std   min   25%   50%   75%   max  nan
# 0          Yield     5.0  43.06  2.181284  40.1  42.2  43.0  44.0  46.0    0
# 1   BioMaterial1     5.0   4.10  1.981161   1.0   3.5   4.5   5.5   6.0    0
# 2   BioMaterial2     5.0   9.10  2.559297   5.0   9.0   9.5  10.0  12.0    0
# 3  ProcessValue1     5.0  11.20  6.760178   2.0   9.0  10.0  15.0  20.0    0




# Kleinere Tabelle


datatable = pd.DataFrame()

datatable["description"] = ["Yield", "BioMaterial1", "BioMaterial2", "ProcessValue1"]
datatable["usage"] = ["target", "feature", "feature", "feature"]
datatable["max"]= [46.5, 6.0, 10.0, 20]
datatable["min"] = [40, 1.0, 5.0, 1.66]
datatable["std"] = [1, 1.0, 0.5, 5]


datatable

# >>> datatable
#      description    usage   max    min
# 0          Yield   target  46.5  40.00
# 1   BioMaterial1  feature   6.0   1.00
# 2   BioMaterial2  feature  10.0   5.00
# 3  ProcessValue1  feature  20.0   1.66


datatable.loc[0, "description"]



# original use of minmax, with original dataframe

from sklearn.preprocessing import MinMaxScaler

instance_minmaxscaler = MinMaxScaler()


instance_minmaxscaler.fit(df.loc[:,target_and_features])


fitted_df = instance_minmaxscaler.transform(df.loc[:,target_and_features])

fitted_df

# >>> fitted_df
# array([[0.66101695, 0.9       , 0.64285714, 1.        ],
#        [0.49152542, 0.7       , 0.57142857, 0.72222222],
#        [1.        , 0.5       , 0.        , 0.44444444],
#        [0.        , 0.        , 0.71428571, 0.38888889],
#        [0.3559322 , 1.        , 1.        , 0.        ]])


# update


def make_minmaxscalingtable_by_descriptiontable(descriptiontable, expand_by=None):
    
    output_df = pd.DataFrame()
    
    if expand_by is None:
        
        for row_index in range(descriptiontable.shape[0]):
            output_df[descriptiontable.loc[row_index, "description"]] = [descriptiontable.loc[row_index, "max"], descriptiontable.loc[row_index, "min"]]

    elif expand_by is "std":
            
            for row_index in range(descriptiontable.shape[0]):
                output_df[descriptiontable.loc[row_index, "description"]] = [descriptiontable.loc[row_index, "max"]+ descriptiontable.loc[row_index, "std"], descriptiontable.loc[row_index, "min"]- descriptiontable.loc[row_index, "std"]]


    return output_df



new_minmaxscalingdf = make_minmaxscalingtable_by_descriptiontable(descriptiontable=datatable, expand_by="std")
new_minmaxscalingdf



new_minmaxscalingdf = make_minmaxscalingtable_by_descriptiontable(descriptiontable=datatable, expand_by=None)
new_minmaxscalingdf

# >>> new_minmaxscalingdf
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   46.5           6.0          10.0          20.00
# 1   40.0           1.0           5.0           1.66



from sklearn.preprocessing import MinMaxScaler

instance_minmaxscaler_new = MinMaxScaler()


instance_minmaxscaler_new.fit(new_minmaxscalingdf.loc[:, target_and_features])


fitted_df_new = instance_minmaxscaler_new.transform(df.loc[:,target_and_features])

fitted_df_new

# >>> new_minmaxscalingdf
#    Yield  BioMaterial1  BioMaterial2  ProcessValue1
# 0   46.5           6.0          10.0          20.00
# 1   40.0           1.0           5.0           1.66

# >>> fitted_df_new
# array([[0.61538462, 0.9       , 0.9       , 1.        ],
#        [0.46153846, 0.7       , 0.8       , 0.72737186],
#        [0.92307692, 0.5       , 0.        , 0.45474373],
#        [0.01538462, 0.        , 1.        , 0.4002181 ],
#        [0.33846154, 1.        , 1.4       , 0.01853871]])



# >>> dft
#      description  counts   mean       std   min    max  
# 0          Yield     5.0  43.06  2.181284  40.1   46.0
# 1   BioMaterial1     5.0   4.10  1.981161   1.0    6.0
# 2   BioMaterial2     5.0   9.10  2.559297   5.0   12.0
# 3  ProcessValue1     5.0  11.20  6.760178   2.0   20.0



# >>> fitted_df
# array([[0.66101695, 0.9       , 0.64285714, 1.        ],
#        [0.49152542, 0.7       , 0.57142857, 0.72222222],
#        [1.        , 0.5       , 0.        , 0.44444444],
#        [0.        , 0.        , 0.71428571, 0.38888889],
#        [0.3559322 , 1.        , 1.        , 0.        ]])





