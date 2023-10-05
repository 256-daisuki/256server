import "./App.css";
import * as THREE from "three";
import { useEffect } from "react";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

function App() {
  let canvas: HTMLCanvasElement;
  let model: THREE.Group;
  let isDragging = false;
  let previousMousePosition = {
    x: 0,
    y: 0,
  };

  useEffect(() => {
    canvas = document.getElementById("canvas") as HTMLCanvasElement;

    const sizes = {
      width: innerWidth,
      height: innerHeight,
    };
    // scene
    const scene: THREE.Scene = new THREE.Scene();

    // camera
    const camera: THREE.PerspectiveCamera = new THREE.PerspectiveCamera(
      75,
      sizes.width / sizes.height,
      0.1,
      1000
    );
    camera.position.set(0, 0.38, 1.2);

    // renderer
    const renderer: THREE.WebGLRenderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
    });
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(window.devicePixelRatio);

    // 3dモデルインポート
    const gltfLoader = new GLTFLoader();

    gltfLoader.load("./models/scene.gltf", (gltf) => {
      model = gltf.scene;
      model.scale.set(0.7, 0.7, 0.7);
      model.rotation.y = -Math.PI / 15;

      scene.add(model);
    });

    // マウスの座標を保持する変数
    const mouse = new THREE.Vector2();

    // マウスのドラッグ開始
    canvas.addEventListener("mousedown", (event) => {
      isDragging = true;
      previousMousePosition.x = event.clientX;
      previousMousePosition.y = event.clientY;
    });

    // マウスの移動に応じてモデルを回転させる
    canvas.addEventListener("mousemove", (event) => {
      // ドラッグ中のみ回転
      if (isDragging) {
        const deltaX = event.clientX - previousMousePosition.x;
        const deltaY = event.clientY - previousMousePosition.y;

        // マウスの移動に応じてモデルを回転
        model.rotation.x += deltaY * 0.01;
        model.rotation.y += deltaX * 0.01;
      }

      previousMousePosition.x = event.clientX;
      previousMousePosition.y = event.clientY;
    });

    // マウスのドラッグ終了
    canvas.addEventListener("mouseup", () => {
      isDragging = false;
    });

    // マウスのホイールイベント
    canvas.addEventListener("wheel", (event) => {
      const zoomSpeed = 0.005;
      const zoom = 1 + event.deltaY * zoomSpeed;

      // マウスの位置を中心に拡大縮小
      const mouse = new THREE.Vector2(
        (event.clientX / sizes.width) * 2 - 1,
        -(event.clientY / sizes.height) * 2 + 1
      );

      const screenPosition = new THREE.Vector3(mouse.x, mouse.y, 0.5);
      screenPosition.unproject(camera);

      const direction = screenPosition.sub(camera.position).normalize();
      camera.position.add(direction.multiplyScalar(zoom - 1));
    });

    // マウスの移動に応じてモデルを回転させる
    canvas.addEventListener("mousemove", (event) => {
      // マウス座標を正規化
      mouse.x = (event.clientX / sizes.width) * 2 - 1;
      mouse.y = -((event.clientY / sizes.height) * 2 - 1);

      // ドラッグ中のみ回転
      if (isDragging) {
        const deltaX = event.clientX - previousMousePosition.x;
        const deltaY = event.clientY - previousMousePosition.y;

        // マウスの移動に応じてモデルを回転
        model.rotation.x += deltaY * 0.01;
        model.rotation.y += deltaX * 0.01;
      }

      previousMousePosition.x = event.clientX;
      previousMousePosition.y = event.clientY;
    });

    // マウスのホイールイベント
    canvas.addEventListener("wheel", (event) => {
      const zoomSpeed = 0.0005;
      const zoom = 1 + event.deltaY * zoomSpeed;

      // マウスの位置を中心に拡大縮小
      camera.position.x *= zoom;
      camera.position.y *= zoom;
      camera.position.z *= zoom;

      event.preventDefault(); // デフォルトのスクロールを防止
    });

    // アニメーション
    function tick() {
      renderer.render(scene, camera);
      requestAnimationFrame(tick);
    }
    tick();
  }, []);

  return (
    <>
      <canvas id="canvas"></canvas>
      <div className="mainContent">
        <h3>hello world</h3>
      </div>
    </>
  );
}

export default App;
