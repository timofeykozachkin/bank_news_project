import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler
from model.lstm import LSTMModel


def preprocess_stock_data(stock_name, sent_score, home_path='/Users/kozachkin/vkr'):
    df_stocks_targets_reg = pd.read_excel(f'{home_path}/app/data/{stock_name}.xlsx', header=1)[['Дата', 'Avg']].tail(11)
    pred_data = add_shifts_and_filter(df_stocks_targets_reg, 'Avg', date_feature='Дата').iloc[-1, 1:-1].to_numpy()
    sc = MinMaxScaler()
    model = LSTMModel(1, 1)
    model.load_state_dict(torch.load(f'{home_path}/app/model/{stock_name.lower()}_model.pt',
                                     map_location=torch.device('cpu')))

    tensor_pred_data = torch.tensor(
        np.concatenate(
            [sc.fit_transform(pred_data.reshape(-1, 1)), np.array([[sent_score]])], axis=0),
        dtype=torch.float32).unsqueeze(dim=0)

    model.eval()
    with torch.no_grad():
        outputs = model(tensor_pred_data).squeeze()

    pred = float(sc.inverse_transform(outputs.unsqueeze(dim=0).numpy().reshape(-1, 1)).squeeze())
    if pred >= pred_data[0]:
        pred_cat = '↑ up'
    else:
        pred_cat = '↓ down'
    return pred, pred_cat


def add_shifts_and_filter(df, target, multi_bank_series_feature=None, date_feature='date', dropna=True,
                          reg_data_for_cls_task=None):
    data = df.copy()

    if not multi_bank_series_feature:
        if reg_data_for_cls_task is None:
            for i in range(1, 11):
                data[f'{target}_shift{i}'] = data[target].shift(i)
        else:
            for i in range(1, 11):
                data[f'{target}_shift{i}'] = reg_data_for_cls_task[target].shift(i)
        data = data.loc[:, [date_feature,
                            *data.columns[data.columns.str.contains(target)].tolist()]]

    else:
        data['occurence'] = data.groupby([multi_bank_series_feature]).cumcount() + 1
        for i in range(1, 11):
            data['prev'] = data['occurence'] - i
            data = data.merge(data[[multi_bank_series_feature, target, 'occurence']],
                              how='left', left_on=[multi_bank_series_feature, 'prev'],
                              right_on=[multi_bank_series_feature, 'occurence'],
                              suffixes=('', f'_shift{i}')).drop(columns=['prev', f'occurence_shift{i}'])
        data = data.loc[:, [multi_bank_series_feature, date_feature,
                            *data.columns[data.columns.str.contains(target)].tolist()]]

    if dropna:
        return data.dropna()
    else:
        return data
