# -*- coding: utf-8 -*-
"""python project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m5A9eJ-PuGN4jScBuohda9ryGXchV0Br
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import seaborn as sns

url="https://raw.githubusercontent.com/mohammedAljadd/students-performance-prediction/refs/heads/main/student-data.csv"
df=pd.read_csv(url)
df.head()

df.shape

df.isnull().sum() #any values null

features=df[['failures','health','age','studytime']]
target=df['passed']

X=features.values
y=target.values

X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.3)

y_train = pd.Series(y_train)
y_test = pd.Series(y_test)
y_train = y_train.map({'yes': 1, 'no': 0})
y_test = y_test.map({'yes': 1, 'no': 0})

scaler=StandardScaler() #to fix weight of multiple features and make it in same range
# normalizing values of x_train and x_test
X_train = scaler.fit_transform(X_train) #normalizing -->look for details
X_test=scaler.transform(X_test) #->>

X_train=torch.tensor(X_train, dtype=torch.float32)
X_test=torch.tensor(X_test, dtype=torch.float32)

y_train=torch.tensor(y_train, dtype = int)
y_test=torch.tensor(y_test, dtype = int)

class MultiClassClassifier(nn.Module):
  def __init__(self):
    super(MultiClassClassifier, self).__init__()
    #like deep nerural networks-> Multi Layers
    self.linear1=nn.Linear(4, 10) # 4 in 10 out -> number of input, number of hidden layers
    self.linear2=nn.Linear(10, 6) # 10 in 6 out -> number of hiddden layers, number of hidden layers
    self.linear3=nn.Linear(6, 3)  # 6 in 3 out -> number of hisden layers, number of categories of target

  def forward(self, x):
    x1 = torch.relu(self.linear1(x))
    x2 = torch.relu(self.linear2(x1))
    x3 = self.linear3(x2)
    return x3

model = MultiClassClassifier()
loss = nn.CrossEntropyLoss()
criteria = torch.optim.SGD(model.parameters(), lr = 0.05)
num_epochs=1000 #number of times

# creating lists to store etst and train loss
train_loss=[]
test_loss=[]

# training loop
for ep in range(num_epochs):
  model.train()
  predicted_y = model(X_train)
  losses = loss(predicted_y, y_train)

  #feedback
  criteria.zero_grad()
  losses.backward()
  criteria.step()
  print(losses.item())

  train_loss.append(losses.item())
  model.eval()
  with torch.no_grad():
    predicted_test_y=model(X_test)
    loss_test=loss(predicted_test_y,y_test)
    test_loss.append(loss_test.item())

plt.plot(test_loss, label = 'Test Loss')
plt.plot(train_loss, color='red', label = 'Train Loss')
plt.legend()
plt.show()

from sklearn.metrics import confusion_matrix
predicted_probs = model(X_test)
predicted_classes = torch.argmax(predicted_probs, dim=1)
predicted_classes = predicted_classes.cpu().numpy()
cm = confusion_matrix(y_test, predicted_classes)
print(cm)
sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels='auto', yticklabels='auto')
plt.show()

#calculating accuracy
with torch.no_grad():
  outputs=model(X_test)
  _, predicted_classes=torch.max(outputs.data,1)  #get predicted classes

accuracy=(predicted_classes==y_test).sum().item()/y_test.size(0)
print(accuracy)