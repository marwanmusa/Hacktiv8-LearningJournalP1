# -*- coding: utf-8 -*-
"""P1W3D3AM - 20220629 - FTDS-012 - Gaussian Mixtures Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10vw03Y2GFn0Jxo37x9ccCYo1xcerHCbs

# Week 3: Day 3 AM // Gaussian Mixture

## Import Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import sys
import sklearn
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt

"""## Create Dataset"""

# Create Dataset
from sklearn.datasets import make_blobs
## Membuat dataset untuk menunjukkan cara kerja GMM

data1, label1 = make_blobs(n_samples=1000, centers=((4, -4), (0, 0)), random_state=42) ##Titik centroid nya di -4,4 dan 0,0 lalu dibuat 1000 data
data2, label2 = make_blobs(n_samples=250, centers=1, random_state=42) ## dibuat 250 data

# Show Features
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.scatter(data1[:, [0]], data1[:, [1]])
plt.title('Scatter Plot of `data1`')

plt.subplot(1, 2, 2)
plt.scatter(data2[:, [0]], data2[:, [1]])
plt.title('Scatter Plot of `data2`')

plt.show()

# Convert to Ellipsoid Form / karena mau pakai GMM di convert bentuknya menjadi ellipsioda menggunakan numpy array
data1 = data1.dot(np.array([[0.374, 0.95], [0.732, 0.598]]))
data2 = data2 + [6, -8]

# Show Features
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.scatter(data1[:, [0]], data1[:, [1]])
plt.title('Scatter Plot of `data1`')

plt.subplot(1, 2, 2)
plt.scatter(data2[:, [0]], data2[:, [1]])
plt.title('Scatter Plot of `data2`')

plt.show()

# Merge `data1` and `data2` 
data_final = np.r_[data1, data2]
label_final = np.r_[label1, label2]

# Show Features
plt.scatter(data_final[:, [0]], data_final[:, [1]])
plt.title('Scatter Plot of `data_final`')

plt.show()

# Display Shape of Dataset
#Total data menjadi 1250 data setelah digabungkan
print('Shape - data_final  : ', data_final.shape) 
print('Shape - label_final : ', label_final.shape)

"""## Gaussian Mixture Model

### Train with Gaussian Mixture Model

---
Let's train a Gaussian mixture model on the previous dataset:
"""

# Train the Model

from sklearn.mixture import GaussianMixture

#GMM akan membuat 10 model (n_init) masing2 ada 3 cluster (n_components) lalu diambil performa terbaiknya
gm = GaussianMixture(n_components=3, n_init=10, random_state=42)
gm.fit(data_final)

"""---
Let's look at the parameters that the EM algorithm estimated:
"""

# Display Weights
#Tiap iterasi bobotnya berubah, cluster terakhir bobotny paling kecil artinya tidak begitu dominan dibanding cluster yg lain
gm.weights_

# Display Means
#Rata-rata per cluster dari masing2 kolom
gm.means_

# Display Variances

gm.covariances_

"""Did the algorithm actually converge?"""

# Display Converged

gm.converged_

"""Yes, good. How many iterations did it take?"""

# Display Number of Step used to Reach the Convergence
# Bisa mencapai converged dalam 4 iterasi dari max_iter = 100
gm.n_iter_

"""### Predict with Gaussian Mixture Model

You can now use the model to predict which cluster each instance belongs to (hard clustering) or the probabilities that it came from each cluster. For this, just use `predict()` method or the `predict_proba()` method:
"""

# Predict as `Hard Clustering`
# 1 data dimasukkan ke dalam 1 cluster
gm.predict(data_final)

# Predict as `Soft Clustering`
# Probabilitas masing2 data terhadap label
# pake threshold yang dibuat sendiri untuk menentukan masuk ke label mana
gm.predict_proba(data_final)

"""### Plot Decision Boundary

Now let's plot the resulting decision boundaries (dashed lines) and density contours:
"""

# Function to Plot Centroids

def plot_centroids(centroids, weights=None, circle_color='w', cross_color='k'):
    if weights is not None:
        centroids = centroids[weights > weights.max() / 10]
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='o', s=35, linewidths=8,
                color=circle_color, zorder=10, alpha=0.9)
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=2, linewidths=12,
                color=cross_color, zorder=11, alpha=1)

# Function to Plot GMM's Decision Boundary

from matplotlib.colors import LogNorm

