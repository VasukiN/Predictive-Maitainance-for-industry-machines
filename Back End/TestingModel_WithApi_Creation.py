import pandas as pd
import seaborn as sns
sns.set()
import numpy as np
import warnings
import pickle
import sys
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from collections import Counter

warnings.filterwarnings('ignore')

import sklearn
print('The scikit-learn version is {}.'.format(sklearn.__version__))


index_columns = ["Unit", "Cycle"]
settings_columns = ["setting" + str(i + 1) for i in range(3)]
sensor_columns = ["s" + str(i + 1) for i in range(21)]
final_columns = index_columns + settings_columns + sensor_columns
engine_data = pd.read_csv("TurbofanDataSet/train_FD001.txt", header=None, sep=" ")
engine_data = engine_data[engine_data.columns[0:26]]
engine_data.columns = final_columns


# Data statistics
engine_data.copy(deep=True).drop(['Unit'], axis=1).describe()

engine_data_test = pd.read_csv("TurbofanDataSet/test_FD001.txt", header=None, sep=" ")
engine_data_test = engine_data_test[engine_data_test.columns[0:26]]
engine_data_test.columns = final_columns
engine_data[engine_data['Unit'] == 1].head()
engine_data[engine_data['Unit'] == 1].tail()

################################################################################################################

# Label Test Data
# RUL_FD001.txt contains the RUL for the last cycle for all the engines in the test data set
# In the test set, the time series ends some time before the system failure.
remaining_RUL_test = pd.read_csv("TurbofanDataSet/RUL_FD001.txt", header=None)
remaining_RUL_test["Unit"] = remaining_RUL_test.index + 1


def get_RUL_test(engine_data_test, remaining_RUL_test):
    # Get the last cycle for all the engines in the test data set
    last_cycle = engine_data_test.copy(deep=True).groupby(['Unit'])["Cycle"].max().reset_index()
    final = pd.merge(last_cycle, engine_data_test.copy(deep=True), how="inner", on=["Unit", "Cycle"])
    final = pd.merge(final, remaining_RUL_test, how="inner", on=["Unit"])

    final["RUL"] = final[0]
    final["binary_class"] = final["RUL"].map(lambda x: str("Danger") if x <= 30 else str("Normal"))
    final["multi_class"] = final["RUL"].map(lambda x: str("Danger") if x <= 15 else str("Ok") if x<= 30 else str("Normal"))
    return final


test_labels = get_RUL_test(engine_data_test.copy(deep=True), remaining_RUL_test)
RUL_test = test_labels["RUL"]
binary_class_test = test_labels["binary_class"]
multi_class_test = test_labels["multi_class"]
unit_test = test_labels["Unit"]

RUL_test_Json  = test_labels[['Unit', 'RUL']]

RUL_test_Binary_Json  = test_labels[['Unit','RUL', 'binary_class']]

#print(test_labels)

RUL_test_MultiClassification_Json  = test_labels[['Unit','RUL', 'multi_class']]

################################################################################################################

# Feature Transformation
# Dimensionality Reduction of Test  Data

from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

# These features are being dropped based on the observation from exploratory data analysis
features_dropped = ['Unit', 'setting1', 'setting2', 'setting3', 's1', 's5', 's10', 's16', 's18', 's19']

normalized_data = engine_data.copy(deep=True).drop(features_dropped, axis=1)
# Scale the test data using the natural logarithm
normalized_data = np.log(normalized_data)

n_components = 13

# Apply PCA by fitting the normalized data with 13 dimensions
pca = PCA(n_components=n_components)
reduced_data = pca.fit_transform(normalized_data)
reduced_data = pd.DataFrame(reduced_data, columns=['Dimension ' + str(i+1) for i in range(n_components)])

################################################################################################################

# Dimensionality Reduction of Test Data

