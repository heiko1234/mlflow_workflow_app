


# https://arrow.apache.org/cookbook/py/io.html



# load data with pyarrow dataset and a pyarrow dataset scanner to filtre data in one column to substrings

import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pyarrow.compute as pc


# load data with dataset 

dataset = ds.dataset('data/ChemicalManufcturingProcess.parquet', format='parquet', partitioning='hive')


# dataset.to_table().to_pandas()
# dataset.to_table().to_pandas().columns


# Hilfe to implement
# test_string = "Yield_1"
# pc.match_substring(pc.field("Yield"), test_string)



#create dataset scanner
# pc.match_substring(pc.field("Yield"), "Yield_1")


pc.field("Yield")

pc.match_substring(pc.field("Yield"), "7.8")

dataset.scanner()

generator = dataset.scanner().to_batches()

generator
# <generator object at 0x7f18fe833cc0>

dataset.scanner().to_batches()
dataset.scanner().to_table().to_pandas()

# >>> dataset.scanner().to_table().to_pandas()
#     Yield  BiologicalMaterial01  BiologicalMaterial02  ...  ManufacturingProcess43  ManufacturingProcess44  ManufacturingProcess45
# 0   43.12                  7.48                 64.47  ...                     0.7                     2.0                     2.2
# 1   43.06                  6.94                 63.60  ...                     0.8                     2.0                     2.2


# dataset.scanner(pc.match_substring(pc.field("Yield"), "7.8")).to_table().to_pandas()

dataset.filter(pc.match_substring(pc.field("Yield"), "7.8")).to_table().to_pandas()



df = dataset.to_table().to_pandas()
df
# a list with 80 times the string "bbb"

repeated_list = ["bbb"] * 80
repeated_list

filter_series = ["baaa", "aa2c", "ab4aa", "abaaa", "aa3bbaaa", "qaaa", *repeated_list]
filter_series
len(filter_series)

df["Filter"] = filter_series
df


# save df as parquet file to data folder
df.to_parquet("data/ChemicalManufcturingProcess_filtred.parquet")


dataset = ds.dataset('data/ChemicalManufcturingProcess_filtred.parquet', format='parquet', partitioning='hive')

dataset.filter(pc.match_substring(pc.field("Filter"), "aa")).to_table().to_pandas()
# >>> dataset.filter(pc.match_substring(pc.field("Filter"), "aa")).to_table().to_pandas()
#    Yield  BiologicalMaterial01  BiologicalMaterial02  BiologicalMaterial03  ...  ManufacturingProcess43  ManufacturingProcess44  ManufacturingProcess45    Filter
# 0  43.12                  7.48                 64.47                 72.41  ...                     0.7                     2.0                     2.2      baaa
# 1  43.06                  6.94                 63.60                 72.06  ...                     0.8                     2.0                     2.2      aa2c


dataset.scanner(filter=pc.match_substring(pc.field("Filter"), "aa")).to_table().to_pandas()

#    Yield  BiologicalMaterial01  BiologicalMaterial02  BiologicalMaterial03  ...  ManufacturingProcess43  ManufacturingProcess44  ManufacturingProcess45    Filter
# 0  43.12                  7.48                 64.47                 72.41  ...                     0.7                     2.0                     2.2      baaa
# 1  43.06                  6.94                 63.60                 72.06  ...                     0.8                     2.0                     2.2      aa2c




generator = dataset.scanner(filter=pc.match_substring(pc.field("Filter"), "aa")).to_batches()
for record_batch in generator:
    # print(record_batch)
    ds.write_dataset(record_batch, "./data/partitioned", format="parquet")



dataset_pat = ds.dataset('./data/partitioned', format='parquet', partitioning='hive')

dataset_pat.to_table().to_pandas()

#    Yield  BiologicalMaterial01  BiologicalMaterial02  BiologicalMaterial03  ...  ManufacturingProcess43  ManufacturingProcess44  ManufacturingProcess45    Filter
# 0  43.12                  7.48                 64.47                 72.41  ...                     0.7                     2.0                     2.2      baaa
# 1  43.06                  6.94                 63.60                 72.06  ...                     0.8                     2.0                     2.2      aa2c
# 2  41.49                  6.94                 63.60                 72.06  ...                     0.9                     1.9                     2.1     ab4aa




