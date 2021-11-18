import re

classifier_class_color = {
    'flat'   : '180, 180, 180',
    'sharp'  : '255,   0,   0',
    'smooth' : '255, 255,   0',
    'invalid': '  0,   0, 255'
}

classifier_class_id = {
    'flat'   : 0,
    'smooth' : 1,
    'sharp'  : 2,
    'invalid': -1
}

classifier_find_color = {
    (255,255,255)   : 'flat',
    (168,  0,  0)   : 'sharp',
    (255,  0,  0)   : 'sharp',
    (  0,  0,  0)   : 'smooth',
    (255,196, 93)   : 'smooth',
    (255,215,  0)   : 'smooth'
}

methods_descr_short = {
    "pced": "PCED(D)",
    "tc": "PCED(D)",
    "tcec": "PCED(E)",
    "abc": "PCED(A)",
#    "abcarch4": "PCED(D)-ABL-ARCH4",
#    "abcarch6": "PCED(D)-ABL-ARCH6",
#    "abcarch8": "PCED(D)-ABL-ARCH8",
#    "abcarch12": "PCED(D)-ABL-ARCH12",
#    "abcarch32": "PCED(D)-ABL-ARCH32",
    "abcreduc4": "PCED(D)-ABL-REDUC4",
    "abcreduc8": "PCED(D)-ABL-REDUC8",
    "abcreduc32": "PCED(D)-ABL-REDUC32",
    "abcreduc64": "PCED(D)-ABL-REDUC64",
    "abcreduc128": "PCED(D)-ABL-REDUC128",
    "shrec": "PCED(S)",
    "pcedss": "PCED(D) Ext",
    "fc": "FC(D)",
    "fc2c": "FC(D)",
    "fcabc": "FC(A)",
    "fcshrec": "FC(S)",
    "fcss": "FC(D) S+S",
    "cnn": "CNN(D)",
    "cnn2c": "CNN(D)",
    "cnnabc": "CNN(A)",
    "cnnshrec": "CNN(S)",
    "cnnss": "CNN(D) S+S",
    "ca": "CA",
    "fee": "FEE",
    "pcpnet": "PCPNet(D)",
    "pcpnetabc": "PCPNet(A)",
    "ecnet": "ECNet",
    "gt": "GT"
}

#Used only to produce svg for the paper figures
methods_descr_short_paper = {
    "pced":        "\\\\pced (\\\\dtsDFLT)",
    "tc":          "\\\\pcedtc (\\\\dtsDFLT)",
    "tcec": 	   "\\\\pcedtc (\\\\dtsEC)",
    "abc":         "\\\\pcedtc (\\\\dtsABC)",
    "abcreduc4":   "\\\\pced (\\\\dtsDFLT) - 4 scales",
    "abcreduc8":   "\\\\pced (\\\\dtsDFLT) - 8 scales",
    "abcreduc32":  "\\\\pced (\\\\dtsDFLT) - 32 scales",
    "abcreduc64":  "\\\\pced (\\\\dtsDFLT) - 64 scales",
    "abcreduc128": "\\\\pced (\\\\dtsDFLT) - 128 scales",
    "shrec":       "\\\\pced (\\\\dtsSHREC)",
    "pcedss":      "\\\\pced (\\\\dtsDFLT)+",
    "fc":          "\\\\fc (\\\\dtsDFLT)",
    "fc2c":        "\\\\fctc (\\\\dtsDFLT)",
    "fcabc":       "\\\\fctc (\\\\dtsABC)",
    "fcshrec":     "\\\\fc (\\\\dtsSHREC)",
    "fcss":        "\\\\fctc (\\\\dtsDFLT)+",
    "cnn":         "\\\\cnn (\\\\dtsDFLT)",
    "cnn2c":       "\\\\cnntc (\\\\dtsDFLT)",
    "cnnabc":      "\\\\cnntc (\\\\dtsABC)",
    "cnnshrec":    "\\\\cnn (\\\\dtsSHREC)",
    "cnnss":       "\\\\cnn (\\\\dtsDFLT)+",
    "ca":          "\\\\ca",
    "fee":         "\\\\fee",
    "pcpnet":      "\\\\pcp (\\\\dtsDFLT)",
    "pcpnetabc":   "\\\\pcptc (\\\\dtsABC)",
    "ecnet":       "\\\\ecnet",
    "gt":          "GT"
}

