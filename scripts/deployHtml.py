import sys, glob
from os import listdir, remove
from os.path import dirname, join, isfile, abspath
from io import StringIO

import numpy as np
import utilsmodule as um
import releasesmodule as releases

script_path    = dirname(abspath(__file__))
datasetPath    = join(script_path,"data/")
deploymentPath = sys.argv[1]
imagesRelPath  = "images/"
imagesPath     = join(deploymentPath,imagesRelPath)
# should be either 'local' or 'server'
deploymentMode = sys.argv[2]


experiments = [f for f in listdir(datasetPath) if dirname(join(datasetPath, f)) and not f.startswith('.')]

image_html_template="""
                      <h3 style="text-align:center;">{F_spaces}</h3>
                      <div class="row">
                      <section class="col-6 col-12-narrower"><p style="text-align:left;">Left image: <select id="dropdown-{F}_left" onchange="updateFigure('{F}_left')">{optsleft}</select></p></section>
                      <section class="col-6 col-12-narrower"><p style="text-align:right;">Right image: <select id="dropdown-{F}_right" onchange="updateFigure('{F}_right')">{optsright}</select></p></section>
                    </div>
                    <div class="row">
                      <section class="col-12 col-12-narrower"><div class="ba-slider"><img id="{F}_right" src="{second}"><div class=" resize"><img id="{F}_left" src="{first}"></div><span class="handle"></span></div></section>
                    </div>
"""
threejs_wrappers = {
    'local':
        """function displayModelWrapper( scene, camera, control, methodname, modelname, resetControl ){

  let buffers   = threeModels[methodname][modelname];
  let gtbuffers = threeModels["Ground Truth"][modelname];
  let material  = new THREE.ShaderMaterial( {

    vertexShader: "attribute float label; varying vec3 vcolor; varying vec3 vnormal; void main() { vec4 mvPosition = modelViewMatrix * vec4( position, 1.0 ); gl_PointSize = ( 15.0 / - mvPosition.z ); gl_Position = projectionMatrix * mvPosition; vec3 color = label==0. ? vec3(180, 180, 180) : (label==2. ? vec3(255, 0, 0) : vec3(255,255,0) );vcolor = color / 255.;  vnormal =  normal; } ",
    fragmentShader: "varying vec3 vcolor; varying vec3 vnormal; void main() { vec3 ldir = vec3(1.,1.,1.); if ( length( gl_PointCoord - vec2( 0.5, 0.5 ) ) > 0.475 ) discard; gl_FragColor = vec4( vcolor, 1.0 ) * (0.5 + 0.7*pow(abs(dot(vnormal,normalize(ldir))),0.5)); }",
  } );


  let geometry = new THREE.BufferGeometry();
  geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( gtbuffers['vertices'], 3 ) );
  geometry.setAttribute( 'normal', new THREE.Float32BufferAttribute( gtbuffers['normals'], 3 ) );
  geometry.setAttribute( 'label', new THREE.Float32BufferAttribute( buffers['label'], 1 ) );


  displayModel(threeScene1, threeCamera1, controls1, geometry, material, resetControl);
}
""",
    'server':
        """
const method_id={
@experiment_list_js@
};

function displayModelWrapper( scene, camera, control, methodname, modelname, resetControl ){
  let plyfile = '3dmodels/@experiment_id@/'+method_id[methodname]+'/'+threeModels[methodname][modelname]["plyfile"];
  
  const loader = new THREE.PLYLoader();
    loader.load( plyfile, function ( geometry ) {
    // let material = new THREE.PointsMaterial( { size: 0.1, vertexColors: THREE.VertexColors } );
    let material  = new THREE.ShaderMaterial( {
      vertexColors: true,
      vertexShader: "varying vec3 vcolor; varying vec3 vnormal; void main() { vec4 mvPosition = modelViewMatrix * vec4( position, 1.0 ); gl_PointSize = ( 15.0 / - mvPosition.z ); gl_Position = projectionMatrix * mvPosition; vcolor = color==vec3(1.)?vec3(0.705):color;  vnormal =  normal; } ",
      fragmentShader: "varying vec3 vcolor; varying vec3 vnormal; void main() { vec3 ldir = vec3(1.,1.,1.); if ( length( gl_PointCoord - vec2( 0.5, 0.5 ) ) > 0.475 ) discard; gl_FragColor = vec4( vcolor, 1.0 ) * (0.5 + 0.7*pow(abs(dot(vnormal,normalize(ldir))),0.5)); }",
    } );
    displayModel(threeScene1, threeCamera1, controls1, geometry, material, resetControl);
  });
}
""",
}


