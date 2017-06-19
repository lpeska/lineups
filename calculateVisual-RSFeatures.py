# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import pandas as pd
from scipy.spatial import distance



if __name__ == "__main__":
    vec = pd.read_csv("personsVectors.csv", sep=';', header=None)
    v = np.asarray(vec)
    users = [str(int(i)) for i in v[:,0]]
    
    v2 = v[:,1:v.shape[0]]

    simMetric = distance.cdist(v2, v2, 'cosine') 
    simMetric = 1 - simMetric

    np.savetxt("cosineDistance.csv", simMetric, delimiter=';')
    np.savetxt("userIDs.csv", users, delimiter=';',fmt='%s')

    
    
    