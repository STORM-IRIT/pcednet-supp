
import sys, glob
from os import listdir, remove
from os.path import dirname, join, isfile, abspath
from io import StringIO

import numpy as np
import utilsmodule as um

script_path    = dirname(abspath(__file__))
datasetPath    = join(script_path,"data/")
deploymentPath = sys.argv[1]

experiments = [f for f in listdir(datasetPath) if dirname(join(datasetPath, f)) and not f.startswith('.')]


for eid, e in enumerate(experiments):
    if um.experiment_skip[e]: continue

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
    experimentFile = join(deploymentPath,"assets/js/data_" + e + ".js")

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
            converter = lambda x:np.fromstring(', '.join(x) , dtype = float, sep =', ' )
            rawdata[aname] = list(map(converter,rawdata[aname]))


    print ("    Loaded methods " + str(rawdata.keys()))


    # Compute new fields from loaded ones, and normalize true/false-positive/negative
    input_file_fields.append("F1")
    input_fields_range.append((0,1))
    input_file_fields.append("Accuracy")
    input_fields_range.append((0,1))
    input_file_fields.append("Selectivity")
    input_fields_range.append((0,1))
    input_file_fields.append("IoU")
    input_fields_range.append((0,1))
    for method, data in rawdata.items():
        precision = data[0]
        recall = data[1]
        tp = data[3]
        fp = data[4]
        tn = data[5]
        fn = data[6]
        data.append(2.*(precision*recall)/(precision+recall)) # f1score
        data.append((tp+tn)/(tp+tn+fp+fn)) # accuracy
        data.append((tn)/(tn+fp)) # Selectivity
        data.append((tp)/(tp+fp+fn)) # IOU



        # normalize
        nbpositivepoints = tp+fp
        nbnegativepoints = tn+fn
        nbtruepoints = tp+tn
        nbfalsepoints = fp+fn
