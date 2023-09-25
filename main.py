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

import math
from datetime import datetime, timedelta

# identify if duplication exists 
print(df1[df1.duplicated()])
print(df2[df2.duplicated()])
print(df3[df3.duplicated()])

# if duplication exists, remove and keep only one 
if len(df1[df1.duplicated()]) > 0: 
    df1 = df1.drop_duplicates(keep = 'first') 
if len(df2[df2.duplicated()]) > 0: 
    df2 = df2.drop_duplicates(keep = 'first') 
if len(df3[df3.duplicated()]) > 0: 
    df3 = df3.drop_duplicates(keep = 'first') 

# convert data type 
df1['Firstname'] = df1['Firstname'].astype('string') 
df1['PostalCode'] = df1['PostalCode'].astype('string') 
df1['HashCode'] = df1['HashCode'].astype('string') 
df1['Gender'] = df1['Gender'].astype('string')

# create a dummy variable, naming it Churn attribute to indicate churn with a value 'yes'
df2['Churn'] = 'yes' 
df2['Churn'] = df2['Churn'].astype('string')

# create Age Attribute deriving from Birthdate.
df1['Age'] = (datetime(2022, 3, 1) - df1['Birthdate']) // timedelta(days=365.2425)

#returns all rows from the Customer, even if there are no matches in Churn dataset
df_merge = df1.merge(df2, on='CustomerId', how='left')

#returns all rows from the Customer, even if there are no matches in Transaction
df_merge = df_merge.merge(df3, on='CustomerId', how='left')

# observe the dataset attributes and data types
print(df_merge.info())

# identify missing value
for i, col in enumerate(df_merge.columns): 
    print(col, df_merge[col].isna().sum())

# to treat null or missing values 
df_merge['Churn'] = df_merge['Churn'].fillna('no') 
df_merge['Cash'] = df_merge['Cash'].fillna(0)
df_merge['Cash'] = df_merge['Cash'].apply(lambda x : math.floor(x))
df_merge['CreditCard'] = df_merge['CreditCard'].fillna(0)
df_merge['CreditCard'] = df_merge['CreditCard'].apply(lambda x : math.floor(x))
df_merge['Cheque'] = df_merge['Cheque'].fillna(0)
df_merge['Cheque'] = df_merge['Cheque'].apply(lambda x : math.floor(x))

# to delete the remaining rows with missing values in any attribute
df_merge.dropna(inplace=True)

# to select the first character of the PostalCode
df_merge['PostalCode'] = df_merge['PostalCode'].str[0].astype('string')

# to select useful attributes for further analysis and modeling
df_merge = df_merge[['CustomerId','Gender', 'Age','PostalCode', 'MinTrxValue', 
                'MaxTrxValue', 'TotalTrxValue', 'Cash', 'CreditCard', 'Cheque', 
                'SinceLastTrx', 'Churn']]

# observe the consolidated data dimension and data types
print(df_merge.shape)
print(df_merge.info())

# save the data into a cvs file
df_merge.to_csv('CustomerChurn.csv')

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/CustomerChurn.csv')

# show basic statistics for numerical columns (count, mean, std, min, max, 25%, 50%, 75%)
print(df.describe())   

# show skewness and kurtusis of a particular columns
print('-----------Skewness--------------')
print(df.skew())

# show the values exist in the attribute and their counts
print(df['Gender'].value_counts())
print(df['Churn'].value_counts())
print(df['PostalCode'].value_counts())

# further exploration to check values
print(df['Cash'].value_counts())
print(df['Cheque'].value_counts())
print(df['CreditCard'].value_counts())

# to locate mänlich in Gender attribute and replace it with male
df.loc[df['Gender'] == 'mänlich', 'Gender'] = 'male' 

# to locate weiblich in Gender attribute and replace it with female
df.loc[df['Gender'] == 'weiblich', 'Gender'] = 'female'

# to confirm the Gender attribute values are correct
print(df['Gender'].value_counts())

# save the data into a CSV file 
df.to_csv('ChurnProcessed.csv')

df = pd.read_csv('data/ChurnProcessed.csv')