# Since remaining_RUL_test contains RUL only for the last cycle in the test data set, 
# we only keep the last cycle for each engine in the test data set
last_cycle = engine_data_test.copy(deep=True).groupby(['Unit'])["Cycle"].max().reset_index()
#print(last_cycle)
normalized_data_test = engine_data_test.copy(deep=True)
normalized_data_test = pd.merge(last_cycle, normalized_data_test, how="inner", on=["Unit", "Cycle"])
normalized_data_test = normalized_data_test.drop(features_dropped, axis=1)
# Scale the test data using the natural logarithm
normalized_data_test = np.log(normalized_data_test)

# transform normalized_data_test using the pca fit
reduced_data_test = pca.transform(normalized_data_test)
reduced_data_test = pd.DataFrame(reduced_data_test, columns=['Dimension ' + str(i+1) for i in range(n_components)])

################################################################################################################

########################   Regression Starts  For 100 Engine  ############

# Train and Test the selected model for RUL (Regression)
# Predict RUL for turbofan engine using Regression


# Load LinearRegression from file
with open('Nov25_LinearRegression.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
RUL_predictions = pickle_model.predict(reduced_data_test)
RUL_test_Json['Linear_Rul'] = RUL_predictions;

linear_rul_mse = str(mean_squared_error(RUL_predictions, RUL_test))

#print("Linear RUL_predictions MSE : " + linear_rul_mse)

##################################################################################

# Load Nueral Network from file
with open('Nov25_NeuralNetwork.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
RUL_predictions_nn = pickle_model.predict(reduced_data_test)
RUL_test_Json['NeuralNetwork_Rul'] = RUL_predictions_nn;

nn_rul_mse = str(mean_squared_error(RUL_predictions_nn, RUL_test))

#print("RUL_predictions_nn  MSE : " + nn_rul_mse)

################################################################################################################

# Load Random Forest from file
with open('Nov25_RandomForest.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
RUL_predictions_randomforest = pickle_model.predict(reduced_data_test)
RUL_test_Json['Randomforest_Rul'] = RUL_predictions_randomforest;

rf_rul_mse = str(mean_squared_error(RUL_predictions_randomforest, RUL_test))

#print("RUL_predictions_randomforest MSE : " + rf_rul_mse)

################################################################################################################

# Load SVM from file
with open('Nov25_SVM.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
RUL_predictions_svm = pickle_model.predict(reduced_data_test)
RUL_test_Json['SVM_Rul'] = RUL_predictions_svm;

svm_rul_mse = str(mean_squared_error(RUL_predictions_svm, RUL_test))

#print("RUL_predictions_svm MSE : " + svm_rul_mse)
#print(" --------------------------------- " )
#print("https://www.quora.com/How-is-mean-squared-error-MSE-used-to-compare-different-estimators-Is-a-larger-or-smaller-MSE-better")
#print("MSE is less for Linear regression,So we can consider that ")
#print(" --------------------------------- " )

################################################################################################################

#API Creation

rul_accuracy = {"Linear": linear_rul_mse, "NeuralNetwork": nn_rul_mse, 
        "RandomForest": rf_rul_mse,"SVM":svm_rul_mse} 

#print(rul_accuracy)

#accuracy_obj = list()
#accuracy_obj.append(linear_rul_mse)
#accuracy_obj.append(nn_rul_mse)
#accuracy_obj.append(rf_rul_mse)
#accuracy_obj.append(svm_rul_mse)
#print(accuracy_obj)
print("--------------------------------------------------------------------------------")

test_array_regression_eachengineId_lessthan50 = list()
test_array_regression_eachengineId_lessthan30_count = 0;

test_array_regression_eachengineId = list()
obj={}
for index, row in RUL_test_Json.iterrows():
    obj={'unit':row["Unit"],'Groundtruth_Rul':row["RUL"],'Linear_Rul':row["Linear_Rul"],'NeuralNetwork_Rul':row["NeuralNetwork_Rul"],
       'Randomforest_Rul':row["Randomforest_Rul"],'SVM_Rul':row["SVM_Rul"]}
    test_array_regression_eachengineId.append(obj)
    if row["Linear_Rul"]<30:
       test_array_regression_eachengineId_lessthan50.append(row["Linear_Rul"])
       
#print("test_array_regression_eachengineId_lessthan50")
#print(test_array_regression_eachengineId_lessthan50)
test_array_regression_eachengineId_lessthan30_count = len(test_array_regression_eachengineId_lessthan50)

#print(test_array_regression_eachengineId_lessthan30_count)

########################   Regression Done For 100 Engine  ############
    
########################## Binary Classification Starts  #########################
    
# Load Random forest  Test model from file
with open('Nov25_RandomForestClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
RandomforestClassification = pickle_model.predict(reduced_data_test)
RUL_test_Binary_Json['RandomforestClassification'] = RandomforestClassification;

#Accuracy
rf_bin_accuracy = str(accuracy_score(RandomforestClassification, binary_class_test))
print("Randomforest Classification Accuracy: " + rf_bin_accuracy)

################################################################################################################

# Load Neural network  from file
with open('Nov25_NeuralNetworkClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
NeuralNetworkClassification = pickle_model.predict(reduced_data_test)
RUL_test_Binary_Json['NeuralNetworkClassification'] = NeuralNetworkClassification;

#Accuracy
nn_bin_accuracy = str(accuracy_score(NeuralNetworkClassification, binary_class_test))
print("NeuralNetwork Classification Accuracy: " + nn_bin_accuracy)

################################################################################################################
# Load decision tree from file
with open('Nov25_DecisionTreeClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
DecisionTreeClassification = pickle_model.predict(reduced_data_test)
RUL_test_Binary_Json['DecisionTreeClassification'] = DecisionTreeClassification;

#print("DecisionTree ")
#print(DecisionTreeClassification)

binaryClassificationCount = Counter(DecisionTreeClassification)
#print("counts")
#print(binaryClassificationCount)

#Accuracy
dt_bin_accuracy =  str(accuracy_score(DecisionTreeClassification, binary_class_test))
print("DecisionTree Classification Accuracy: " +dt_bin_accuracy)

################################################################################################################
# Load SVM from file
with open('Nov25_SVMClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
SVMClassification = pickle_model.predict(reduced_data_test)
RUL_test_Binary_Json['SVMClassification'] = SVMClassification;

#Accuracy
svm_bin_accuracy =  str(accuracy_score(SVMClassification, binary_class_test))
print("SVM Classification Accuracy: " + svm_bin_accuracy)

################################################################################################################

#API Creation

bin_accuracy = {"RandomForest": rf_bin_accuracy, "NeuralNetwork": nn_bin_accuracy, 
        "Decisiontree": dt_bin_accuracy,"SVM":svm_bin_accuracy} 

print()
print("Accuracy of Binary Classification")
print(bin_accuracy)


test_array_binary_classification = list()
obj={}
for index, row in RUL_test_Binary_Json.iterrows():
    obj={'unit':row["Unit"],
         'Groundtruth_Rul':row["RUL"],
         'GroundtruthClassification':row["binary_class"],
         'RandomforestClassification':row["RandomforestClassification"],
         'NeuralNetworkClassification':row["NeuralNetworkClassification"],
       'DecisionTreeClassification':row["DecisionTreeClassification"],
       'SVMClassification':row["SVMClassification"]}
    test_array_binary_classification.append(obj)

########################################################## End of Binary Classification #####################################################
    
########################################################## Start of Multi Classification #####################################################
# Load Random forest  from file
with open('Nov25_RandomForestMultiClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
RandomforestMultiClassification = pickle_model.predict(reduced_data_test)
RUL_test_MultiClassification_Json['RandomforestMultiClassification'] = RandomforestMultiClassification; 

#Accuracy
#print(" --------------------------------------")
rf_multi_accuracy = str(accuracy_score(RandomforestMultiClassification, multi_class_test))
#print("RandomforestMultiClassification Accuracy: " + rf_multi_accuracy)

################################################################################################################

# Load Neural network  from file
with open('Nov25_NeuralNetworkMultiClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
NeuralNetworkMultiClassification = pickle_model.predict(reduced_data_test)   
RUL_test_MultiClassification_Json['NeuralNetworkMultiClassification'] = NeuralNetworkMultiClassification;

#Accuracy
nn_multi_accuracy = str(accuracy_score(NeuralNetworkMultiClassification, multi_class_test))
#print("NeuralNetworkMultiClassification Accuracy: " + nn_multi_accuracy)

################################################################################################################

# Load decision tree from file
with open('Nov25_DecisionTreeMultiClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
DecisionTreeMultiClassification = pickle_model.predict(reduced_data_test)
RUL_test_MultiClassification_Json['DecisionTreeMultiClassification'] = DecisionTreeMultiClassification;

#print("DecisionTreeMultiClassification ")
#print(DecisionTreeMultiClassification)

multiClassificationcount = Counter(DecisionTreeMultiClassification)
#print("multi classification counter ")
#print(multiClassificationcount)

#Accuracy
dt_multi_accuracy = str(accuracy_score(DecisionTreeMultiClassification, multi_class_test))
#print("DecisionTreeMultiClassification Accuracy: " + dt_multi_accuracy)

################################################################################################################


# Load SVM from file
with open('Nov25_SVMMultiClassification.pkl', 'rb') as file:
    pickle_model = pickle.load(file)
    
SVMMultiClassification = pickle_model.predict(reduced_data_test)
RUL_test_MultiClassification_Json['SVMMultiClassification'] = SVMMultiClassification;

#Accuracy
svm_multi_accuracy = str(accuracy_score(SVMMultiClassification, multi_class_test))
#print("SVMMultiClassification Accuracy: " + svm_multi_accuracy)
#print(" --------------------------------------")

################################################################################################################

#API Creation


multi_accuracy = {"RandomForest": rf_multi_accuracy, "NeuralNetwork": nn_multi_accuracy, 
        "Decisiontree": dt_multi_accuracy,"SVM":svm_multi_accuracy} 

#print(multi_accuracy)



test_array_multi_classification = list()
obj={}
for index, row in RUL_test_MultiClassification_Json.iterrows():
    obj={'unit':row["Unit"],
         'Rul':row["RUL"],
         'Groundtruth':row["multi_class"],
         'Randomforest':row["RandomforestMultiClassification"],
         'NeuralNetwork':row["NeuralNetworkMultiClassification"],
       'DecisionTree':row["DecisionTreeMultiClassification"],
       'SVM':row["SVMMultiClassification"]}
    test_array_multi_classification.append(obj)
    

#print(test_array_multi_classification)
########################################################## End of Multi Classification #####################################################
    

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/getRulByRegressionWithEngineId')
def getRulByRegressionWithEngineId():
    return jsonify({"data":test_array_regression_eachengineId})

@app.route('/getRulByRegressionWithEngineIdCountLessthan30')
def getRulByRegressionWithEngineIdCountLessthan30():
    return jsonify({"data":test_array_regression_eachengineId_lessthan30_count})


@app.route('/getMseOfRulByRegressionWithEngineId')
def getMseOfRulByRegressionWithEngineId():
    return jsonify({"data":rul_accuracy})

@app.route('/getBinaryClassificationWithEngineId')
def getBinaryClassificationWithEngineId():
    return jsonify({"data":test_array_binary_classification})


@app.route('/getAccuracyOfBinaryClassificationWithEngineId')
def getAccuracyOfBinaryClassificationWithEngineId():
    return jsonify({"data":bin_accuracy})


@app.route('/getMultiClassificationWithEngineId')
def getMultiClassificationWithEngineId():
    return jsonify({"data":test_array_multi_classification})

@app.route('/getAccuracyOfMultiClassificationWithEngineId')
def getAccuracyOfMultiClassificationWithEngineId():
    return jsonify({"data":multi_accuracy})


@app.route('/getCountOfBinaryClassificationWithEngineId')
def getCountOfBinaryClassificationWithEngineId():
    return jsonify({"data":binaryClassificationCount})

@app.route('/getCountOfMultiClassificationWithEngineId')
def getCountOfMultiClassificationWithEngineId():
    return jsonify({"data":multiClassificationcount})

################################################################################################################
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    
    
#####################################################################################################


