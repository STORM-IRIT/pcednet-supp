# Website Generator for PCEDNet

Set of scripts and data required to build the website accompanying the paper:

    Chems-Eddine Himeur, Thibault Lejemble, Thomas Pellegrini, Mathias Paulin, Loic Barthe, and Nicolas Mellado. 2021. 
    PCEDNet: A Lightweight Neural Network for Fast and Interactive Edge Detection in 3D Point Clouds. 
    ACM Trans. Graph. 41, 1, Article 10 (February 2022), 21 pages. 
    DOI:https://doi.org/10.1145/3481804

The website can be generated in two version: 
 - **local**: generate a self-contained folder with all the assets (including 3d point clouds), that can be browsed 
   without requiring a distant server (just open the file `index.html` and enjoy).
 - **server**: generate server-side html and webgl pages, where point clouds are streamed from the server to the client
on request (normal standard webgl pipeline). This version requires to copy the whole deployment folder to a server and
access it remotely.
   
## Usage
### Local deployment
```bash
cd scripts
./deploy.sh local path/to/deployment true #last parameter ask for deleting any content in deployment folder
cd path/to/deployment   # You can now open index.html with your favorite browser
```
Local deployment takes some time as the ply files need to be translated to javascript arrays to allow for local webGL 
visualization.

### Server deployment
```bash
cd scripts
./deploy.sh server path/to/deployment true #last parameter ask for deleting any content in deployment folder
```
The deployment folder can then be copied to your server and accessed by any browser.