#For Normal Distribution = Age / SinceLastTrx
#get acceptable range h - l
# find the highest value allowed h
h1 = df['Age'].mean() + 3*df['Age'].std() 
h2 = df['SinceLastTrx'].mean() + 3*df['SinceLastTrx'].std() 

# find the lowest value allowed l
w1 = df['Age'].mean() - 3*df['Age'].std()
w2 = df['SinceLastTrx'].mean() - 3*df['SinceLastTrx'].std()


# get outliers based on the range identified between h and l
df1_outliers = df[(df['Age'] > h1) | (df['Age'] < w1)]
df2_outliers = df[(df['SinceLastTrx'] > h2) | (df['SinceLastTrx'] < w2)]

# find the number of outliers
print('No. of outliers (mean-std) in Age = ', df1_outliers.shape[0]) 
print('No. of outliers (mean-std) in SinceLastTrx = ', df2_outliers.shape[0])

#For Skewed Distribution =  MaxTrxValue / MinTrxValue / TotalTrxValue 
# find the upper/lower limits for each attribute
pct25_ttl = df['TotalTrxValue'].quantile(0.25) 
pct75_ttl = df['TotalTrxValue'].quantile(0.75) 
pct25_max = df['MaxTrxValue'].quantile(0.25) 
pct75_max = df['MaxTrxValue'].quantile(0.75) 
pct25_min = df['MinTrxValue'].quantile(0.25) 
pct75_min = df['MinTrxValue'].quantile(0.75) 

# calculate the iqr and range for each attribute
iqr_ttl = pct75_ttl - pct25_ttl 
up_ttl = pct75_ttl + 1.5 * iqr_ttl 
low_ttl = pct25_ttl - 1.5 * iqr_ttl 
iqr_max = pct75_max - pct25_max 
up_max = pct75_max + 1.5 * iqr_max 
low_max = pct25_max - 1.5 * iqr_max 
iqr_min = pct75_min - pct25_min 
up_min = pct75_min + 1.5 * iqr_min 
low_min = pct25_min - 1.5 * iqr_min 

# detect and print number of outliers in each attribute
df3_outliers = df[(df['TotalTrxValue'] > up_ttl) | (df['TotalTrxValue'] < low_ttl)] 
print('No. of outliers (IQR) in TotalTrxValue = ', df3_outliers.shape[0]) 
df4_outliers = df[(df['MaxTrxValue'] > up_max) | (df['MaxTrxValue'] < low_max)] 
print('No. of outliers (IQR) in MaxTrxValue = ', df4_outliers.shape[0]) 
df5_outliers = df[(df['MinTrxValue'] > up_min) | (df['MinTrxValue'] < low_min)] 
print('No. of outliers (IQR) in MinTrxValue = ', df5_outliers.shape[0]) 

import matplotlib.pyplot as plt 
import seaborn as sb

plt.figure(figsize=(10,15)) # define the plot width and height 

# histogram for each of these attributes to observe the data
# subplot(x, y, z) where x=rownum, y=colnum, z=plotnum, x(y)must be >=z
plt.subplot(3,1,1) 
sb.distplot(df['MinTrxValue']) 
plt.subplot(3,1,2)  
sb.distplot(df['MaxTrxValue']) 
plt.subplot(3,1,3) 
sb.distplot(df['TotalTrxValue'])   

plt.savefig('plot_dist.png')

import numpy as np
# apply sqrt on attributes that have outliers
# quare root transformation
df['SqrtTotal'] = np.sqrt(df['TotalTrxValue'])
df['SqrtMax'] = np.sqrt(df['MaxTrxValue'])
df['SqrtMin'] = np.sqrt(df['MinTrxValue'])

# observe that the values range has been reduced using the following example codes
print ('SqrtTotal min/max: ', df['SqrtTotal'].min(), df['SqrtTotal'].max()) 
print ('SqrtMax min/max: ', df['SqrtMax'].min(), df['SqrtMax'].max())
print ('SqrtMin min/max: ', df['SqrtMin'].min(), df['SqrtMin'].max())

# save the data into a CSV file 
df.to_csv('ChurnFinal.csv')
