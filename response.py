import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import pickle
import sys
import urllib
import urllib.request
import warnings

warnings.simplefilter("ignore")
# so the path i mentioned here is where my dataset is stored and im saving it in a variable called df.
df = pd.read_csv('D:/Projects/Telebot/telegram/dataset.csv')
df.drop(['Symptom_7', 'Symptom_8', 'Symptom_9', 'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
         'Symptom_15', 'Symptom_16', 'Symptom_17'], axis=1, inplace=True)

df1 = pd.read_csv('D:/Projects/Telebot/telegram/symptom-severity.csv')
df.isna().sum()
df.isnull().sum()
cols = df.columns
data = df[cols].values.flatten()

s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(df.shape)

df = pd.DataFrame(s, columns=df.columns)

df = df.fillna(0)
vals = df.values
symptoms = df1['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = df1[df1['Symptom'] == symptoms[i]]['weight'].values[0]

d = pd.DataFrame(vals, columns=cols)

d = d.replace('dischromic _patches', 0)
d = d.replace('spotting_ urination', 0)
df = d.replace('foul_smell_of urine', 0)
df.head()
(df[cols] == 0).all()

df['Disease'].value_counts()

df['Disease'].unique()

data = df.iloc[:, 1:].values
labels = df['Disease'].values
x_train, x_test, y_train, y_test = train_test_split(data, labels, shuffle=True, train_size=0.8, random_state=42)

param_grid = {'C': [0.02, 0.03, 0.04, 0.05], 'gamma': [0.2, 0.3, 0.4, 0.5],
              'kernel': ['linear', 'rbf', 'poly', 'sigmoid']}
grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=2)
grid.fit(x_train, y_train)

grid_predictions = grid.predict(x_test)

model = SVC(C=0.02, gamma=0.4, kernel='poly')
model.fit(x_train, y_train)

preds = model.predict(x_test)
import pickle

# now you can save it to a file
with open('SympDetector.pkl', 'wb') as f:
    pickle.dump(model, f)
# and later you can load it
with open('SympDetector.pkl', 'rb') as f:
    model = pickle.load(f)
conf_mat = confusion_matrix(y_test, preds)
df_cm = pd.DataFrame(conf_mat, index=df['Disease'].unique(), columns=df['Disease'].unique())
print('F1-score% =', f1_score(y_test, preds, average='macro') * 100, '|', 'Accuracy% =',
      accuracy_score(y_test, preds) * 100)


def predd(S1, S2, S3, S4, S5, S6):
    psymptoms = [S1, S2, S3, S4, S5, S6]
    print(psymptoms)
    a = np.array(df1["Symptom"])
    b = np.array(df1["weight"])
    for j in range(len(psymptoms)):
        for k in range(len(a)):
            if psymptoms[j] == a[k]:
                psymptoms[j] = b[k]

    psy = [psymptoms]

    pred2 = model.predict(psy)
    return pred2[0]


def sample(input_text):
    usr_msg = str(input_text).split(" ")
    new_lst = []
    for x in usr_msg:
        new_lst.append(x.replace("\n", ""))

    sympList = df1["Symptom"].to_list()
    str1 = predd(new_lst[0], new_lst[1], new_lst[2], new_lst[3], new_lst[4], new_lst[5])
    print(str1)
    str2 = "Hello" + "\nYou have high chances of " + str1 + ", Requesting you to consult a Doctor as soon as possible!"
    return str2
