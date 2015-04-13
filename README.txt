if mosek is not working then
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/abir/mosek/7/tools/platform/linux64x86/bin/

to create the clean dataset 
python cleandata.py

for analysis and test use tester.py

for computing the weights given timeboundary
python train.py

*for computing the future opinions

*for tesing preictions againsts test data
