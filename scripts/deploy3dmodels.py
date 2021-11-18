
import sys, glob
from os import listdir, remove
from os.path import dirname, join, isfile, abspath, isdir
from io import StringIO
from plyfile import PlyData, PlyElement

import numpy as np
import utilsmodule as um

import glob, json

script_path    = dirname(abspath(__file__))
datasetPath    = join(script_path,"3dmodels/")
deploymentPath = sys.argv[1]
deploymentMode = sys.argv[2] # should be either 'local' or 'server'

experiments = [f for f in listdir(datasetPath) if dirname(join(datasetPath, f)) and not f.startswith('.')]


for eid, e in enumerate(experiments):
    if um.experiment_skip[e]: continue

    print ("  Processing experiment " + e)

    experimentFile = join(deploymentPath,"assets/js/3d_" + e + ".js")

    #try to load naming json file
    nameToId = dict()
    try:
        json_file = open(join(join(datasetPath,e),"nameToId.json"));
        nameToId = json.load(json_file)
    except FileNotFoundError:
        nameToId = dict()

    methodnames = [f for f in listdir(join(datasetPath,e)) if isdir(join(join(datasetPath,e), f))]

    print ("    Generate experiment file: " + experimentFile)
    jsfile = open(experimentFile, "w")

    jsfile.write( "var threeModels = {\n")

    for amethodname in methodnames:
        methodpath = join(join(datasetPath,e), amethodname)
        plyfiles = glob.glob(methodpath+'/*.ply')

        print ("      Processing method " + amethodname)

        jsfile.write( "  '" + um.methods_descr[amethodname.lower()] + "' : {\n" )

        # Load data
        for apath in plyfiles:
            abuff = apath.split('/')
            afilename = apath.split('/')[-1:][0]
            amodelname = afilename[:-4]
            # Model id in the dataset
            aid = nameToId[afilename] if afilename in nameToId.keys() else amodelname;
            print ("      Processing " + apath)

            descrpath = apath[:-3] + 'txt'

            with open(apath, 'rb') as f:

                # Loading description from file
                descr = "";
                try:
                    f = open(descrpath)
                    descr = ''.join([line.rstrip('\n') for line in f])
                except FileNotFoundError:
                    descr = "";

                # Format data to js string
                jsfile.write( "    '" + str(aid) + "' : {\n" )

                if deploymentMode == 'local':
                    plydata = PlyData.read(f)
                    el = plydata.elements[0];
                    nbsamples = len(el.data['x'])

                    concat_str_pos = StringIO()
                    concat_str_nor = StringIO()
                    concat_str_lab = StringIO()

                    for i in range (0, nbsamples):
                        p = el.data[i]
                        concat_str_pos.write( '{:.4f},{:.4f},{:.4f},'.format(p[0],p[1],p[2]))
                        concat_str_nor.write( '{:.2f},{:.2f},{:.2f},'.format(p[3],p[4],p[5]))

                        # fix rbg:
                        class_name = 'invalid';
                        color_tuple = (p[6],p[7],p[8]);
                        if color_tuple in um.classifier_find_color:
                            class_name = um.classifier_find_color[color_tuple];
                        else:
                            print("Error: inconsistent vertex input " + str(p[6]) + "-" + str(p[7]) + "-" + str(p[8]));
                        concat_str_lab.write( str(um.classifier_class_id[class_name])  + "," );

                    if amethodname.lower() == "gt":
                        jsfile.write( "      'vertices': new Float32Array( [" + concat_str_pos.getvalue()[:-1] + "] ),\n" );
                        jsfile.write( "      'normals': new Float32Array( [" + concat_str_nor.getvalue()[:-1] + "] ),\n" );
                    jsfile.write( "      'label': new Float32Array( [" + concat_str_lab.getvalue()[:-1] + "] ),\n" );
                jsfile.write( "      'description': '" + descr + "',\n" );
                jsfile.write( "      'plyfile': '" + afilename + "',\n" );

                jsfile.write("    },\n" )
        jsfile.write("  },\n" )

    jsfile.write( "}; // closing 3dmodels\n")
    jsfile.close()

