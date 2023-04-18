# -*- coding: utf-8 -*-
"""final.q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DTENETEVftCjiHU-Xr1iDGneTXmv0uLA
"""

import pandas as pd # for data handling
from sklearn.model_selection import cross_val_score # for cross-validation
from sklearn.metrics import accuracy_score, classification_report # evaluation metrics
import matplotlib.pyplot as plt # for plotting

# scikit-learn classifiers evaluated (change as desired)
from sklearn.naive_bayes import GaussianNB 
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

!unzip '/content/drive/MyDrive/final.q2.data.zip'

# Read data from CSV files into pandas dataframes
train = pd.read_csv('final.q2.train.csv') # training data
test = pd.read_csv('final.q2.test.csv') # test data
new = pd.read_csv('final.q2.new.csv') # unlabeled data
# Show number of rows and columns in each dataframe
print('train contains %d rows and %d columns' %train.shape)
print('test contains %d rows and %d columns' %test.shape)
print('new contains %d rows and %d columns' %new.shape)
print('First 3 rows in train:') 
train.head(3) # display first 3 training samples

print('Last 2 rows in new:') 
new.tail(2) # display last 2 unlabeled samples

list(new)

features = list(train)[1:] # all but the first column header are feature names
print("features:", features)
X_train, X_test, X_new = train[features], test[features], new[features]
y_train, y_test = train.y, test.y
print('Shapes:')
print(f'X_train: {X_train.shape}, X_test: {X_test.shape}, X_new: {X_new.shape}')
print(f'y_train: {y_train.shape}, y_test: {y_test.shape}')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# model = DecisionTreeClassifier(max_leaf_nodes=5) # change hyperparameters as desired
# score = cross_val_score(model, X_train, y_train, cv=10).mean() # mean cross-validation accuracy
# print(f'Mean cross-validation accuracy = {score:0.4f}')

for k in range(2,20): # number of rules
    model = DecisionTreeClassifier(max_leaf_nodes=k)
    score = cross_val_score(model, X_train, y_train).mean() # mean cross-validation accuracy
    print(f'Mean cross-validation accuracy with {k} rules = {score:0.4f}')

chosen_model = DecisionTreeClassifier(max_leaf_nodes=5) # chosen model
print(chosen_model) # display model parameters

chosen_model.get_params()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# chosen_model.fit(X_train, y_train) # train selected model on ALL training examples
# predicted = chosen_model.predict(X_test) # predicted diagnosis for test examples
# acc = accuracy_score(y_test, predicted) # accuracy on test samples
# print(f'Accuracy on test samples = {acc:0.4f}') # show test accuracy
# print("Classification report on test samples:") # for precision, recall, F1-score
# print(classification_report(y_test, predicted, digits=4)) # rounded to 4 decimal places

from sklearn.metrics._plot.confusion_matrix import confusion_matrix
confusion_matrix(y_test, predicted)

predicted_new = chosen_model.predict(X_new) # predicted classes for unlabeled samples
new_prediction = pd.DataFrame() # dataframe with predicted classes
new_prediction['ID'] = new.ID # identifiers for unlabeled samples
new_prediction['y'] = predicted_new # # predicted classes for unlabeled samples
new_prediction.to_csv('final.q2.prediction.csv', index=False) # save as CSV file
new_prediction # display results

cm = pd.DataFrame(confusion_matrix(y_test, predicted))
cm.to_csv('hw2.q1.cm.csv')
cm

plt.figure(figsize=(10, 10)) # size of figure to be displayed

plot_tree(chosen_model, 
          feature_names=features, 
          class_names=[f'{c}' for c in chosen_model.classes_], 
          filled=True, rounded=True, impurity=False) # plot tree

plt.savefig("decision_tree.png") # save as PNG file
plt.show() # show tree

plt.figure(figsize=(16, 4)) # size of figure to be displayed
plt.bar(features, chosen_model.feature_importances_)
plt.xticks(rotation = 60, fontsize=16)
plt.title('Feature importances', fontsize=24)
plt.show()