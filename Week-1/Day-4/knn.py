# -*- coding: utf-8 -*-
"""P1W2D3AM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/ardhiraka/FSDS_Guidelines/blob/master/p1/w2/d3am.ipynb

# K - Nearest Neighbor Classifier

# A. KNN Introduction

## Import Libraries

First, let's import some libraries that we will use to demonstrate K - Nearest Neighbor.
"""

# Commented out IPython magic to ensure Python compatibility.
# Import Libraris

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc,roc_auc_score

# %matplotlib inline

"""## Generate sample data"""

# Function for Generate Data that Will Be Used by KNN

def generate_sample(x1_center, x2_center, max_radius, num_samples, ymax=999, ymin=-999):
    i = 0
    x1_list = []
    x2_list = []
    x1_min = x1_center - max_radius
    x1_max = x1_center + max_radius
    x2_min = x2_center - max_radius
    x2_max = x2_center + max_radius
    while i < num_samples:
        x1 = np.random.uniform(x1_min, x1_max)
        x2 = np.random.uniform(x2_min, x2_max)
        mag_data = np.power(x1 - x1_center, 2) + np.power(x2 - x2_center, 2)
        if (
            (mag_data <= np.power(max_radius, 2))
            & (x2 > ymin)
            & (x2 < ymax)
        ):
            x1_list.append(x1)
            x2_list.append(x2)
            i = i + 1
        else:
            continue

    return np.vstack((x1_list, x2_list)).T

# Generate Dataset

x1_centers = [0, 0, 2]
x2_centers = [0, 2, 0]
num_data = 50

datas = []
for i in range(0,len(x1_centers)):
    datas.append(generate_sample(x1_centers[i], x2_centers[i], 1.5, num_data))
    
X = np.vstack(datas)
y = list(np.hstack([[1] * num_data,[2] * num_data,[3] * num_data]))

# Display Data

## Display First 10 Data from X and y
print('First 10 Data')
print('X : ', X[:10])
print('y : ', y[:10])
print('')

## Display Number of Total Data per Class
print('Number of Total Data per Class')
for cls in list(set(y)):
  print('Class : ', cls, ' - Count : ', y.count(cls))

# Visualization of Dataset

plt.scatter(X[:,0], X[:,1], c=y)
plt.xlim(-2,4)
plt.ylim(-2,4)

"""Color description from above graph :
* Class `1` : Purple
* Class `2` : Green
* Class `3` : Yellow
"""

# Save the Colors into a Dictionary

class_colors = {
    '1': 'purple',
    '2': 'green',
    '3': 'yellow'
}

"""## Nearest Neighbors

Let's find the neighbors of two test data on the previously created dataset. To do that, we are going to implement module `NearestNeighbors` from Scikit-learn.
"""

# Define Two Test Data

X_sample = np.array(([0,1],[1,0]))

# Create Object of NearestNeighbors and Enter Dataset into this Object

neigh = NearestNeighbors(n_neighbors=15)
neigh.fit(X,y)

# Get the Neighbors for Test Data

neighbors_distances, neighbors_indices = neigh.kneighbors(X_sample)
y = np.array(y)

print('X_sample[0]               : ', X_sample[0])
print('Neighbors Distance        : ', neighbors_distances[0].tolist())
print('Neighbors Index           : ', neighbors_indices[0])
print('Neighbors Class           : ', y[neighbors_indices[0]])
print('Neighbors Class (Counter) : ', [(cls, list(y[neighbors_indices[0]]).count(cls)) for cls in list(set(y))])
print('Max Class                 : ', max(list(y[neighbors_indices[0]]), key=list(y[neighbors_indices[0]]).count))
print('Class Color               : ', class_colors[str(max(list(y[neighbors_indices[0]]), key=list(y[neighbors_indices[0]]).count))])
print('')

print('X_sample[1]               : ', X_sample[1])
print('Neighbors Distance        : ', neighbors_distances[1].tolist())
print('Neighbors Index           : ', neighbors_indices[1])
print('Neighbors Class           : ', y[neighbors_indices[1]])
print('Neighbors Class (Counter) : ', [(cls, list(y[neighbors_indices[1]]).count(cls)) for cls in list(set(y))])
print('Max Class                 : ', max(list(y[neighbors_indices[1]]), key=list(y[neighbors_indices[1]]).count))
print('Class Color               : ', class_colors[str(max(list(y[neighbors_indices[1]]), key=list(y[neighbors_indices[1]]).count))])
print('')

