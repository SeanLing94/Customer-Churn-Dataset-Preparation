import pandas as pd

df1 = pd.read_excel ('Customer-Churn-and-Dataset/customer.xlsx')
df2 = pd.read_excel ('Customer-Churn-and-Dataset/churn.xlsx')
df3 = pd.read_excel ('Customer-Churn-and-Dataset/ptransaction.xlsx')

# to display dataset dimension in row and column
print("Customer dataset: ", df1.shape)
print("Churn dataset: ",df2.shape)
print("Payment transaction dataset: ",df3.shape)

# to display dataset column names, #non-null, data type
print(df1.info())
print(df2.info())
print(df3.info())

# to display first few items in the xlsx
print(df1.head())
print(df2.head())
print(df3.head())
