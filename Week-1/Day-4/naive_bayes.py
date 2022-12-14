# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/ardhiraka/FSDS_Guidelines/blob/master/p1/w2/d3pm.ipynb

# Week 2: Day 3 PM // Naive Bayes

Naive Bayes employ bayesian logic and theorem to infer probability given hypotheses and their evidences.
"""

# Commented out IPython magic to ensure Python compatibility.
# Import Libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc,roc_auc_score
import time
import pandas as pd

# %matplotlib inline

"""To solidify our understanding of Bayes Theorem and Naive Bayes, we will manually implement Bayes Theorem by `Pandas` and compare it with `Scikit-Learn` utility.

We will intialize a toy dataset containing **whether a family buy a car given their family structure, age group, and income**.
"""

# Assigning features and label variables

family_struct = ['Nuclear','Extended','Childless','Childless','Single Parent','Childless','Nuclear','Nuclear','Extended','Single Parent']
age_group = ['Young','Old','Middle-aged','Young','Middle-aged','Young','Old','Middle-aged','Middle-aged','Old']
income = ['Low','Low','Low','Medium','Medium','Low','High','Medium','High','Low']
buy_car = ['Yes','No','No','Yes','Yes','No','Yes','Yes','Yes','No']

# Convert to Pandas Dataframe

dict = {'family_struct': family_struct,'age_group':age_group,'income':income,'buy_car':buy_car} 
    
df = pd.DataFrame(dict)
df.columns=list(df.columns[:-1])+['label']

# Display Pandas Dataframe

df

"""---
First, we **count the probability of our class/label**.
"""

# Create Frequency and Probability Each Label

df_grp_lbl=df.groupby('label').count().reset_index()[['label','income']]
df_grp_lbl.columns=list(df_grp_lbl.columns[:-1])+['f_h']
df_grp_lbl['p_h']=df_grp_lbl['f_h']/df_grp_lbl['f_h'].sum()

# Display Frequency and Probability for Each Label

df_grp_lbl

"""Notes : 
* `f_h` : Frequency of a label.
* `p_h` : Probability of a label.

