# -*- coding: utf-8 -*-
"""Codsoft task2(movie rating).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A7eHt20WBIBReeWb28x-l28_jNklZEDe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

ds = pd.read_csv('/content/IMDb Movies India.csv',encoding='latin1')

ds

ds.shape

ds.info()

ds.describe()

# Function for calculating missing values percentage
def missing_values_withpercent():
   return pd.DataFrame({
    'Missing Values': ds.isna().sum().values,
    'Percentage': ((ds.isna().sum()/len(ds)) * 100).apply(lambda x: f'{x:.2f}%')
}, index=ds.columns)

missing_values_withpercent()

# Checking for missing values according to row
ds.isnull().sum(axis=1).sort_values(ascending=False)

# Droping columns consisting many missing values
ds.drop(['Actor 2', 'Actor 3'],axis=1, inplace=True)

# There are many duplicates in dataset for example:
duplicates = ds[ds.duplicated()]
if duplicates.empty:
    print("No duplicates found.")
else:
    print("Duplicates found.")

# Checking For Duploicates
print("Duplicate Rows except first occurrence:")
print(duplicates)

# removing Duplicates
ds_no_duplicates = ds.drop_duplicates()

ds.dropna(subset=['Duration'],inplace=True)

ds= ds[(ds.isnull().sum(axis=1).sort_values(ascending=False) <=5)]

missing_values_withpercent()

ds.dropna(subset=['Rating', 'Votes'],inplace=True)

missing_values_withpercent()

# Similar Process goes with Director Column
ds.Director.describe()

ds.groupby('Director').Director.count().sort_values(ascending=False)

# fill genre column with drama
ds.groupby('Genre').Genre.count().sort_values(ascending=False)

ds['Genre'].fillna('Drama',inplace=True)

missing_values_withpercent()

# SAme thing to apply omn actor 1 column
ds['Actor 1'].describe()

ds['Actor 1']. fillna('Amitabh Bachchan', inplace = True)

missing_values_withpercent()

ds.head()

ds['Year'] = ds['Year'].str.replace(r'[()]','',regex=True)

ds['Duration'] = ds['Duration'].str.replace(r'min','',regex=True)

ds.info()

"""## Changing colunm type data from EDA"""

ds['Year'] = ds['Year'].astype('int')
ds['Duration'] = ds['Duration'].astype('int')

ds['Votes'] = ds['Votes'].str.replace(',','')

ds['Votes'] = ds['Votes'].astype('int')

ds.info()

ds.describe()

"""##DATA ANALYSIS"""

plt.figure(figsize=(15,8))
ds['Year'].value_counts().plot(kind='bar')
plt.title('Number of Movies Per Year')

plt.figure(figsize=(20,10))
ds['Actor 1'].value_counts().sort_values(ascending = False).head(10).plot(kind='bar')
plt.title('Actor with Many Movies')

plt.figure(figsize=(20,10))
ds['Director'].value_counts().sort_values(ascending =False).head(10).plot(kind='bar')
plt.title('Director with most Movies')

ds['Rating'].plot(kind='box')

# Acording to above box plot there are many outlieers
ds['Votes'].plot(kind='box')

plt.figure(figsize=(15,10))
sns.heatmap(pd.crosstab(ds['Rating'],ds['Year'], normalize='columns')*100)

plt.figure(figsize=(15,10))
sns.heatmap(pd.crosstab(ds['Rating'], ds['Genre'], normalize='columns')*100)

plt.figure(figsize=(15,10))
sns.heatmap(pd.crosstab(ds['Rating'],ds['Duration'],normalize='columns')*100)

"""## Model Building"""

genre_counts = ds['Genre'].value_counts()
ds['Genre_encoded'] = ds['Genre'].map(genre_counts)

genre_mean_rating = ds.groupby('Genre')['Rating'].transform('mean')
ds['Genre_mean_rating'] = genre_mean_rating

director_mean_rating = ds.groupby('Director')['Rating'].transform('mean')
ds['Director_encoded'] = director_mean_rating

actor_mean_rating = ds.groupby('Actor 1')['Rating'].transform('mean')
ds['Actor_encoded'] = actor_mean_rating

print(ds.columns)

ds['Genre_mean_rating'].plot(kind='hist')

X = ds[[ 'Year', 'Votes', 'Duration','Genre_mean_rating','Director_encoded','Actor_encoded']]
y = ds['Rating']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit an imputer
imputer = SimpleImputer(strategy='mean')  # You can choose a different strategy
X_train_imputed = imputer.fit_transform(X_train)

# Initialize and train a Linear Regression model
model = LinearRegression()
model.fit(X_train_imputed, y_train)

# make prediction on the test set
y_pred = model.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
rsme = mse **0.5
print(f"Root Mean Squared Error:{rsme}")

# Replacing NaN values with the mean of each column
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Initialize and train a Linear Regression model
lr = LinearRegression()
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Evaluate the model
print('Mean squared error: ', mean_squared_error(y_test, y_pred))
print('Mean absolute error: ', mean_absolute_error(y_test, y_pred))
print('R2 score: ', r2_score(y_test, y_pred))