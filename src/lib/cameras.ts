import { z } from "zod";

const Vec3 = z.tuple([z.number(), z.number(), z.number()]);
const Quat = z.tuple([z.number(), z.number(), z.number(), z.number()]);

export const CameraSpec = z.object({
  phase: z.number().int().min(1).max(9),
  name: z.string(),
  position: Vec3,
  quaternion: Quat,
  target: Vec3,
  focal_length_mm: z.number().positive(),
  sensor_width_mm: z.number().positive(),
  distance_hint_m: z.number().positive(),
  clip_start: z.number().positive(),
  clip_end: z.number().positive(),
});

export const CamerasDoc = z.object({
  version: z.string(),
  units: z.literal("meters"),
  up_axis: z.enum(["Y", "Z"]),
  handedness: z.enum(["right", "left"]),
  cameras: z.array(CameraSpec).length(9),
});

export type CameraSpec = z.infer<typeof CameraSpec>;
export type CamerasDoc = z.infer<typeof CamerasDoc>;

/** Convert a 36 mm sensor focal length to Three.js FOV (degrees). */
export function focalToFov(focal_mm: number, sensor_mm = 36): number {
  return (2 * Math.atan(sensor_mm / (2 * focal_mm)) * 180) / Math.PI;
}
