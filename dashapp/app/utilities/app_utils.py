
import os


from dotenv import load_dotenv

load_dotenv()

local_run = os.getenv("LOCAL_RUN")
local_run


def get_option_list(a_list):
    cnames_data = a_list
    options_list = []
    for i in cnames_data:
        options_list.append({"label": i, "value": i})
    return options_list

