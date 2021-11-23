# Website Generator for PCEDNet

Set of scripts and data required to build the website accompanying the paper:

    Chems-Eddine Himeur, Thibault Lejemble, Thomas Pellegrini, Mathias Paulin, Loic Barthe, and Nicolas Mellado. 2021. 
    PCEDNet: A Lightweight Neural Network for Fast and Interactive Edge Detection in 3D Point Clouds. 
    ACM Trans. Graph. 41, 1, Article 10 (February 2022), 21 pages. 
    DOI:https://doi.org/10.1145/3481804

Online version of the website: http://storm-irit.github.io/pcednet-supp/

The website can be deployed in two versions:
 - **local**: generates a self-contained folder with all the assets (including 3d point clouds), that can be browsed 
   without requiring a distant server (just open the file `index.html` and enjoy). We used this version to build the
   supplementary materials submitted with the paper.
 - **server**: generates static server-side html and webgl pages, where point clouds are streamed from the server to the 
   client on request (standard webgl pipeline). This version requires to copy the entire deployment folder to a server 
   and access it remotely.
   
## Usage
### Local deployment
```bash
cd scripts
./deploy.sh local path/to/deployment true #last parameter ask for deleting any content in deployment folder
cd path/to/deployment   # You can now open index.html with your favorite browser
```
Local deployment takes some time as the ply files need to be translated to javascript arrays to allow for local webGL 
visualization (see https://en.wikipedia.org/wiki/Same-origin_policy) **without** having to run a local server (as suggested 
in the [documentation](https://threejs.org/docs/#manual/en/introduction/How-to-run-things-locally)).

### Server deployment
```bash
cd scripts
./deploy.sh server path/to/deployment true #last parameter ask for deleting any content in deployment folder
```
The deployment folder can then be copied to your server and accessed with your favorite browser.