def plot_gaussian_mixture(clusterer, X, resolution=1000, show_ylabels=True):
    mins = X.min(axis=0) - 0.1
    maxs = X.max(axis=0) + 0.1
    xx, yy = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                         np.linspace(mins[1], maxs[1], resolution))
    Z = -clusterer.score_samples(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z,
                 norm=LogNorm(vmin=1.0, vmax=30.0),
                 levels=np.logspace(0, 2, 12))
    plt.contour(xx, yy, Z,
                norm=LogNorm(vmin=1.0, vmax=30.0),
                levels=np.logspace(0, 2, 12),
                linewidths=1, colors='k')

    Z = clusterer.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z,
                linewidths=2, colors='r', linestyles='dashed')
    
    plt.plot(X[:, 0], X[:, 1], 'k.', markersize=2)
    plot_centroids(clusterer.means_, clusterer.weights_)

    plt.xlabel("$x_1$", fontsize=14)
    if show_ylabels:
        plt.ylabel("$x_2$", fontsize=14, rotation=0)
    else:
        plt.tick_params(labelleft=False)

# Plot GMM's Decision Boundary

plt.figure(figsize=(8, 4))
plot_gaussian_mixture(gm, data_final)
plt.title('Gaussian Mixture Model\'s Decision Boundary')
plt.show()

##Distribusi normalnya dilihat dari atas
##Garis merah adalah decision boundary
## Garis hitam yang menentukan seberapa jauh dengan centroid nya / semakin jauh artinya probabilitas data tersebut outliers itu tinggi

"""### Type of Hyperparameter `covariance_type`"""

# covariance_type yang menentukan decision boundary nya seperti apa
# dilihat dulu data nya bentuknya seperti apa terus disesuaikan cobariance_type nya

"""You can impose constraints on the covariance matrices that the algorithm looks for by setting the `covariance_type` hyperparameter:

* `"full"` (default): no constraint, all clusters can take on **any ellipsoidal shape of any size**.

* `"tied"`: all clusters **must have the same shape**, which can be any ellipsoid (i.e., they all share the same covariance matrix).

* `"spherical"`: all clusters **must be spherical**, but they can have different diameters (i.e., different variances).

* `"diag"`: clusters **can take on any ellipsoidal shape of any size, but the ellipsoid's axes must be parallel to the axes** (i.e., the covariance matrices must be diagonal).
"""

# Train with Different Value of `covariance_type`

## Define the Model
gm_full = GaussianMixture(n_components=3, n_init=10, covariance_type="full", random_state=42)
gm_tied = GaussianMixture(n_components=3, n_init=10, covariance_type="tied", random_state=42)
gm_spherical = GaussianMixture(n_components=3, n_init=10, covariance_type="spherical", random_state=42)
gm_diag = GaussianMixture(n_components=3, n_init=10, covariance_type="diag", random_state=42)

## Train the Model using `.fit`
gm_full.fit(data_final)
gm_tied.fit(data_final)
gm_spherical.fit(data_final)
gm_diag.fit(data_final)

# Create Function to Compare Multiple Model of GMM

def compare_gaussian_mixtures(gm1, gm2, gm3, gm4, X):
    plt.figure(figsize=(20, 10))

    plt.subplot(221)
    plot_gaussian_mixture(gm1, X)
    plt.title('covariance_type="{}"'.format(gm1.covariance_type), fontsize=14)

    plt.subplot(222)
    plot_gaussian_mixture(gm2, X, show_ylabels=True)
    plt.title('covariance_type="{}"'.format(gm2.covariance_type), fontsize=14)

    plt.subplot(223)
    plot_gaussian_mixture(gm3, X, show_ylabels=False)
    plt.title('covariance_type="{}"'.format(gm3.covariance_type), fontsize=14)

    plt.subplot(224)
    plot_gaussian_mixture(gm4, X, show_ylabels=False)
    plt.title('covariance_type="{}"'.format(gm4.covariance_type), fontsize=14)

    plt.show()

# Display Comparison

compare_gaussian_mixtures(gm_full, gm_tied, gm_spherical, gm_diag, data_final)

"""### Model selection

We cannot use the `inertia` or the `silhouette_score` because they both assume that the clusters are spherical. Instead, we can try to find the model that minimizes a theoretical information criterion such as the Bayesian Information Criterion (BIC) or the Akaike Information Criterion (AIC):

${BIC} = {\log(m)p - 2\log({\hat L})}$

${AIC} = 2p - 2\log(\hat L)$

* $m$ is the number of instances.
* $p$ is the number of parameters learned by the model.
* $\hat L$ is the maximized value of the likelihood function of the model. This is the conditional probability of the observed data $\mathbf{X}$, given the model and its optimized parameters.

Both BIC and AIC penalize models that have more parameters to learn (e.g., more clusters), and reward models that fit the data well (i.e., models that give a high likelihood to the observed data).
"""

# Get `BIC` Score and `AIC` Score for Previous Model

print('BIC Score : ', gm.bic(data_final))
print('AIC Score : ', gm.aic(data_final))

"""We could compute the BIC manually like this:"""

