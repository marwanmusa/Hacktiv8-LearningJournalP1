# -*- coding: utf-8 -*-
"""knn-nb-model_eval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PSFkUacEgdqdIqs6ovb0vpFeyjh3PNv4

Step memodelkan data dengan Machine Learning :

- Import library
- Siapkan Dataset
  - Data Cleansing (handle missing value, outlier, dll)
  - Feature Engineering (encoding, scaling, dll.)
- Deklarasi model
- Training Model
  - Model Optimization (tuning parameter, tweaking, dll.) (todo)
- Gunakan Model
  - Evaluasi
  - Inference
  - Save Model
  - Deployment
"""

# import library
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import matplotlib.pyplot as plt

# siapkan data
df = pd.read_csv("https://raw.githubusercontent.com/npradaschnor/Pima-Indians-Diabetes-Dataset/master/diabetes.csv")
df.head()

df.info()

# pisahkan antara fitur dan label
X = df.drop("Outcome", axis=1)
y = df['Outcome']

# split train-test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=46)

# deklarasikan scaler
scaler = StandardScaler()

# scale data training
X_train_scaled = scaler.fit_transform(X_train)

# scale data test
X_test_scaled = scaler.transform(X_test)

# Deklarasikan model

knn = KNeighborsClassifier(n_neighbors=7)

# training model
knn.fit(X_train_scaled, y_train)

# prediksi data test
y_pred = knn.predict(X_test_scaled)

# evaluasi model
print(classification_report(y_pred, y_test))

from sklearn.metrics import precision_score
print(precision_score(y_pred, y_test))

# save model
with open("model_knn.pkl", "wb") as model_file:
  pickle.dump(knn, model_file)

"""### Choose K"""

# loop k dan train masing2 k
max_k = 30
training = []
testing = []
for k in range(1, max_k+1):
  # deklarasi
  knn_loop = KNeighborsClassifier(n_neighbors=k)

  # training
  knn_loop.fit(X_train_scaled, y_train)

  # evaluasi training
  score_training = knn_loop.score(X_train_scaled, y_train)
  training.append(score_training)
  
  # evaluasi testing
  score_testing = knn_loop.score(X_test_scaled, y_test)
  testing.append(score_testing)

metrics = pd.DataFrame({'training': training, 'testing':testing})

metrics.plot()

metrics[metrics['testing'] == metrics['testing'].max()]

"""# Naive Bayes"""

# import library
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score
import pickle
import matplotlib.pyplot as plt

# siapkan data
df = pd.read_csv("https://raw.githubusercontent.com/npradaschnor/Pima-Indians-Diabetes-Dataset/master/diabetes.csv")
df.head()

# pisahkan antara fitur dan label
X = df.drop("Outcome", axis=1)
y = df['Outcome']

# split train-test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=46)

# deklarasikan scaler
scaler = StandardScaler()

# scale data training
X_train_scaled = scaler.fit_transform(X_train)

# scale data test
X_test_scaled = scaler.transform(X_test)

nb = GaussianNB()

nb.fit(X_train, y_train)

y_pred = nb.predict(X_test)
print(classification_report(y_test, y_pred))

nb.predict(X_test)[:5]

nb.predict_proba(X_test)[:5]

from sklearn.metrics import roc_curve, roc_auc_score

nb.predict_proba(X_test)[:,1]

y_pred_proba = nb.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
auc = roc_auc_score(y_pred, y_pred_proba)

import pandas as pd

pd.DataFrame({'fpr':fpr, 'tpr':tpr})

plt.plot(fpr, tpr, label=f"AUC={auc}")
plt.plot([0,1],[0,1]);
plt.ylabel("TPR")
plt.xlabel("FPR")
plt.legend()

auc

