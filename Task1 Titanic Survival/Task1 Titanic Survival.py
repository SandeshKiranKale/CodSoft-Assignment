# -*- coding: utf-8 -*-
"""Cod Titanic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MxSfNkt-2X0YXXvYkzRHfJg-UUmlLYjP
"""

#Importing Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import  matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

"""## Importing CSV"""

# Loading Dataset
df = pd.read_csv("/content/Titanic-Dataset.csv")

df.head()

df.info()

df.describe()

# checking for missing values
df.isnull().sum().sort_values(ascending =  False)

# filling missing values in age column with mean
df['Age'].fillna(df['Age'].mean(),inplace=True)

#filling missing values in 'cabin column'
df['Cabin'].fillna('Unknown', inplace=True)

# filling missing values in embarked column
most_frequent_embarked = df['Embarked'].mode()[0]
df['Embarked'].fillna(most_frequent_embarked, inplace=True)

# checking for missing values if remaining
print(df.isnull().sum())

df.columns

"""#Visualization

"""

#visualizating survival based on socio-economic status (age)
plt.figure(figsize=(7,5))
sns.histplot(x='Age',hue='Survived', data=df,kde=True,palette='coolwarm')
plt.title('Count of survival based on Socio_economic Status Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.legend(loc='upper right', labels=['Did not Survived','Survived'])

# Survival based on gender
sns.barplot(x = 'Sex',y='Survived', data = df)
plt.ylabel('Survival Probability')
plt.title('Survival Based on Gender')

# Survival Probability based on passenger class
sns.barplot(x='Pclass',y='Survived',data = df)
plt.ylabel('Survival Probability')
plt.title('Survival Based on Passenger class')

# Survival based on siblings spouse on board
plt.figure(figsize=(6,4))
sns.countplot( x ='SibSp' , hue= 'Survived' ,data=df, palette = 'winter')
plt.title('Survival Count Base on Number Of Siblings')
plt.xlabel('SibSp(Number of Sibling/Spouses)')
plt.ylabel('Count')
plt.legend(title='Survived',loc='upper right', labels=['No', 'Yes'])
plt.show()

#Survival based on number of parent/Children onboard
plt.figure(figsize=(6,4))
sns.countplot(x='Parch', hue='Survived', data=df, palette='Set1')
plt.title('Survival Count Based on Number of PArent children onboard')
plt.xlabel('Parch(Number of  Parents/Children)')
plt.ylabel('Count')
plt.legend(title='Survived', loc='upper right', labels=['No', 'Yes'])
plt.show()

df.head().T

# Dropping  columns which are not going to get used
columns_to_drop = ['PassengerId', 'Name','Ticket', 'Cabin', 'Fare','Embarked']
df1 =df.drop(columns=columns_to_drop)

df1

#Using label Encoder to convert categorical features to numericl
label_encoder = LabelEncoder()
df1['Sex'] = label_encoder.fit_transform(df1['Sex'])

X = df1.drop('Survived', axis=1)
y = df1['Survived']

#Seperate variables and target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Training the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
DecisionTreeClassifier

# Evaluating the model
y_pred =model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:",accuracy)

"""###Random Forest


"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)

#Training the model on available data
model.fit(X_train, y_train)

#Checking for Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:",accuracy)

"""###KNN Model"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the KNN model
knn_model = KNeighborsClassifier()
knn_model.fit(X_train, y_train)

# Checking for Accuracy
y_pred_knn = knn_model.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
print("KNN Model Accuracy:", accuracy_knn)

"""###Conclusion
The Random Forest is the best Model with the highest accuracy among the others
"""