repgeneral = {
    "@paper_title@": "A Light-Weight Neural Network for Fast and Interactive Edge Detection in 3D Point Clouds",
    "@classifier_class_color_flat@": 'rgb(' + um.classifier_class_color['flat'] + ')',
    "@classifier_class_color_sharp@": 'rgb(' + um.classifier_class_color['sharp'] + ')',
    "@classifier_class_color_smooth@": 'rgb(' + um.classifier_class_color['smooth'] + ')',
    "@method_list@": "\n".join(['<li><strong>{short}</strong>: {descr}</li>'.format(short=i,descr=um.methods_descr[k]) for k,i in um.methods_descr_short.items()]),
    "@experiment_list@": "\n".join(['<li><strong>{short}</strong>: {descr}</li>'.format(short=k.upper(),descr=i) for k,i in um.experiment_names.items()]),
    "@experiment_list_js@": "\n".join(['   "{key}": "{value}",'.format(key=i,value=k) for k,i in um.methods_descr.items()]),
}




### Process index
pagetemplates = ["index", "software"]
for templateName in pagetemplates:
    templateFilename = templateName + "_template.html"
    with open(templateFilename, 'r') as myfile:
        print ("Preparing page " + templateName)
        webcontent = myfile.read()
        webcontent = um.processWildcards( webcontent, repgeneral )

        if templateName == "index":
            # Generate image list
            image_list=""
            figures = [f for f in listdir(imagesPath) if dirname(join(imagesPath, f))]

            figures.sort()

            for f in figures:
                pngfiles = glob.glob(join(imagesPath,f)+'/*.png')
                jpgfiles = glob.glob(join(imagesPath,f)+'/*.jpg')

                figurefiles = pngfiles + jpgfiles

                if figurefiles:

                    print ("Processing " + f)
                    first_option_list = ""
                    second_option_list = ""

                    firstselectid  = 0
                    secondselectid = (0,1)[len(figurefiles)>1];

                    for count, p in enumerate(figurefiles):
                        htmlpngpath = p.replace(deploymentPath+("/"),"")
                        method = htmlpngpath.split('/')[-1:][0][:-4]
                        if method in um.methods_descr.keys():
                            methodname = um.methods_descr[method]
                        else:
                            methodname = method.replace('_', ' ')
                            print("Warning unknown method {m}, using name={name}".format(m=method, name=methodname))
                        first_option_list = first_option_list + '<option value="{path}" {selected}>{name}</option>' \
                            .format(name=methodname, path=htmlpngpath,selected=("", "selected")[count == firstselectid])
                        second_option_list = second_option_list + '<option value="{path}" {selected}>{name}</option>' \
                            .format(name=methodname, path=htmlpngpath,selected=("", "selected")[count == secondselectid])

                    first = figurefiles[firstselectid].replace(deploymentPath+("/"),"")
                    second = figurefiles[secondselectid].replace(deploymentPath+("/"),"")
                    image_list = image_list +image_html_template.format(optsleft=first_option_list,
                                                                        optsright=second_option_list,
                                                                        F=f,
                                                                        F_spaces=f.replace('_',' '),
                                                                        first=first,
                                                                        second=second);
            webcontent = um.processWildcards( webcontent, {"@image_list@":image_list} )

        elif templateName == "software":
            webcontent = um.processWildcards( webcontent,{"@release_list@":releases.build_release_list()})

        with open( join(deploymentPath,templateName+'.html'), 'wt') as myfile:
            myfile.write(webcontent)

for eid, e in enumerate(experiments):
    if um.experiment_skip[e]: continue

    print ("  Processing experiment " + e)

################################################################################################
    # Generate html file
    html_template_filename = join(script_path,"dataset_template.html")
    html_output_filename = join(deploymentPath,e +".html")
    with open(html_template_filename, 'r') as myfile:
        webcontent = myfile.read()

        # Replace wildcards.
        # Source: https://stackoverflow.com/a/6117124
        rep = {
            "@title_page_class1@": "current" if e == "default" else "",
            "@title_page_class2@": "current" if e == "abc" else "",
            "@title_page_class3@": "current" if e == "abc_noise_0.04" else "",
            "@title_page_class4@": "current" if e == "shrec" else "",
            "@title_page_class5@": "current" if e == "shrec2" else "",
            "@experiment_id@": e,
            "@experiment_id3d@": "shrec" if e == "shrec2" else e,
            "@experiment_name@": um.experiment_names[e],
            "@experiment_descr@": um.experiment_descriptions[e],
        }

        threejs_methodwrapper = um.processWildcards( threejs_wrappers[deploymentMode], repgeneral);
        threejs_methodwrapper = um.processWildcards( threejs_methodwrapper, rep);
        rep["@threejs_displayModelWrapper@"] = threejs_methodwrapper;

        webcontent = um.processWildcards( webcontent, rep )
        webcontent = um.processWildcards( webcontent, repgeneral )

        # write output file
        with open(html_output_filename, 'wt') as myfile:
            myfile.write(webcontent)