# Visualization of the Neighbors of Test Data

neighbors_indices = neighbors_indices.flatten().tolist()

X_neighbors =  X[neighbors_indices]
y_neighbors = y[neighbors_indices]
X_not_neighbors = np.array([element for i, element in enumerate(X) if i not in neighbors_indices])


plt.scatter(X_neighbors[:,0], X_neighbors[:,1], c=y_neighbors)
plt.scatter(X_sample[:,0], X_sample[:,1], marker='x', c='k')
plt.scatter(X_not_neighbors[:,0], X_not_neighbors[:,1], c='k', alpha=0.1)

"""As we see, there are data points that are closer to our sample points compared to other neighbors. Currently, those close data points will have the same vote weight as the one that is farther. We can modify this charactheristic by using euclidean distance as weight factor on majority vote to reflect that closer data points have closer resemblance.

## Using K-Nearest Neighbor Classifier

In the code above, we see the neighbors for test data. But we must compute manually the maximum class to get the prediction class. Let's use module `KNeighborsClassifier` from Scikit Learn to get automatically our class prediction.
"""

# Create Object of KNeighborsClassifier and Enter Dataset into this Object

neigh = KNeighborsClassifier(n_neighbors=15)
neigh.fit(X, y)

# Predict Test Data

y_predictions = neigh.predict(X_sample)

print('Predictions - X_sample[0] : ', y_predictions[0])
print('Predictions - X_sample[1] : ', y_predictions[1])

"""### Effect of distance functions

We can use different type of distances function, which may results to different nearest neighbors. For example, let's try using 4 different distances type:  
- Euclidean 
- Minkowski
- Manhattan
- Mahalanobis
"""

metrictypes=['euclidean','minkowski','manhattan','mahalanobis']
fig, axs = plt.subplots(int(len(metrictypes)/2), 2, figsize=(20, 12))
for i,metrictype in enumerate(metrictypes):
    if(metrictype=='mahalanobis'):
        neigh = NearestNeighbors(n_neighbors=15,algorithm='brute', metric=metrictype,metric_params={'V': np.cov(X)})
    else:
        neigh = NearestNeighbors(n_neighbors=15,metric=metrictype)
    neigh.fit(X,y)
    neighbors=neigh.kneighbors(X_sample)
    id_arr = neighbors[1]
    id_arr = id_arr.flatten().tolist()

    arr =  X[id_arr]
    y = np.array(y)
    arr_y = y[id_arr]
    arr_ex = np.array([element for i, element in enumerate(X) if i not in id_arr])

    axs[int(i/2),i%2].scatter(arr[:,0],arr[:,1],c=arr_y)
    axs[int(i/2),i%2].scatter(X_sample[:,0],X_sample[:,1],marker='x',c='k')
    axs[int(i/2),i%2].scatter(arr_ex[:,0],arr_ex[:,1],c='k',alpha=0.1)
    axs[int(i/2),i%2].set_title(metrictype)

"""We can see there are changes at the edges point due to how the distance calculated differently

# B. KNN on Real Dataset

Let's try to use KNN Classifier on real world data. This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. 

The objective of the dataset is to diagnostically predict whether or not a patient has diabetes, based on certain diagnostic measurements included in the dataset. Several constraints were placed on the selection of these instances from a larger database. In particular, all patients here are females at least 21 years old of Pima Indian heritage.

The datasets consists of several medical predictor variables and one target variable, `Outcome`. Predictor variables includes the number of pregnancies the patient has had, their BMI, insulin level, age, and so on.


URL = [Prima Indians Diabetes Dataset](https://www.kaggle.com/uciml/pima-indians-diabetes-database)
"""

# Load Dataset

df = pd.read_csv('diabetes.csv')
df.head()

# Check Features of Dataset

df.info()

"""We can see that the dataset has no missing values."""

# Create Final Dataset

