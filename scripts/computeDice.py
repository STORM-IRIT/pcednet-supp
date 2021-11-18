import sys, glob
from os import listdir, remove
from os.path import dirname, join, isfile, abspath
from io import StringIO

import numpy as np
import utilsmodule as um

script_path = dirname(abspath(__file__))
datasetPath = join(script_path,"data/")

e = 'shrec'

### Compute the dice coefficient used in Table 1,
# E Moscoso Thompson, G Arvanitis, K Moustakas, N Hoang-Xuan, E R Nguyen, et al..
# SHREC’19track: Feature Curve Extraction on Triangle Meshes.
# 12th EG Workshop 3D Object Retrieval 2019,May 2019, Gênes, Italy.


print ("  Processing experiment " + e)

# Fields loaded from the file
input_file_fields   = ['Precision', 'Recall', 'MCC', 'TP', 'FP', 'TN', 'FN']
# Expected range for the fields (used to compute the histogram bins)
input_fields_range  = [(0,1), (0,1), (-1,1), (0,1), (0,1), (0,1), (0,1)]
input_fields_bins   = []
# Functions used to summarize a field for the whole dataset
input_fied_summary = {
      "median": lambda buf: np.nanmedian(buf),
      "mean":   lambda buf: np.nanmean(buf)
    }

experimentPath = join(datasetPath, e)
experimentFile = join(script_path,"../assets/js/data_" + e + ".js")

approaches = [f for f in listdir(experimentPath) if isfile(join(experimentPath, f))]

# Data loaded from the file
rawdata = dict()
# Number of samples (3D models) used in this experiment
nbsamples = 0

# Load data
for a in approaches:
  if a.endswith(".txt"):
    aname = a[:-4]
    apath = join(experimentPath,a)

    # Load and skip comments, empty lines
    lines = [item.split() for item in tuple(open(apath, 'r')) if not item[0].startswith('#') or item == '']
    nbsamples = len(lines)

    # Current layout: lines[lineid][columnid]
    # Reshape so we have columns[columnid][lineid]
    rawdata[aname] = np.swapaxes( lines, 0, 1 )
    # Convert array of str to numpy array of numbers
    converter = lambda x:np.fromstring(', '.join(x) , dtype = np.float, sep =', ' )
    rawdata[aname] = list(map(converter,rawdata[aname]))

print ("    Loaded methods " + str(rawdata.keys()))


for method, data in rawdata.items():
    precision = data[0]
    recall = data[1]
    tp = data[3]
    fp = data[4]
    tn = data[5]
    fn = data[6]


    # Compute dice
    dice = (2.*tp) / (2.*tp + fn + fp)
    #dice = data[2]
    data.append(dice)

# Now print the latex table header
for method, data in rawdata.items():
    print (method + " & ", end = '')
print("\\\\ \n \hline")

# Find max value per model
maxid = []
for i in range (0,nbsamples):
    vmax = 0.
    mmax = 0
    m = 0
    for method, data in rawdata.items():
        if data[7][i] > vmax:
            vmax = data[7][i]
            mmax = m
        m = m+1
    maxid.append(mmax)

# Now print the latex table content
for i in range (0,nbsamples):
    m = 0
    for method, data in rawdata.items():
#        print ( str(data[:-1][i]) + " & " )
        valstr = "{:.2f}".format(data[7][i])
    
        if maxid[i] == m:
            valstr = "\\textbf{" + valstr + "}"
        print ( valstr + " & " , end = '')

        m = m+1
    print("\\\\ \n \hline")





