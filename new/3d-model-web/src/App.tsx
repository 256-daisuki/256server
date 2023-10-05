import { useEffect } from "react";
import "./App.css";
import * as THREE from "three";

function App() {

  useEffect(() => {
    //scene
    const scene: THREE.Scene = new THREE.Scene();

    //camera
    const camera: THREE.PerspectiveCamera = new THREE.PerspectiveCamera();

    //renderer
  },[]);

  return (
    <>
      <canvas id="canvas"></canvas>
      <div className='mainContent'></div>
    </>
  )
}

export default App;
