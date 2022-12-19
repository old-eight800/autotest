from tools import BASE_DIR
import os
import yaml


test_case_path = os.path.join(BASE_DIR,"test_case","UI","test_case.yaml")
with open(test_case_path, "r", encoding="utf-8") as file:
    l = []
    d = {}
    test_case_raw_data = yaml.load(file.read(), Loader=yaml.FullLoader)
    for k,v in test_case_raw_data.items():
        l.append({k:v})
        # d.update(**{k:v})
    # l.append(d)
    print(l)
    print(len(l))
    # print("".format(l))