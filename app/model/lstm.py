import torch.nn as nn


class LSTMModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=input_size, hidden_size=50, batch_first=True)
        self.dropout1 = nn.Dropout(0.15)
        self.lstm2 = nn.LSTM(input_size=50, hidden_size=30, batch_first=True)
        self.dropout2 = nn.Dropout(0.05)
        self.lstm3 = nn.LSTM(input_size=30, hidden_size=20, batch_first=True)
        self.dropout3 = nn.Dropout(0.01)
        self.fc = nn.Linear(20, output_size)
        self.tanh = nn.Tanh()

    def forward(self, x):
        out, _ = self.lstm1(x)
        out = self.dropout1(out)
        out, _ = self.lstm2(out)
        out = self.dropout2(out)
        out, _ = self.lstm3(out)
        out = self.dropout3(out)
        out = out[:, -1, :]  # take the last output of the sequence
        out = self.fc(out)
        return out
