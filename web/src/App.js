import Model from './models/globe';
import { OrbitControls } from '@react-three/drei'
import { Canvas, useThree } from '@react-three/fiber'

export default function App() {
    return (
        <Canvas>
            <ambientLight intensity={Math.PI / 2} />
            <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
            <pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />

            <mesh>
                <Model />
            </mesh>

            <OrbitControls enableZoom={true} /> {/* Updated to directly use Vector3 */}
        </Canvas>
    );
}
