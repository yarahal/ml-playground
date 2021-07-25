import numpy as np
from cvxopt import matrix, solvers
solvers.options['show_progress'] = False

def sign(x):
    x[x < 0] = -1
    x[x >= 0] = 1
    return x

class SVM:    
    def __init__(self,kernel='linear',d=2,C=100):
        self.kernel = kernel
        self.d = d
        self.C = C

    def __kernel(self,x,z):
        if(self.kernel=='linear'):
            K = np.inner(x,z)
        elif(self.kernel=='polynomial'):
            inner_prod = np.inner(x,z)
            K = 1
            for t in range(self.d-1):
                K += inner_prod
                inner_prod *= inner_prod
        return K

    def fit(self,X,y):
        m, n = X.shape[0], X.shape[1]
        y[y == 0] = -1
        P = np.zeros((m,m))
        for i in range(m):
            for j in range(m):
                P[i,j] = y[i]*y[j]*self.__kernel(X[i,:],X[j,:])
        P = matrix(P)
        q = matrix(-np.ones(m))
        A = matrix(y.reshape(1,m))
        G = matrix(np.concatenate([np.eye(m),-np.eye(m)],axis=0))
        h = matrix(np.concatenate([np.full(m,self.C),np.zeros(m)],axis=0))
        b = matrix(np.zeros(1))
        self.alpha = np.array(solvers.qp(P=P,q=q,G=G,h=h,A=A,b=b)['x'])
        self.w = np.sum(y.reshape(m,1)*X*self.alpha,axis=0).transpose()
        on_margin = np.logical_and(self.alpha[:,0] > 10e-4,self.alpha[:,0] < self.C)
        X_margin, y_margin = X[on_margin], y[on_margin]
        self.b = -(np.min((X_margin @ self.w)[y_margin == -1]) + np.max((X_margin @ self.w)[y_margin == 1]))/2
        self.x, self.y = X[self.alpha[:,0] > 10e-4], y[self.alpha[:,0] > 10e-4]
        self.alpha = self.alpha[self.alpha[:,0] > 10e-4]
        
    def predict(self,X):
        K = np.zeros((self.x.shape[0],X.shape[0]))
        for i in range(self.x.shape[0]):
            for j in range(X.shape[0]):
                K[i,j] = self.__kernel(self.x[i,:],X[j,:])
        return sign(np.sum(self.alpha*self.y*K,axis=0)+self.b)