#Used only to produce svg for the paper figures
methods_figure_name = {
    "pced": "pced-default",
    "tc": "pcedtc-default",
    "tcec": "pcedtc-ec",
    "abc": "pcedtc-abc",
    "abcreduc4": "pced_reduc_4",
    "abcreduc8": "pced_reduc_8",
    "abcreduc32": "pced_reduc_32",
    "abcreduc64": "pced_reduc_64",
    "abcreduc128": "pced_reduc_128",
    "shrec": "pced-shrec",
    "pcedss": "pcedss",
    "fc": "fc-default",
    "fc2c": "fctc-default",
    "fcabc": "fctc-abc",
    "fcshrec": "fctc-shrec",
    "fcss": "fcss",
    "cnn": "cnn-default",
    "cnn2c": "cnntc-default",
    "cnnabc": "cnntc-abc",
    "cnnshrec": "cnn-shrec",
    "cnnss": "cnnss",
    "ca": "ca",
    "fee": "fee",
    "pcpnet": "pcpnet-default",
    "pcpnetabc": "pcpnet-abc",
    "ecnet": "ecnet",
    "gt": "GT"
}


methods_descr = {
    "pced": "PCED (trained on Default)",
    "tc": "PCED-2C (trained on Default)",
    "tcec": "PCED-2C (trained on EC)",
    "abc": "PCED-2C (trained on ABC)",
#    "abcarch4": "PCED (trained on Default) - Ablation Study (same arch.) 4",
#    "abcarch6": "PCED (trained on Default) - Ablation Study (same arch.) 6",
#    "abcarch8": "PCED (trained on Default) - Ablation Study (same arch.) 8",
#    "abcarch12": "PCED (trained on Default) - Ablation Study (same arch.) 12",
#    "abcarch32": "PCED (trained on Default) - Ablation Study (same arch.) 32",
    "abcreduc4": "PCED (trained on Default) - 4 scales",
    "abcreduc8": "PCED (trained on Default) - 8 scales",
    "abcreduc32": "PCED (trained on Default) - 32 scales",
    "abcreduc64": "PCED (trained on Default) - 64 scales",
    "abcreduc128": "PCED (trained on Default) - 128 scales",
    "shrec": "PCED-2C (trained on Shrec)",
    "pcedss": "PCED (trained on Default - P = Sharp+Smooth)",
    "fc": "FC (trained on Default)",
    "fc2c": "FC-2C (trained on Default)",
    "fcabc": "FC-2C (trained on ABC)",
    "fcshrec": "FC-2C (trained on Shrec)",
    "fcss": "FC (trained on Default - P = Sharp+Smooth)",
    "cnn": "CNN (trained on Default)",
    "cnn2c": "CNN-2C (trained on Default)",
    "cnnabc": "CNN-2C (trained on ABC)",
    "cnnshrec": "CNN-2C (trained on Shrec)",
    "cnnss": "CNN (trained on Default - P = Sharp+Smooth)",
    "ca": "Covariance Analysis",
    "fee": "Feature Edge Extraction",
    "pcpnet": "PCPNet (trained on Default)",
    "pcpnetabc": "PCPNet (trained on ABC)",
    "ecnet": "Edge-aware Point set Consolidation Network (Pre-trained)",
    "gt": "Ground Truth"
}

methods_nbclasses = {
    "pced": "3",
    "pcedss": "3",
    "tc": "2",
    "tcec": "2",
    "abc": "2",
#    "abcarch4": "3",
#    "abcarch6": "3",
#    "abcarch8": "3",
#    "abcarch12": "3",
#    "abcarch32": "3",
    "abcreduc4": "3",
    "abcreduc8": "3",
    "abcreduc32": "3",
    "abcreduc64": "3",
    "abcreduc128": "3",
    "shrec": "2",
    "fc": "3",
    "fcss": "3",
    "fc2c": "2",
    "fcabc": "2",
    "fcshrec": "2",
    "cnn": "3",
    "cnnss": "3",
    "cnn2c": "2",
    "cnnabc": "2",
    "cnnshrec": "2",
    "ca": "2",
    "fee": "2",
    "pcpnet": "3",
    "pcpnetabc": "3",
    "ecnet": "2"
}

