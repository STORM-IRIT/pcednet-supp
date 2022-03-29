function displayModel( scene, camera, control, geometry, material, resetControl )
{
    // clear memory
    if (resetControl)
        control.reset();
    scene.children.splice(0, scene.children.length);

    // generate new model
    const points = new THREE.Points( geometry, material );

    // center 3d model on origin
    geometry.computeBoundingBox();

    const sphere = new THREE.Sphere();
    geometry.boundingBox.getBoundingSphere( sphere );

    // scale to unit box
    s = 1.0 / sphere.radius;
    geometry.scale(s,s,s);

    // center object to origin
    const center = geometry.boundingBox.getCenter();
    points.position.x = -center.x;
    points.position.y = -center.y;
    points.position.z = -center.z;

    // Move back camera
    if (resetControl)
        camera.position.set( 0, 4, 0);

    scene.add( points );
}


function generateViewer( divname ){

    var container,camera, scene, renderer, controls;

    init();
    animate();
    function init() {

        container = document.getElementById( divname );

        const width = container.clientWidth;
        const height = container.clientHeight;

        camera = new THREE.PerspectiveCamera( 35, width/height, 0.1, 50 );
        camera.lookAt( new THREE.Vector3(0,0,0) );

        scene = new THREE.Scene();
        scene.background = new THREE.Color( 0xffffff );

        // renderer

        renderer = new THREE.WebGLRenderer( { antialias: true } );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.outputEncoding = THREE.sRGBEncoding;
        renderer.setSize( width, height );

        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.update();

        container.appendChild( renderer.domElement );
    }

    function animate() {
        requestAnimationFrame( animate );
        controls.update();
        render();

    }

    function render() { renderer.render(scene, camera); }

    return [scene, camera, controls];
} //function generateViewer

