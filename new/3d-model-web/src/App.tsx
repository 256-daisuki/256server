import "./App.css";
import * as THREE from "three";
import { useEffect } from "react";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"; // 追加

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
      camera.position.set(0, 0, 2);

    //renderer
    const renderer: THREE.WebGLRenderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
    });
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(window.devicePixelRatio);

    // const geometry = new THREE.BoxGeometry( 1, 1, 1 ); 
    // const material = new THREE.MeshBasicMaterial( {color: 0x00ff00} ); 
    // const cube = new THREE.Mesh( geometry, material ); 
    // scene.add( cube );

    //3dモデルインポート
    const gltfLoader = new GLTFLoader();

    gltfLoader.load("./test/miku4.gltf", (gltf) => {
      model = gltf.scene;
      model.scale.set(0.7, 0.7, 0.7)
      model.rotation.y = -Math.PI / 8;
    
      // 3Dモデルの中心を調整
      const box = new THREE.Box3().setFromObject(model);
      const center = box.getCenter(new THREE.Vector3());
      model.position.sub(center); // 中心を原点に移動
    
      scene.add(model);
    });
    

    // Add controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // ドリフトを減衰させる
    controls.dampingFactor = 0.25; // ドリフトの割合
    
    //アニメーション
    function tick() {
      controls.update(); // マウスコントロールの更新
      renderer.render(scene, camera);
      requestAnimationFrame(tick);
    }
    tick();
  },[]);

  return (
    <>
      <canvas id="canvas"></canvas>
      <div className='mainContent'>
        
      </div>
    </>
  )
}

export default App;