# Compute `BIC` Score and `AIC` Score Manually from Scratch

n_clusters = 3
n_dims = 2
n_params_for_weights = n_clusters - 1
n_params_for_means = n_clusters * n_dims
n_params_for_covariance = n_clusters * n_dims * (n_dims + 1) // 2
n_params = n_params_for_weights + n_params_for_means + n_params_for_covariance

max_log_likelihood = gm.score(data_final) * len(data_final) # log(L^)

bic = np.log(len(data_final)) * n_params - 2 * max_log_likelihood
aic = 2 * n_params - 2 * max_log_likelihood

print('BIC Score : ', bic)
print('AIC Score : ', aic)

"""---
Let's train Gaussian Mixture models with various values of `k` and measure their `BIC` and `AIC` :
"""

# Train GMM with Various Number of Clusters
## Berapa k yang optimal?

## Membuat model GMM dari cluster 1-10 dengan 10 model masing-masing
gms_per_k = [GaussianMixture(n_components=k, n_init=10, random_state=42).fit(data_final)
             for k in range(1, 11)]

# Get BIC and AIC Scores

bics = [model.bic(data_final) for model in gms_per_k]
aics = [model.aic(data_final) for model in gms_per_k]

for k in range(0, 10):
  print('Cluster : ', k+1, '\tBIC : ', bics[k], '\tAIC : ', aics[k])

##Yang dilihat pertama AIC score yang minimum dulu

# Plot BIC Score and AIC Score

plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), bics, "bo-", label="BIC")
plt.plot(range(1, 11), aics, "go--", label="AIC")
plt.xlabel("$k$", fontsize=14)
plt.ylabel("Information Criterion", fontsize=14)
plt.axis([1, 11, np.min(aics) - 50, np.max(aics) + 50])
plt.annotate('Minimum',
             xy=(3, bics[2]),
             xytext=(0.35, 0.6),
             textcoords='figure fraction',
             fontsize=14,
             arrowprops=dict(facecolor='black', shrink=0.1)
            )
plt.legend()
plt.show()

"""Let's search for best combination of values for both the number of clusters and the `covariance_type` hyperparameter:"""

# Commented out IPython magic to ensure Python compatibility.
# # Get Best Cluster and Best Hyperparameter
# # You can think this below code is like GridSearchCV on Supervised Learning
# ## GridSearchCV hanya di Supervised, kita gunakan looping untuk unsupervised
# 
# %%time
# min_bic = np.infty
# 
# #Loop untuk cluster 1-10
# for k in range(1, 11):
#     #Loop untuk masing-masing covariance_type
#     for covariance_type in ("full", "tied", "spherical", "diag"):
#         bic = GaussianMixture(n_components=k, n_init=10,
#                               covariance_type=covariance_type,
#                               random_state=42).fit(data_final).bic(data_final)
#         #Cari BIC paling kecil, lalu lihat cluster keberapa dan covariance_type yang mana
#         if bic < min_bic:
#             min_bic = bic
#             best_k = k
#             best_covariance_type = covariance_type
# 
# print('Best - n_components    : ', best_k)
# print('Best - covariance_type : ', best_covariance_type)

"""## Bayesian Gaussian Mixtures

Rather than manually searching for the optimal number of clusters, it is possible to use instead the `BayesianGaussianMixture` class which is capable of **giving weights equal (or close) to zero to unnecessary clusters**. 

Just **set the number of components (`n_components`) to a value that you believe is greater than the optimal number of clusters**, and the algorithm will eliminate the unnecessary clusters automatically.
"""

# Commented out IPython magic to ensure Python compatibility.
# # Di GMM kita harus menentukan nilai k
# # Di BGM, akan diberikan bobot mendekati 0 ketika clusternya tidak diperlukan
# 
# # Train Model using Bayesian Gaussian Mixture
# 
# %%time
# from sklearn.mixture import BayesianGaussianMixture
# 
# ## Set n_components dengan nilai yang besar
# bgm = BayesianGaussianMixture(n_components=10, n_init=10, random_state=42)
# bgm.fit(data_final)

"""The algorithm automatically detected that only 3 components are needed:"""

# Display Weight of Each Cluster
## Menurut BGM pakai 3 cluster saja sudah cukup karena cluster yg lainnya mendekati 0 bobotnya

print('Weight - Full Value             : \n', bgm.weights_)
print('')
print('Weight - Round to Two Digits    : \n', np.round(bgm.weights_, 2))
print('')
print('Weight - Gaussian Mixture Model : \n', gm.weights_)

# Plot Decision Boundary from Bayesian Gaussian Mixture

plt.figure(figsize=(8, 5))
plot_gaussian_mixture(bgm, data_final)
plt.show()