import type { Object3D, Mesh, MeshStandardMaterial, Group } from "three";
import { Vector3 } from "three";

/** Shared refs populated once on GLB mount, consumed by the phase timeline. */
export type SceneRegistry = {
  /** The root group of the loaded GLTF scene. */
  root: Object3D | null;
  /** Per-face metadata: the mesh group to translate + its outward normal. */
  hexFaces: FaceEntry[];
  pentFaces: FaceEntry[];
  /** Shared materials (dedup'd in the GLB). Opacity tweens hit these once. */
  materials: {
    hexFrame: MeshStandardMaterial | null;
    hexGlass: MeshStandardMaterial | null;
    hexSolar: MeshStandardMaterial | null;
    pentFrame: MeshStandardMaterial | null;
    pentGlass: MeshStandardMaterial | null;
    wireframe: MeshStandardMaterial | null;
    waterRed: MeshStandardMaterial | null;
    waterBlue: MeshStandardMaterial | null;
  };
  /** Interior geometry we fade in on Phase 4. Collected into a synthetic group. */
  interiorGroup: Group | null;
  /** Wireframe mesh (cyan edges). Hidden by default until Phase 2. */
  wireframeMesh: Mesh | null;
  /** Phase 5 teardown slabs (PANEL_TEARDOWN_L1..L7), ordered vacuum→interior. */
  teardownLayers: TeardownLayer[];
};

export type FaceEntry = {
  /** The node holding HEX_NN_Frame / HEX_NN_Glass / HEX_NN_Solar meshes
   *  (or PENT_NN_Frame / PENT_NN_Glass). We translate this node as a group. */
  node: Object3D;
  /** Unit vector pointing outward from world origin to the face. */
  faceNormal: Vector3;
  /** The node's initial position (pre-translation). */
  initialPosition: Vector3;
};

export type TeardownLayer = {
  node: Object3D;
  material: MeshStandardMaterial;
  /** 1-indexed layer order (vacuum side → crew side), from Blender custom prop. */
  index: number;
  /** Authored alpha baked in Blender; we fade multiplicatively against this
   *  so transmission-heavy layers keep their intended translucency. */
  baseOpacity: number;
};

export function emptyRegistry(): SceneRegistry {
  return {
    root: null,
    hexFaces: [],
    pentFaces: [],
    materials: {
      hexFrame: null,
      hexGlass: null,
      hexSolar: null,
      pentFrame: null,
      pentGlass: null,
      wireframe: null,
      waterRed: null,
      waterBlue: null,
    },
    interiorGroup: null,
    wireframeMesh: null,
    teardownLayers: [],
  };
}