# used to order the curves in the graphs
methods_priority = {
    "pced": "100",
    "pcedss": "99",
    "abc": "98",
    "tcec": "97",
#    "abcarch4": "13",
#    "abcarch6": "13",
#    "abcarch8": "13",
#    "abcarch12": "13",
#    "abcarch32": "13",
    "abcreduc4": "13",
    "abcreduc8": "13",
    "abcreduc32": "13",
    "abcreduc64": "13",
    "abcreduc128": "13",
    "shrec": "97",
    "tc": "96",
    "fc": "80",
    "fcss": "79",
    "fcabc": "78",
    "fcshrec": "77",
    "fc2c": "76",
    "cnn": "60",
    "cnnss": "59",
    "cnnabc": "58",
    "cnnshrec": "57",
    "cnn2c": "56",
    "ca": "20",
    "fee": "15",
    "pcpnet": "10",
    "pcpnetabc": "11",
    "ecnet": "25"
}

# used to order the curves in the graphs
methods_legend_group = {
    "pced": "pced",
    "pcedss": "pced",
    "abc": "pced",
    "tcec": "pced",
#    "abcarch4": "ablation-same arch.",
#    "abcarch6": "ablation-same arch.",
#    "abcarch8": "ablation-same arch.",
#    "abcarch12": "ablation-same arch.",
#    "abcarch32": "ablation-same arch.",
    "abcreduc4": "ablation-same reduc rate",
    "abcreduc8": "ablation-same reduc rate",
    "abcreduc32": "ablation-same reduc rate",
    "abcreduc64": "ablation-same reduc rate",
    "abcreduc128": "ablation-same reduc rate",
    "shrec": "pced",
    "tc": "pced",
    "fc": "Fully Connected",
    "fcss": "Fully Connected",
    "fcabc": "Fully Connected",
    "fcshrec": "Fully Connected",
    "fc2c": "Fully Connected",
    "cnn": "CNN",
    "cnnss": "CNN",
    "cnnabc": "CNN",
    "cnnshrec": "CNN",
    "cnn2c": "CNN",
    "ca": "Other",
    "fee": "Other",
    "pcpnet": "Other",
    "pcpnetabc": "Other",
    "ecnet": "Other"
}

methods_is_pced = {
    "pced": "true",
    "pcedss": "true",
    "tc": "true",
    "tcec": "true",
    "abc": "true",
#    "abcarch4": "true",
#    "abcarch6": "true",
#    "abcarch8": "true",
#    "abcarch12": "true",
#    "abcarch32": "true",
    "abcreduc4": "true",
    "abcreduc8": "true",
    "abcreduc32": "true",
    "abcreduc64": "true",
    "abcreduc128": "true",
    "shrec": "true",
    "fc": "false",
    "fcss": "false",
    "fc2c": "false",
    "fcabc": "false",
    "fcshrec": "false",
    "cnn": "false",
    "cnnss": "false",
    "cnn2c": "false",
    "cnnabc": "false",
    "cnnshrec": "false",
    "ca": "false",
    "fee": "false",
    "pcpnet": "false",
    "pcpnetabc": "false",
    "ecnet": "false"
}

methods_is_gls = {
    "pced": "true",
    "pcedss": "true",
    "tc": "true",
    "tcec": "true",
    "abc": "true",
#    "abcarch4": "true",
#    "abcarch6": "true",
#    "abcarch8": "true",
#    "abcarch12": "true",
#    "abcarch32": "true",
    "abcreduc4": "true",
    "abcreduc8": "true",
    "abcreduc32": "true",
    "abcreduc64": "true",
    "abcreduc128": "true",
    "shrec": "true",
    "fc": "true",
    "fcss": "true",
    "fc2c": "true",
    "fcabc": "true",
    "fcshrec": "true",
    "cnn": "true",
    "cnnss": "true",
    "cnn2c": "true",
    "cnnabc": "true",
    "cnnshrec": "true",
    "ca": "false",
    "fee": "false",
    "pcpnet": "true",
    "pcpnetabc": "true",
    "ecnet": "false"
}

