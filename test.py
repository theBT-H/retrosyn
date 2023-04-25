import numpy as np
import pandas as pd

from learn_flask.service import getMax2Structure


def calculate_accuracy(data_path):
    # 读取数据集
    data = pd.read_csv(data_path)
    # 随机选择 10% 的数据进行预测
    num_samples = int(np.ceil(len(data) * 0.1))
    random_indices = np.random.choice(len(data), num_samples, replace=False)
    # 初始化正确预测的数量
    correct_predictions = 0
    # 对每一行进行预测，prod_smiles为目标产物，rxn_smiles为正确的反应物
    for index, row in data.iloc[random_indices].iterrows():
        now = row['prod_smiles']
        rxn_smiles = row['rxn_smiles'].split(',')
        res = getMax2Structure(now)
        if set(res) == set(rxn_smiles):
            correct_predictions += 1
    # 计算准确率
    accuracy = correct_predictions / num_samples
    print("accuracy = {} with total samples {}".format(accuracy, num_samples))
    return accuracy