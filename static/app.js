const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);
camera.position.z = 3;

// Hologram sphere
const geometry = new THREE.SphereGeometry(1, 32, 32);
const material = new THREE.MeshStandardMaterial({
  color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.6
});
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Lighting
scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const light = new THREE.PointLight(0x00ffcc, 2, 10);
light.position.set(3, 3, 3);
scene.add(light);

const subtitle = document.getElementById("subtitle");
let isSpeaking = false;

// Poll Flask for status every 500ms
setInterval(async () => {
  try {
    const res = await fetch("/status");
    const data = await res.json();
    subtitle.textContent = data.text || 'Listening...';
    isSpeaking = data.speaking;

    // Change color by emotion
    const colors = {
      happy: 0xffdd00, sad: 0x4488ff,
      angry: 0xff4422, curious: 0xaa44ff, neutral: 0x00ffcc
    };
    material.color.setHex(colors[data.emotion] || 0x00ffcc);
  } catch (e) {}
}, 500);

function animate() {
  requestAnimationFrame(animate);
  sphere.rotation.y += isSpeaking ? 0.03 : 0.005;
  sphere.rotation.x += 0.002;
  renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});