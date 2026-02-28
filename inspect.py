import pandas as pd
import os
base='real_estate_predictor'
df=pd.read_csv(os.path.join(base,'data','indian_real_estate_data.csv'))
print(df.columns)
print(df.head())
