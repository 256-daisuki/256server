import "./App.css";
import * as THREE from "three";
import { useEffect } from "react";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

function App() {
  let canvas: HTMLCanvasElement;
  let model: THREE.Group;

  useEffect(() => {
    canvas = document.getElementById("canvas") as HTMLCanvasElement;

    const sizes = {
      width: innerWidth,
      height: innerHeight,
    }
    //scene
    const scene: THREE.Scene = new THREE.Scene();

    //camera
    const camera: THREE.PerspectiveCamera = new THREE.PerspectiveCamera(
      75, 
      sizes.width / sizes.height,
      0.1,
      1000
      );
      camera.position.set(0, 0.2, 2);

    //renderer
    const renderer: THREE.WebGLRenderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true, //透明度を取る
    });
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(window.devicePixelRatio);

    // const geometry = new THREE.BoxGeometry( 1, 1, 1 ); 
    // const material = new THREE.MeshBasicMaterial( {color: 0x00ff00} ); 
    // const cube = new THREE.Mesh( geometry, material ); 
    // scene.add( cube );

    //3dモデルインポート
    const gltfLoader = new GLTFLoader();

    gltfLoader.load("./models/scene.gltf", (gltf) => {
      model = gltf.scene;
      model.scale.set(0.7, 0.7, 0.7)
      model.rotation.y = -Math.PI / 8;

      scene.add(model);
    });

    //アニメーション
    function tick() {
      renderer.render(scene, camera);
      requestAnimationFrame(tick);
    }
    tick();
  },[]);

  return (
    <>
      <canvas id="canvas"></canvas>
      <div className='mainContent'>
        <h3>hello world</h3>
      </div>
    </>
  )
}

export default App;
