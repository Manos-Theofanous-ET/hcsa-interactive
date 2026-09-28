# Rev S shell in the site model

`public/3d/HCSA_MAIN.glb` is the Blender export from `blender-automation`, with its
32 shell faces replaced by the Rev S CAD shell (25 Sep 2026 release): edge frames,
ribs and hub, the L1 and L7 panes on each hexagon and the plate on each pentagon.
Everything else (interior, teardown slabs, wireframe, cameras, water loops,
greenhouse, docking collar) is the Blender export as it was.

To rebuild after a new Blender sync or a new Rev S release:

    node scripts/revs-shell/build_site_glb.mjs \
      "<Rev S models>/models/HCSA_shell_RevS/HCSA_shell_RevS.glb" \
      <HCSA_MAIN.glb from blender-automation> \
      public/3d/HCSA_MAIN.glb

The script needs `@gltf-transform/core`, `@gltf-transform/extensions`,
`@gltf-transform/functions`, `meshoptimizer` and `draco3dgltf`. It stops with an
error if the Rev S panel centres do not land on the site's face centres, or if the
matching is not one to one. Bolts, nuts, washers, O-rings and beads are left out
(too small to see at site scale), and the frames are simplified to about 250
triangles each.

Running `pnpm sync:geometry` on its own brings back the old faces; run this
script after it.
