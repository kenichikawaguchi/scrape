import pandas as pd
import csv


def get_code_list():
    with open("output.csv") as f:
        code_list = []
        for idx, row in enumerate(csv.reader(f)):
            if idx == 0:
                continue
            code_list.append(row[3])
    return code_list


if __name__ == '__main__':
    code_list = get_code_list()
    print(code_list)
    print(len(code_list))