methods_base_marker = {
    "pced": "circle",
    "pcedss": "circle",
    "tc": "circle",
    "tcec": "circle",
    "abc": "circle",
#    "abcarch4": "circle",
#    "abcarch6": "circle",
#    "abcarch8": "circle",
#    "abcarch12": "circle",
#    "abcarch32": "circle",
    "abcreduc4": "circle",
    "abcreduc8": "circle",
    "abcreduc32": "circle",
    "abcreduc64": "circle",
    "abcreduc128": "circle",
    "shrec": "circle",
    "fc": "square",
    "fcss": "square",
    "fc2c": "square",
    "fcabc": "square",
    "fcshrec": "square",
    "cnn": "diamond",
    "cnnss": "diamond",
    "cnn2c": "diamond",
    "cnnabc": "diamond",
    "cnnshrec": "diamond",
    "ca": "cross",
    "fee": "cross",
    "pcpnet": "triangle",
    "pcpnetabc": "triangle",
    "ecnet": "triangle"
}

experiment_names = {
    "abc": "ABC Dataset",
    "abc_noise_0.04": "ABC Dataset (noisy version)",
    "shrec": "Feature Curve Extraction on Triangle Meshes (SHREC'19) - Sharp edges",
    "default": "Default Dataset: simple geometrical objects with noise",
}

experiment_fieldslogscale = {
    "abc": True,
    "abc_noise_0.04": True,
    "shrec": False,
    "default": False,
}