---
Next, **we count the frequency of each events**. We will need this to count the conditional probability.
"""

# Create a dataframe that contains chopped of a features and its label

df_melt = df.melt(id_vars=['label'],var_name='features',value_name='value')
df_melt.columns=['label']+list(df_melt.columns[1:])

# Addition - Display `df_melt`

print('Original Dataframe')
print(df)
print('')
print('Chopped Datafram')
print(df_melt)

# Let's group it and get its frequencies

df_grp=df_melt.groupby(['label','features','value']).size().reset_index(name='count')
df_grp.columns=list(df_grp.columns[:-1])+['f_e_given_h']

print(df_grp)

# Now, we can filter the data based on whatever condition we like. Let's display rows that contains value == `Low`
# f_h = frequency of Yes/No (regardless of attributes)
# p_h = probabilty of Yes/No (regardless of attributes) (P(Yes) or P(No))

# f_e_given_h = frequency of Yes/No given a specific attribute
# p_e_given_h = probability of Yes/No given a specific attribute (P(attribute | Yes/No))

df_grp[df_grp['value']=='Low'].head(5)

# Merging chopped dataframe with frequency and probability of label

df_a=df_grp.groupby((['features','value'])).count().reset_index()[['features','value']]
df_a['key']=1
df_b = df_grp_lbl
df_b['key']=1
df_feat=pd.merge(df_a, df_b, on ='key').drop("key", 1)

print(df_feat)

"""---
Then, we built the conditional probability table. In case there is a combination of event and hypotheses that never happened, i.e. Nuclei family size not buying car, we will fill the conditional probability with the prior probability of given class.
"""

# Combine all dataframe into one big dataframe with its frequencies and probabilities

df_prob=df_feat.merge(df_grp,on=['label','features','value'], how='outer')
df_prob['p_e_given_h']=df_prob['f_e_given_h']/df_prob['f_h']
df_prob['p_e_given_h']=df_prob['p_e_given_h'].fillna(0)

print(df_prob)

## Adition - Legends
'''
f_h = frequency of Yes/No (regardless of attributes)
p_h = probabilty of Yes/No (regardless of attributes) (P(Yes) or P(No))

f_e_given_h = frequency of Yes/No given a specific attribute
p_e_given_h = probability of Yes/No given a specific attribute (P(attribute | Yes/No))

'''

"""---
We can then use this table as a lookup to infer our data. As example, lets try to infer a family which is **Single Parent, Young, with Low income**.
"""

# Step 1 : Get all data with attributes where `family_struct=Single Parent`, or `age_group=Young`, or `income=Low` regardless its label/target.
df_ext=df_prob[(df_prob['value'].isin(['Single Parent','Young','Low']))]
print('Step 1')
print(df_ext)
print('')

# Step 2 : Get probability based on filtered data from Step 1 for each label (`Yes` and `No`).
# How ? Multiply all probability values (`p_e_given_h`) based on the label/target ('Yes` and `No`)
df_ext=df_ext.groupby('label').agg({'p_e_given_h':np.prod}).reset_index()
print('Step 2')
print(df_ext)
print('')

# Step 3 : Get sum/total of this two probabilities values.
total_prob = df_ext['p_e_given_h'].sum()
print('Step 3')
print('Total Probability : ', total_prob)
print('')

# Step 4 : Divide `p_e_given_h` with `total_prob`
print('Step 4')
df_ext['norm_prob']=df_ext['p_e_given_h']/total_prob
print(df_ext)

"""---
Let's inference all our training data
"""

# Inferencing all possibilities of features based on given dataset

small_dfs = []
X=df[df.columns[:-1]]
for idx in range(len(X)):
    df_select = X.iloc[[idx]]
    df_ext=df_prob[df_prob['value'].isin(df_select.values[0])]
    df_ext=df_ext.groupby('label').agg({'p_e_given_h':np.prod}).reset_index()
    df_ext.columns=['label','p_h']
    df_ext['total_prob']=df_ext['p_h'].sum()
    df_ext['norm_prob']=df_ext['p_h']/df_ext['total_prob']
    df_select['prob_no']=df_ext[df_ext['label']=='No']['norm_prob'].values[0]
    df_select['prob_yes']=df_ext[df_ext['label']=='Yes']['norm_prob'].values[0]
    small_dfs.append(df_select)
    
df_infer = pd.concat(small_dfs, ignore_index=True)

# Display probabilities for given dataset

df_infer

"""---
Let's compare it with Scikit-Learn implementation
"""

# First, we must encode the dataset into numeric. Let's use One Hot Encoding for Features and Label Encoder for Target.

from sklearn.preprocessing import OneHotEncoder,LabelEncoder
enc = OneHotEncoder()

X = df[df.columns[:-1]]
enc.fit(X)
X_enc=enc.transform(X).toarray()

# Display `X`

print('X : \n', X, '\n')
print('One Hot Encoding : \n', X_enc)

# Encode Target into numeric

le = LabelEncoder()
label_encoded=le.fit_transform(df['label'])
print("Label:",label_encoded)

# Import Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB

# Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets
model.fit(X_enc,label_encoded)

# Merging result from scratch with result from Scikit-Learn

df_result_sklearn = df_infer.copy()
df_result_sklearn['prob_no_sklearn'] =  model.predict_proba(X_enc)[:,0]
df_result_sklearn['prob_yes_sklearn'] =  model.predict_proba(X_enc)[:,1]
df_result_sklearn

# Test A New Data

new_data = {'family_struct': ['Childless'],'age_group': ['Young'],'income': ['High']} 
    
df_new_data = pd.DataFrame(new_data)
X_new_data = enc.transform(df_new_data).toarray()
result_class = model.predict(X_new_data)
result_proba = model.predict_proba(X_new_data)

print('New Data - Real      : \n', df_new_data, '\n')
print('New Data - Encode    : ', X_new_data, '\n')
print('Result - Class       : ', result_class[0])
print('Result - Probability : ', result_proba)

# Add New Naive Bayes Classifiers

from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import CategoricalNB

# Create Several Naive Bayes Classifiers
model_bernoullinb = BernoulliNB()
model_multinomialnb = MultinomialNB()
model_categoricalnb = CategoricalNB()

# Train the model using the training sets
model_bernoullinb.fit(X_enc,label_encoded)
model_multinomialnb.fit(X_enc,label_encoded)
model_categoricalnb.fit(X_enc,label_encoded)

# Test A New Data

# new_data = {'family_struct': ['Childless'],'age_group': ['Young'],'income': ['High']} 
new_data = {'family_struct': ['Single Parent'],'age_group': ['Young'],'income': ['Low']} 
    
df_new_data = pd.DataFrame(new_data)
X_new_data = enc.transform(df_new_data).toarray()

print('New Data - Real      : \n', df_new_data, '\n')
print('New Data - Encode    : ', X_new_data, '\n')

result_class = model.predict(X_new_data)
result_proba = model.predict_proba(X_new_data)
print('Result - Gaussian NB')
print('Result - Class       : ', result_class[0])
print('Result - Probability : ', result_proba, '\n')

result_class = model_bernoullinb.predict(X_new_data)
result_proba = model_bernoullinb.predict_proba(X_new_data)
print('Result - Bernoulli NB')
print('Result - Class       : ', result_class[0])
print('Result - Probability : ', result_proba, '\n')

result_class = model_multinomialnb.predict(X_new_data)
result_proba = model_multinomialnb.predict_proba(X_new_data)
print('Result - Multinomial NB')
print('Result - Class       : ', result_class[0])
print('Result - Probability : ', result_proba, '\n')

result_class = model_categoricalnb.predict(X_new_data)
result_proba = model_categoricalnb.predict_proba(X_new_data)
print('Result - Categorical NB')
print('Result - Class       : ', result_class[0])
print('Result - Probability : ', result_proba, '\n')

# Let's compare it with our previous category {'family_struct': ['Single Parent'],'age_group': ['Young'],'income': ['Low']} 

print(df_ext)