# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import math
import pandas as pd
from scipy.spatial import distance

def getFeaturesFromUser(i, vec):
    featureList = []
    
    if i < 4653:
        featureList.append("M")
    else: 
        featureList.append("F")
    
    featureList.append(vec.nationality[i])
        
    if not math.isnan(float(vec.born[i])):
        featureList.append(vec.born[i]) 
        age = 2017 - int(vec.born[i])

        if age < 18:
            featureList.append("age_0-18")
        if age > 15 and age < 25:
            featureList.append("age_15-25")
        if age > 20 and age < 30:
            featureList.append("age_20-30")
        if age > 25 and age < 35:
            featureList.append("age_25-35")   
        if age > 30 and age < 40:
            featureList.append("age_30-40") 
        if age > 35 and age < 45:
            featureList.append("age_35-45") 
        if age > 40 and age < 50:
            featureList.append("age_40-50")
        if age > 45 and age < 55:
            featureList.append("age_45-55")  
        if age > 50 and age < 60:
            featureList.append("age_50-60")
        if age > 55 and age < 65:
            featureList.append("age_55-65") 
        if age > 60 and age < 70:
            featureList.append("age_60-70")                 
        if age > 65:
            featureList.append("age_65-") 
    fl = vec.features[i].split(",")   
    featureList.extend(fl)    
    return featureList

if __name__ == "__main__":
    vec = pd.read_csv("personsData.csv", sep=';', header=0)
    with open("userIDs.csv", "r") as f:
        users = [int(line) for line in f]    
    featureList = []
    maxM = 4652
    #print(users)
    #find all possible features
    for i in range(0, maxM):#len(vec)):
        if int(vec.pid[i]) in  users:
            featureList.extend( getFeaturesFromUser(i, vec) )
    
    featureSet = set(featureList)  
    finalFeatureList = list(featureSet)
    print(len(featureSet), len(finalFeatureList))
    userMatrix = np.zeros((len(users), len(set(featureList))))
    
    print userMatrix.shape
    fotoIDList = []
    j = 0
    for i in range(0,  maxM):#len(vec)):
        try:
            if int(vec.pid[i]) in  users:
                userFeatures = getFeaturesFromUser(i, vec)
                indeces = [ finalFeatureList.index( feature )  for feature in userFeatures]
                userMatrix[j, indeces] = 1
                fotoIDList.append(str(vec.pid[i]))
                j = j+1
                #print(j)
        except:
            print("Error user:" + str(i))
            print(userFeatures)
            j = j+1
            print(j)
        
        
            
    sum_vector = np.sum(userMatrix, axis=0)  
  
    np.savetxt("finalFeatureList.csv", finalFeatureList, delimiter=';', fmt="%s" )
    np.savetxt("sum_vector.csv", sum_vector, delimiter=';')
    
    idf_vector = [math.log(len(users)/count, 10) for count in sum_vector]
    
    userMatrix = userMatrix * idf_vector
    

    
    simMetric = distance.cdist(userMatrix, userMatrix, 'cosine') 
    simMetric = 1 - simMetric
    
    np.savetxt("cbDistance.csv", simMetric, delimiter=';')
    
    maxVal = np.amax(userMatrix)
    userMatrix = userMatrix / maxVal
    
    np.savetxt("personsCBVectors.csv", userMatrix, delimiter=';')
    np.savetxt("personsCB_IDs.csv", fotoIDList, delimiter=';', fmt='%s' )
    
    #print(userMatrix) 
   
    
    

