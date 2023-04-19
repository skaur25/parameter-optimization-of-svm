import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as r
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


kernalList=[ 'linear','poly', 'rbf', 'sigmoid']
bestAccuracy = 0


cvgs_data = []
all_samples = []


data = pd.read_csv('./ai4i2020.csv')
df = data.iloc[:,2:9]

# encoding type values
encoder = {'L':1,'M':2,'H':3}
for i in range(df.shape[0]):
    df['Type'][i]=encoder[df['Type'][i]]    


X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values

def get_accuracy(X_train,y_train,X_test,y_test,params):
    print(params)
    c = SVC(kernel=params[0],C=params[1],gamma=params[2],degree=params[3])    
    c.fit(X_train,y_train)
    y_pred = c.predict(X_test)
    return accuracy_score(y_test,y_pred)


def sample(X,y,iter=100):
    global bestAccuracy
    sample_bestAccuracy = 0
    sample_bestGamma = 0     #  rbf,poly sig only
    sample_bestKernel = ''
    sample_bestC =  0       
    sample_bestDegree = 0  #1-5        # poly only
    sample_cvgs_data = []

    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    for _ in range(iter):
        kernel = r.choice(kernalList)
        c = r.randint(1,7)
        g = r.randint(-1,7)
        p = r.randint(1,7)
        if(g<1):
            g=r.choice(['scale','auto'])
        if(kernel == 'poly'):
            g=r.choice(['scale','auto'])

        accu = get_accuracy(X_train,y_train,X_test,y_test,[kernel,c,g,p])    

        print(accu)

        if(accu>sample_bestAccuracy):
            sample_bestAccuracy=accu
            sample_bestC=c
            sample_bestDegree=p
            sample_bestKernel=kernel
            sample_bestGamma=g
        
        sample_cvgs_data.append(sample_bestAccuracy)
    
    all_samples.append([sample_bestKernel,sample_bestC,sample_bestGamma,sample_bestDegree,sample_bestAccuracy])
    
    if(sample_bestAccuracy>bestAccuracy):
        global cvgs_data
        cvgs_data = sample_cvgs_data
        bestAccuracy=sample_bestAccuracy

for _ in range(10):
    sample(X,y,500)

all_samples = pd.DataFrame(all_samples,columns=['Kernel','c','gamma','degree','Accuracy'])
print(all_samples)


all_samples.to_csv('./result.csv',index=False)
all_samples.to_markdown('./result.md',index=False)

plt.plot(np.arange(len(cvgs_data)),cvgs_data)
plt.title('Convergence graph of best SVM')
plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.show()