experiment_skip = {
    "abc": False,
    "abc_noise_0.04": False,
    "shrec": False,
    "default": False,
}
experiment_descriptions = {
    "abc": '''<p>This experiment consists in classifying edge points on the chunk <code>0000</code> (7167 models) of the <a target="_blank" href="https://deep-geometry.github.io/abc-dataset/">ABC Dataset</a>. We randomly selected 200 and 50 models for training and validation, respectively:</p><ul><li>Training models: <code>0037, 0039, 0044, 0048, 0101, 0116, 0124, 0137, 0143, 0150, 0156, 0189, 0202, 0230, 0233, 0254, 0299, 0310, 0324, 0342, 0374, 0382, 0387, 0392, 0435, 0457, 0467, 0480, 0501, 0502, 0513, 0533, 0542, 0550, 0551, 0553, 0584, 0603, 0618, 0640, 0646, 0654, 0662, 0664, 0673, 0683, 0686, 0688, 0746, 0753, 0794, 0840, 0871, 0901, 0915, 0925, 0950, 0959, 0980, 0982, 1001, 1022, 1035, 1043, 1054, 1058, 1080, 1095, 1139, 1142, 1143, 1154, 1173, 1193, 1197, 1203, 1226, 1231, 1242, 1250, 1263, 1299, 1301, 1314, 1341, 1361, 1369, 1374, 1387, 1390, 1393, 1401, 1403, 1405, 1413, 1418, 1452, 1473, 1521, 1532, 1536, 1538, 1559, 1589, 1599, 1607, 1608, 1611, 1613, 1617, 1627, 1634, 1675, 1697, 1700, 1713, 1722, 1724, 1729, 1739, 1744, 1751, 1761, 1811, 1840, 1841, 1848, 1877, 1896, 1898, 1903, 1913, 1944, 1950, 1954, 1955, 1961, 1967, 2034, 2036, 2046, 2082, 2089, 2107, 2118, 2131, 2135, 2138, 2161, 2170, 2177, 2189, 2201, 2207, 2236, 2245, 2295, 2304, 2310, 2329, 2340, 2354, 2358, 2389, 2425, 2426, 2427, 2430, 2432, 2435, 2438, 2452, 2472, 2487, 2492, 2499, 2517, 2520, 2538, 2540, 2584, 2586, 2596, 2609, 2678, 2685, 2686, 2690, 2714, 2719, 2726, 2732, 2744, 2763, 2768, 2771, 2776, 2777, 2799, 2800</code>,</li><li>Validation models: <code>0008, 0091, 0138, 0198, 0277, 0353, 0402, 0487, 0541, 0576, 0643, 0667, 0713, 0844, 0939, 0994, 1051, 1106, 1155, 1217, 1258, 1323, 1384, 1402, 1433, 1534, 1594, 1612, 1672, 1716, 1743, 1813, 1884, 1937, 1957, 2038, 2117, 2139, 2192, 2248, 2337, 2392, 2431, 2465, 2507, 2572, 2667, 2703, 2738, 2775</code>.</li></ul></p>''',
    "abc_noise_0.04": '''<p>This experiment consists in classifying edge points on a noisy version of the chunk <code>0000</code> (7167 models) of the <a target="_blank" href="https://deep-geometry.github.io/abc-dataset/">ABC Dataset</a>. We randomly selected 200 and 50 models for training and validation, respectively:</p><ul><li>Training models: <code>0037, 0039, 0044, 0048, 0101, 0116, 0124, 0137, 0143, 0150, 0156, 0189, 0202, 0230, 0233, 0254, 0299, 0310, 0324, 0342, 0374, 0382, 0387, 0392, 0435, 0457, 0467, 0480, 0501, 0502, 0513, 0533, 0542, 0550, 0551, 0553, 0584, 0603, 0618, 0640, 0646, 0654, 0662, 0664, 0673, 0683, 0686, 0688, 0746, 0753, 0794, 0840, 0871, 0901, 0915, 0925, 0950, 0959, 0980, 0982, 1001, 1022, 1035, 1043, 1054, 1058, 1080, 1095, 1139, 1142, 1143, 1154, 1173, 1193, 1197, 1203, 1226, 1231, 1242, 1250, 1263, 1299, 1301, 1314, 1341, 1361, 1369, 1374, 1387, 1390, 1393, 1401, 1403, 1405, 1413, 1418, 1452, 1473, 1521, 1532, 1536, 1538, 1559, 1589, 1599, 1607, 1608, 1611, 1613, 1617, 1627, 1634, 1675, 1697, 1700, 1713, 1722, 1724, 1729, 1739, 1744, 1751, 1761, 1811, 1840, 1841, 1848, 1877, 1896, 1898, 1903, 1913, 1944, 1950, 1954, 1955, 1961, 1967, 2034, 2036, 2046, 2082, 2089, 2107, 2118, 2131, 2135, 2138, 2161, 2170, 2177, 2189, 2201, 2207, 2236, 2245, 2295, 2304, 2310, 2329, 2340, 2354, 2358, 2389, 2425, 2426, 2427, 2430, 2432, 2435, 2438, 2452, 2472, 2487, 2492, 2499, 2517, 2520, 2538, 2540, 2584, 2586, 2596, 2609, 2678, 2685, 2686, 2690, 2714, 2719, 2726, 2732, 2744, 2763, 2768, 2771, 2776, 2777, 2799, 2800</code>,</li><li>Validation models: <code>0008, 0091, 0138, 0198, 0277, 0353, 0402, 0487, 0541, 0576, 0643, 0667, 0713, 0844, 0939, 0994, 1051, 1106, 1155, 1217, 1258, 1323, 1384, 1402, 1433, 1534, 1594, 1612, 1672, 1716, 1743, 1813, 1884, 1937, 1957, 2038, 2117, 2139, 2192, 2248, 2337, 2392, 2431, 2465, 2507, 2572, 2667, 2703, 2738, 2775</code>.</li></ul></p><p>Noisy samples are obtained by applying displacement noise in the direction of the normal vector, with <code>magniture=4% of the object bounding box</code></p>''',
    "shrec": '''''',
    "default": '''''',
}

