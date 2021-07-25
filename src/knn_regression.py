import numpy as np

def euclidean_distance(p1,p2):
    return np.sum((p1-p2)**2)

class KNNRegression:
    def __init__(self,k=3):
        self.k = k

    def fit(self,X,y):
        self.points = list(zip(X,y))

    def predict(self,X):
        sorted_points = sorted(self.points,key=lambda p1: euclidean_distance(p1[0],X))
        k_closest_points = sorted_points[:self.k]
        return np.mean(k_closest_points,axis=0)[1]