import type { Object3D, Mesh, MeshStandardMaterial, Quaternion } from "three";
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
  /** Collected interior meshes (ramps, pods, aerogarden, figures) — faded in on
   *  Phase 4. We keep the list so each mesh's material can receive an alpha
   *  tween without needing a synthetic parent group. */
  interiorMeshes: InteriorMeshEntry[];
  /** Plant-tray emissive materials driven by `led_green` (Phase 6 greenhouse). */
  plantLedMaterials: MeshStandardMaterial[];
  /** PENT_02 hinge choreography (Phase 6). Captured at init: the meshes to
   *  rotate, the pivot point in world space, and the axis direction. */
  pent02Hinge: Pent02Hinge | null;
  /** BEAM_TRUNK systems-core node (Phase 7 longitudinal scale). */
  beamTrunk: BeamTrunkEntry | null;
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

export type InteriorMeshEntry = {
  mesh: Mesh;
  material: MeshStandardMaterial;
  /** Authored alpha; phase opacity fades multiplicatively against this. */
  baseOpacity: number;
};

export type Pent02Hinge = {
  /** Meshes belonging to PENT_02 that should rotate together. */
  meshes: Object3D[];
  /** Each mesh's pre-hinge initial pose (captured at init). */
  initialPoses: Array<{ position: Vector3; quaternion: Quaternion }>;
  /** Hinge pivot point in world space (from PENT_02_HINGE_PIVOT empty). */
  pivotWorld: Vector3;
  /** Hinge axis direction in world space (PENT_02_HINGE_PIVOT local +X). */
  axisWorld: Vector3;
};

export type BeamTrunkEntry = {
  node: Object3D;
  /** Initial scale captured at init (identity 1,1,1 unless Blender set otherwise). */
  initialScale: Vector3;
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
    interiorMeshes: [],
    plantLedMaterials: [],
    pent02Hinge: null,
    beamTrunk: null,
    wireframeMesh: null,
    teardownLayers: [],
  };
}
