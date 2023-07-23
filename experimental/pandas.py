




import pandas as pd


# create a function to make a print statement for a dataframe

df = pd.read_parquet("/home/heiko/Repos/dash_apps/mlflow_workflow_app/data/ChemicalManufcturingProcess.parquet")

df

df.head()

dft=df.describe().reset_index(drop = True).T
dft = dft.reset_index(drop=False)
dft
dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
dft["nan"]=df.isna().sum().values
dft.head()
#             description  counts       mean       std    min      25%    50%      75%    max
# 0                 Yield    86.0  40.429651  2.010721  35.25  39.0275  40.11  41.9450  46.34
# 1  BiologicalMaterial01    86.0   6.613023  0.610227   5.17   6.2725   6.65   6.9400   8.81
# 2  BiologicalMaterial02    86.0  57.094302  3.702737  51.28  54.1400  57.03  60.1675  64.75

# get number of nan values per column
df.isna().sum()


## ############




df = pd.DataFrame()

df["a"] = [1,2,3,4,5]

df["string_a"]= ["1","2","3","4","5"]

print(df)

def add_colum_b(df, column_name="a"):

    df[f"{column_name}_2"] = df[column_name] * df[column_name]
    return df



print(df)

df = add_colum_b(df=df, column_name="a")
df = add_colum_b(df=df, column_name="string_a")


print(df)



# ###################

variable_a = "a"

variable_a_2 = "a_2"

f"{variable_a}_2"

f"{variable_a}/{variable_a}"


# ###################
{}
()
[]


["a","b","c"]

[f"{variable_a}", "b", "c"]

list_a = ["a","b","c", "1", 5]


for element in list_a:
    try:
        print(int(element))
    except BaseException as e:
        print(f"Fehlermeldung: {e}")


int("1")
float("1.0")

int("a")

str(5)

int(str(5))

for element in list_a:
    try:
        print(str(element))
    except BaseException as e:
        print(f"BaseExeption: {e}")



eng_dict = {"here": "hier", "there": "da", "where": "wo"}

eng_dict["here"]  # "hier"
eng_dict["hier"]





a_dict = {"a": 1, "b": 2, "c": 3}
a_dict


a_dict["a"]  # 1
a_dict["b"]  # 2
a_dict["d"]   # key error

list_a = ["a","b","c", "1", 5]


for element_from_list_a in list_a:
    try:
        print(
            a_dict[element_from_list_a]
        )
    except:
        print(
            int(element_from_list_a)
        )


print("afujhtgfd")

int("13")


#  # ############

list_a = ["a","b","c", "4", 5]
a_dict = {"a": 1, "b": 4, "c": 3}


def my_for_loop(list_a, a_dict):
    output = []
    for element in list_a:
        try:
            output.append(
                a_dict[element]
            )
        except:
            output.append(
                int(element)
            )

    return output



my_for_loop(list_a=list_a, a_dict=a_dict)







