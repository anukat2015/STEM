import os
import numpy as np
import pandas as pd
import subprocess
import optparse
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn import grid_search
from sklearn.cross_validation import train_test_split
from stacking_create_training_set import stacking_create_training_set
import xml.etree.ElementTree as ET

###################################################
# Testing the model on pure test set of 0.5 size ##
###################################################
########## OUTPUT: p,r,f1 on test set #############
###################################################

#defining the options of the script

#INPUTS: -i duke_config.xml, -N number_of_configurations, -a amplitude_of_perturbation, -g gold_standard_name

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
parser.add_option('-N','--number', dest = 'N', help = 'number of classifiers',type = int)
parser.add_option('-a','--amplitude', dest = 'a', help = 'amplitude of perturbation',type = float)
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')

(options, args) = parser.parse_args()

if options.file_name is None:
   options.file_name = raw_input('Enter file name:')

if options.N is None:
    options.N = raw_input('Enter number of classifiers:')

if options.a is None:
    options.a = 0.05 #default to 0.05

if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file name:')


file_name = options.file_name #define the variables
gold_standard_name = options.gold_standard_name
N = int(options.N)
a = float(options.a)

#open files for writing

output_file_raw = open('ensemble_duke_output_raw_T2_n%d.txt' %N,'w') 

#output_file = open('ensemble_duke_stacking_output_T2_n%d.txt' %N,'w') 

gold_standard_read = open(gold_standard_name,'rU')

#iterate for each tweaked configuration

#read actual threshold

tree = ET.parse(file_name)
root = tree.getroot()

for thresh in root.iter('threshold'):
    central_thresh = float(thresh.text) #central value of the threshold

thresholds = np.linspace(central_thresh - a/2, central_thresh + a/2, N)


for threshold in thresholds:

    for thresh in root.iter('threshold'):
        thresh.text = str(threshold)
        thresh.set('updated','yes')

    tree.write('../../../config/FEIII2016/copy_T2.xml') 

    java_command = ["java","-Xmx5000m", "-cp", "../../../lib/Duke/duke-core/target/*:../../../lib/Duke/duke-dist/target/*:../../../lib/Duke/duke-es/target/*:../../../lib/Duke/duke-json/target/*:../../../lib/Duke/duke-lucene/target/*:../../../lib/Duke/duke-mapdb/target/*:../../../lib/Duke/duke-mongodb/target/*:../../../lib/Duke/duke-server/target/*:../../../lib/Duke/lucene_jar/*", "no.priv.garshol.duke.Duke", "--showmatches","--batchsize=100000", "--threads=4", "../../../config/FEIII2016/copy_T2.xml"]

    output_file_raw.write(subprocess.check_output(java_command)) #call duke on the copy.xml file and write the raw output on file
    
    output_file_raw.write('\n')
    output_file_raw.write('End of run\n') 
    
output_file_raw.close()

#duke_output_parser('ensemble_duke_output_raw_T2_n%d.txt' %N, 'ensemble_duke_output_union_T2_n%d.txt' %N,'FFIEC','SEC')

#create the training set, named training_set_T1_n%d.csv

stacking_create_training_set('ensemble_duke_output_raw_T2_n%d.txt' %N,'training_set_T2_n%d.csv' %N, gold_standard_name, N)

#read it and make machine learning on it

data = pd.read_csv('training_set_T2_n%d.csv' %N)

#turn data into arrays
X = data.values[:,2:(N+2)] #x variables
y = np.array(data['y']) #class variables

#p_scores = []
#r_scores = []
#f1_scores = []

#T = 5

#repeat the split many times and average the results in order to cancel random fluctuations
#for i in range(T):
#stratified split in train and test set 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50, stratify = y, random_state = 20)

    # fit an SVM with rbf kernel
clf = SVC( kernel = 'rbf',cache_size = 1000)

#hyper-parameter optimization through grid-search cross validation

parameters = {'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}

gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 4)
gs_rbf.fit(X_train,y_train)

#select the best hyper-parameters
clf = gs_rbf.best_estimator_

#save the output
y_predict = np.reshape(clf.predict(X_test),(len(X_test),1))

#p_scores.append(precision_score(y_test,y_predict,average = 'binary'))

#r_scores.append(recall_score(y_test,y_predict,average = 'binary'))

#f1_scores.append(f1_score(y_test,y_predict,average = 'binary'))

#p = np.mean(p_scores)

#r = np.mean(r_scores)

#f1 = np.mean(f1_scores)

p = precision_score(y_test,y_predict,average = 'binary')

r = recall_score(y_test,y_predict,average = 'binary')

f1 = f1_score(y_test,y_predict,average = 'binary')

print "%.3f,%.3f,%.3f" %(p,r,f1)