import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()
    for column in df.columns:
        if df[column].dtype == 'string':
            most_frequent = df[column].mode()[0]
            df[column].fillna(most_frequent, inplace=True)
        elif df[column].dtype == 'int64' or df[column].dtype == 'float64':
            mean_value = df[column].mean()
            df[column].fillna(mean_value, inplace=True)
            df[column] = scaler.fit_transform(df[column].values.reshape(-1, 1))
    for column in df.columns:
        if df[column].dtype == 'string':
            dummies = pd.get_dummies(df[column], prefix=column, drop_first=True)
            df = pd.concat([df, dummies], axis=1)
            df.drop(column, axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    return df