input_fields_description  = {
    'Precision': """<p>Precision (also denoted positive predictive value -- PPV) measures the proportion of positive identifications that was actually correct (higher is better). It is defined as:</p>$$\\\\displaystyle {\\\\text{precision}} = \\\\frac{TP}{TP + FP}$$""",
    'Recall': """<p>Recall (also denoted sensitivity, hit rate, or true positive rate  -- TPR) measures the proportion of actual positives that was identified correctly (higher is better). It is defined as:</p>$$\\\\displaystyle {\\\\text{recall}} = \\\\frac{TP}{TP + FN}$$""",
    'MCC': """<p>The Matthews Correlation Coefficient (MCC) is a correlation coefficient between the observed and predicted binary classifications; it returns a value between −1 and +1. A coefficient of +1 represents a perfect prediction, 0 no better than random prediction and −1 indicates total disagreement between prediction and observation. It is defined as:</p>$$\\\\displaystyle {\\\\text{MCC}}={\\\\frac {TP\\\\times TN-FP\\\\times FN}{\\\\sqrt {(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}}$$<p>Advantages of MCC over Accuracy and F1 score are given <a href="https://en.wikipedia.org/wiki/Matthews_correlation_coefficient#Advantages_of_MCC_over_accuracy_and_F1_score" target="_blank">here</a>.</p>""",
    'TP': "THIS FIELD SHOULD NOT BE VISIBLE",
    'FP': "THIS FIELD SHOULD NOT BE VISIBLE",
    'TN': "THIS FIELD SHOULD NOT BE VISIBLE",
    'FN': "THIS FIELD SHOULD NOT BE VISIBLE",
    'Selectivity': """<p>Selectivity (also denoted specificity or true negative rate -- TNR) measures the proportion of actual positives that are correctly identified as such (higher is better). It is defined as:</p>$$\\\\displaystyle {\\\\text{selectivity}} = \\\\frac{TN}{TN + FP}$$""",
    'F1': """<p>F1 score measures is a measure of a test\\'s accuracy. For binary classification, F1 is defined as follows:</p>$$\\\\displaystyle {\\\\text{F1}} = 2 . \\\\frac{\\\\displaystyle {\\\\text{precision}} \\\\times \\\\displaystyle {\\\\text{recall}}}{\\\\displaystyle {\\\\text{precision}} + \\\\displaystyle {\\\\text{recall}}}$$<p>Note that F1 ignores the True Negatives and thus is misleading for unbalanced classe, which is our case in general, ie. the number of edge points (True Positives) is in general very small in comparison to non-edge points (True Negatives). Advantages of MCC over Accuracy and F1 score are given <a href="https://en.wikipedia.org/wiki/Matthews_correlation_coefficient#Advantages_of_MCC_over_accuracy_and_F1_score" target="_blank">here</a>.</p>""",
    'Accuracy': """<p>Accuracy measures is the fraction of predictions our model got right. For binary classification, accuracy is defined as follows:</p>$$\\\\displaystyle {\\\\text{accuracy}} = \\\\frac{TP+TN}{TP + TN + FP + FN}$$<p>Advantages of MCC over Accuracy and F1 score are given <a href="https://en.wikipedia.org/wiki/Matthews_correlation_coefficient#Advantages_of_MCC_over_accuracy_and_F1_score" target="_blank">here</a>.</p>""",
    'IoU': """<p>Intersection over Union, also known as Jaccard Index. This measure estimates a likelihood of an element being positive, if it is not correctly classified a negative element. It is defined as follows:</p>$$\\\\displaystyle {\\\\text{IoU}} = \\\\frac{TP}{TP + FP + FN}$$""",
}


# Usage examples:
#    rep = {
#        "@title_page_class1@": "current" if e == "default" else "",
#        "@title_page_class2@": "current" if e == "abc" else "",
#        "@title_page_class3@": "current" if e == "shrec" else "",
#        "@experiment_id@": e,
#        "@experiment_name@": experiment_names[e],
#        "@experiment_descr@": experiment_descriptions[e]
#    }
#    mystring = processWildcards(mystring, rep)
#
def processWildcards(inputstring, wildcards) :
    rep = dict((re.escape(k), v) for k, v in wildcards.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], inputstring)

