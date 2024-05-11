# 获取数据，并划分训练集和测试集
import pandas as pd
from sklearn.model_selection import train_test_split
import os


def get_data(data_path):
    data = pd.read_csv(data_path)
    data = data.rename(columns={data.columns[0]: 's1', data.columns[1]: 's2', data.columns[2]: 'label'})
    print(data.columns)
    x = data[['s1', 's2']].values.tolist()
    y = data['label'].values.tolist()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=123, shuffle=True)
    print('总共有数据：{}条，其中正样本：{}条，负样本：{}条'.format(
        len(x), sum(y), len(x) - sum(y)))
    print('训练数据：{}条,其中正样本：{}条，负样本：{}条'.format(
        len(x_train), sum(y_train), len(x_train) - sum(y_train)))
    print('测试数据：{}条,其中正样本：{}条，负样本：{}条'.format(
        len(x_test), sum(y_test), len(x_test) - sum(y_test)))
    return x_train, x_test, y_train, y_test


if __name__ == '__main__':
    x_train, x_test, y_train, y_test = get_data(r'train_data.csv')
