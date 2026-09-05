import pandas as pd

from google.colab import files
uploaded = files.upload()

df = pd.read_csv("train.csv")

print("SHAPE:")
print(df.shape)

print("\nCOLUMNS:")
print(df.columns)

print("\nDATA TYPES:")
print(df.dtypes)

print("\nFIRST 10 ROWS:")
print(df.head(10))

print("\nSTATISTICAL SUMMARY:")
print(df.describe())