X = df.drop('Outcome',axis=1).values
y = df['Outcome'].values

# Split Dataset into Train Data and Test Data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10, stratify=y)

print('Total Data Train : ', X_train.shape[0])
print('Total Data Test  : ', X_test.shape[0])

# Normalization
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Commented out IPython magic to ensure Python compatibility.
# # Train
# 
# %%time
# cls_knn_euclidean = KNeighborsClassifier(n_neighbors=5)
# cls_knn_manhattan = KNeighborsClassifier(n_neighbors=5, metric='manhattan')
# 
# cls_knn_euclidean.fit(X_train, y_train)
# cls_knn_manhattan.fit(X_train, y_train)

# Check Accuracy of Test Data

acc_knn_euclidean = cls_knn_euclidean.score(X_test, y_test)
acc_knn_manhattan = cls_knn_manhattan.score(X_test, y_test)

print('Accuracy - KNN - Euclidean : ', acc_knn_euclidean)
print('Accuracy - KNN - Manhattan : ', acc_knn_manhattan)

"""---

Let's check the effect of `k` on the accuracy of Train Data and Test Data.
"""

# Commented out IPython magic to ensure Python compatibility.
# # Get Accuracy from k = 1 to k = 15
# %%time
# 
# max_k = 15
# 
# train_acc_euclidean = []
# test_acc_euclidean = []
# 
# train_acc_manhattan = []
# test_acc_manhattan = []
# 
# for ii in range (1, max_k+1):
#   # With Euclidean Distance
#   cls_knn_euclidean = KNeighborsClassifier(n_neighbors = ii)
#   cls_knn_euclidean.fit(X_train, y_train)
# 
#   train_acc_euclidean.append(cls_knn_euclidean.score(X_train, y_train))
#   test_acc_euclidean.append(cls_knn_euclidean.score(X_test, y_test))
# 
#   # With Manhattan Distance
#   cls_knn_manhattan = KNeighborsClassifier(n_neighbors = ii, metric='manhattan')
#   cls_knn_manhattan.fit(X_train, y_train)
# 
#   train_acc_manhattan.append(cls_knn_manhattan.score(X_train, y_train))
#   test_acc_manhattan.append(cls_knn_manhattan.score(X_test, y_test))
# 
# print('Train Accuracy - Euclidean : ', train_acc_euclidean)
# print('Test Accuracy - Euclidean  : ', test_acc_euclidean, '\n')
# 
# print('Train Accuracy - Manhattan : ', train_acc_manhattan)
# print('Test Accuracy - Manhattan  : ', test_acc_manhattan, '\n')
#

# Visualization of Accuracy


plt.figure(figsize=(20,5))
plt.subplot(1, 2, 1)
plt.title('Effect of Value k on Accuracy - Euclidean Distance')
plt.plot(range(1, max_k+1), test_acc_euclidean, label='Testing Accuracy')
plt.plot(range(1, max_k+1), train_acc_euclidean, label='Training accuracy')

plt.subplot(1, 2, 2)
plt.title('Effect of Value k on Accuracy - Manhattan Distance')
plt.plot(range(1, max_k+1), test_acc_manhattan, label='Testing Accuracy')
plt.plot(range(1, max_k+1), train_acc_manhattan, label='Training accuracy')

plt.legend()
plt.xlabel('Number of k')
plt.ylabel('Accuracy')
plt.show()

"""`kNN Classifier` is a lazy learning method, thus **time to predict is relatively slower compared to time to fit/train**. This is contrast to model like `Logistic Regression`, `Decision Tree`, or `Artifical Neural Network`.

---

Let's compare its performance with logistic regression that we have previously learned
"""

# Commented out IPython magic to ensure Python compatibility.
# # Train with Logistic Regression
# %%time
# 
# logreg = LogisticRegression(random_state=10)
# logreg.fit(X_train, y_train)

# Check Accuracy of Test Data

acc_logreg = logreg.score(X_test, y_test)

print('Accuracy - KNN - Euclidean     : ', acc_knn_euclidean)
print('Accuracy - KNN - Manhattan     : ', acc_knn_manhattan)
print('Accuracy - Logistic Regression : ', acc_logreg)