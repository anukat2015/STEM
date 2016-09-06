#! /bin/bash	

############################################################################################
## runs Duke and test it against the gold standard, then it saves the results on file ######
############################################################################################

java -Xmx5000m -cp "duke-core/target/*:duke-dist/target/*:duke-es/target/*:duke-json/target/*:duke-lucene/target/*:duke-mapdb/target/*:duke-mongodb/target/*:duke-server/target/*:lucene_jar/*" no.priv.garshol.duke.Duke --testfile=gold_standard_T2.txt --showmatches --batchsize=100000 test_data_FEIII/FFIEC_SEC.xml > results_T2.txt