#        data[3] = np.divide(tp, nbpositivepoints)
#        data[4] = np.divide(fp, nbpositivepoints)
#        data[5] = np.divide(tn, nbnegativepoints)
#        data[6] = np.divide(fn, nbnegativepoints)
        data[3] = np.divide(tp, nbtruepoints)
        data[4] = np.divide(fp, nbfalsepoints)
        data[5] = np.divide(tn, nbtruepoints)
        data[6] = np.divide(fn, nbfalsepoints)

        # filter inf points

    # Compute the histogram bins for the fields
    nbbins = min(75,int(np.ceil(nbsamples* 0.8)))
    for fieldid, (fmin, fmax) in enumerate(input_fields_range):
        input_fields_bins.append( np.linspace(fmin, fmax, nbbins) )


    # Stores the curves data describing the experiment
    curvesdata = dict(); # = { "median": { 'Precision'=[], 'Recall' =[] }, ...}
    for s in input_fied_summary.keys(): # median, mean
        curvesdata[s] = dict()
        for field in input_file_fields: # Precision, Recall, ...
            curvesdata[s][field] = []


    print ("    Generate experiment file: " + experimentFile)
    jsfile = open(experimentFile, "w")

    jsfile.write( "var datasets = {\n")



    for method, data in rawdata.items():
        jsfile.write( "                  '" + method + "' : {\n" );
        jsfile.write( "                    'Name' : '" + um.methods_descr[method] + "',\n" )
        jsfile.write( "                    'NamePaper' : '" + um.methods_descr_short_paper[method] + "',\n" )
        jsfile.write( "                    'FigureFilename' : '" + um.methods_figure_name[method] + "',\n" )

        for index, value in enumerate ( input_file_fields ):
            # Write field values
            jsfile.write( "                    '" + value + "' : [" )
            concat_str = StringIO()
            for p in data[index]:
                concat_str.write( " " + str(p) + "," )
            jsfile.write( concat_str.getvalue().replace("nan", "NaN").replace("inf", "Infinity")[:-1] + "],\n" )

            # Write field values distribution
            jsfile.write( "                    '" + value + "-Hist' : [" )
            concat_str = StringIO()
            for p in np.histogram(data[index], input_fields_bins[index])[0]:
                concat_str.write( " " + str(p) + "," )
            jsfile.write( concat_str.getvalue().replace("nan", "NaN").replace("inf", "Infinity")[:-1] + "],\n" )
            # Compute curves summaries
            for name, fun in input_fied_summary.items():
                curvesdata[name][value].append(fun(data[index]))


        jsfile.write( "                  },\n")



    jsfile.write( "               };\n")

    # Generate curve data
    #  1. PR scatter plot: one point sample per dataset with median precision and recall
    jsfile.write( "var dataset_properties = {\n")
    jsfile.write( "  'curves' : {\n" );
    for curvename, curvearray in curvesdata.items():
        jsfile.write( "    '" + curvename + "' : {\n" );

        # Loop over data, e.g., 'Precision': [], 'Recall': [], 'MCC':[]
        for fieldname, fieldvalues in curvearray.items():
            # Write field values
            jsfile.write( "      '" + fieldname + "' : [");
            concat_str = StringIO()
            for p in fieldvalues:
                concat_str.write( " " + str(p) + "," )
            jsfile.write( concat_str.getvalue().replace("nan", "NaN").replace("inf", "Infinity")[:-1] + "],\n" )

        jsfile.write( "    },\n")

    jsfile.write( "  },\n")

    jsfile.write( "  'fields_properties' : {\n" );
    jsfile.write( "    'range' : {\n" );
    # Loop over data, e.g., 'Precision': [], 'Recall': [], 'MCC':[]
    for fieldid, fieldname in enumerate(input_file_fields):
        # Write field values
        jsfile.write( "      '" + fieldname + "' : [");
        concat_str = StringIO()
        for p in input_fields_range[fieldid]:
            concat_str.write( " " + str(p) + "," )
        jsfile.write( concat_str.getvalue()[:-1] + "],\n" )
    jsfile.write( "    },\n")


    jsfile.write( "    'bins' : {\n" );
    # Loop over data, e.g., 'Precision': [], 'Recall': [], 'MCC':[]
    for fieldid, fieldname in enumerate(input_file_fields):
        # Write field values
        jsfile.write( "      '" + fieldname + "' : [");
        concat_str = StringIO()
        for p in input_fields_bins[fieldid]:
            concat_str.write( " " + str(p) + "," )
        jsfile.write( concat_str.getvalue()[:-1] + "],\n" )
    jsfile.write( "    },\n")


    jsfile.write( "    'description' : {\n" );
    # Loop over data, e.g., 'Precision': [], 'Recall': [], 'MCC':[]
    for fieldid, fieldname in enumerate(input_file_fields):
        # Write field values
        jsfile.write( "      '" + fieldname + "' : '" + um.input_fields_description[fieldname] + "',\n" );
    jsfile.write( "    },\n")



    jsfile.write( "  },\n")

    jsfile.write( "  'methods' : {\n" );
    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " '" + um.methods_descr[method] + "'," )
    jsfile.write( "    'Names' : [" + concat_str.getvalue()[:-1] + "],\n");

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " '" + um.methods_descr_short[method] + "'," )
    jsfile.write( "    'ShortNames' : [" + concat_str.getvalue()[:-1] + "],\n");

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " " + um.methods_nbclasses[method] + "," )
    jsfile.write( "    'NbClasses' : [" + concat_str.getvalue()[:-1] + "],\n" )

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " " + um.methods_is_pced[method] + "," )
    jsfile.write( "    'IsPCED' : [" + concat_str.getvalue()[:-1] + "],\n" )

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " '" + um.methods_legend_group[method] + "'," )
    jsfile.write( "    'LegendGroup' : [" + concat_str.getvalue()[:-1] + "],\n" )

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " " + um.methods_priority[method] + "," )
    jsfile.write( "    'Priority' : [" + concat_str.getvalue()[:-1] + "],\n" )

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " " + um.methods_is_gls[method] + "," )
    jsfile.write( "    'IsGLS' : [" + concat_str.getvalue()[:-1] + "],\n" )

    concat_str = StringIO()
    for method in rawdata.keys():
        concat_str.write( " '" + um.methods_base_marker[method] + "'," )
    jsfile.write( "    'Markers' : [" + concat_str.getvalue()[:-1] + "],\n" )
    jsfile.write( "  },\n")

    jsfile.write( "};\n")

