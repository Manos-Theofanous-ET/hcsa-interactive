# HCSA Rev F parts library additions, 8 Nov 2026 (PROPOSAL)

Built with CadQuery 2.8 by `build_parts_revF.py` (conventions of `parts_lib.py`: mm; z 0 outer face of the rib/frame grid, z 180 pane seat plane, z 400 cabin face of the main rib and corner block). Everything here is a proposal for the 13 November review with Marco Cross and Prof. Fleeter, not a decision. Outputs: `step/`, `stl/`, `svg/` (front, top, side, iso), `glb/`, `parts.json` (masses from model volume x nominal density), `checks.json` (bounding boxes, hole volumes, clearances, dihedrals), `montage_parts_revF.png`.

## Parts

| id | name | material | mass kg | bbox mm | status |
|---|---|---|---|---|---|
| CB-01 | Corner block, hexagon corner (120 deg), 2219-T852, R10 inside corners | 2219-T852 | 21.514 | 344.0 x 223.2 x 400.0 | 8 Nov 2026 PROPOSAL |
| CB-02 | Corner block, pentagon corner (108 deg) | 2219-T852 | 20.694 | 300.5 x 233.6 x 400.0 | 8 Nov 2026 PROPOSAL |
| HP-01 | Hardpoint block in the frame, 50 thick, as drawn (pins at z 140) | 6061-T6 | 6.408 | 50.0 x 360.0 x 180.0 | 8 Nov 2026 PROPOSAL |
| HP-01M | Hardpoint block, moved fitting (pins at z 76) | 6061-T6 | 6.408 | 50.0 x 360.0 x 180.0 | 8 Nov 2026 PROPOSAL |
| HP-02 | Hardpoint fitting half, Ti-6Al-4V (TP3), as drawn | Ti-6Al-4V | 1.031 | 30.0 x 200.0 x 60.0 | 8 Nov 2026 PROPOSAL |
| HP-03 | Hardpoint pin, 40 mm, 160 long, A286, dry-film lubricated | A286 | 1.595 | 160.0 x 40.0 x 40.0 | 8 Nov 2026 PROPOSAL |
| P-11 | Main rib lateral brace at a node, 7075-T7351 (pair) | 7075-T7351 | 1.116 | 152.0 x 90.0 x 195.0 | 8 Nov 2026 PROPOSAL |
| P-07 | Pressure pane L7, 531 mm, 21 mm BOROFLOAT 33 | BOROFLOAT 33 | 5.498 | 407.9 x 470.0 x 21.0 | DECIDED 5 Nov 2026 (21 mm), regenerated 8 Nov |
| PL-01 | Pentagon closure plate, one of five triangles, 10 mm 6061-T6 | 6061-T6 | 44.926 | 1713.6 x 2057.4 x 10.0 | 8 Nov 2026 PROPOSAL |
| A-03 | Corner node assembly: two hexagon blocks and one pentagon block at a vertex, with 12 ties and 6 dowels | 2219-T852 + Inconel 718 + A286 | 76.630 | 445.71 x 453.55 x 433.77 | 8 Nov 2026 PROPOSAL |
| A-04 | Pentagon panel assembly, schematic: five frames, five main ribs, hub, 90 secondary ribs, five corner blocks, closure plate | 6061-T6 + 2219-T852 | 921.900 | 3639.34 x 3461.25 x 400.15 | 8 Nov 2026 PROPOSAL |

Masses of the assemblies: A-03 blocks_kg 63.72, ties_kg 11.41, dowels_kg 1.5; A-04 frames 110.8, main_ribs 238.4, hub 50.8, secondary 193.8, blocks 103.5, closure 224.6 (kg).

## Clashes and departures from the brief (for the review)

1. **CB-01 / CB-02 tie columns.** The brief put the two tie columns 56 mm apart centred on the 230 mm leg (87 and 143 mm from the vertex). The main rib landing (110 wide pocket along the bisector) reaches 92.4 mm (hexagon) and 104.3 mm (pentagon) along the legs' inner faces, so a 23.5 mm hole at 87 mm breaks into the pocket. The columns are drawn at 136 and 192 mm (pitch 56 kept), the nearest position where a 45 mm washer clears the landing on both blocks. The C1 model has them elsewhere and should be rerun.
2. **CB-01 / CB-02 landing depth.** '30 mm into the block' from the re-entrant corner (57.7 mm from the vertex on the hexagon, 61.8 on the pentagon) cannot be cut: 30 mm nearer the vertex the block is only 96 mm (hex) / 88 mm (pent) wide, so a 110 pocket there breaks through the joint faces. The pocket bottom is at 55 mm (hex) / 60 mm (pent) from the vertex, the deepest position that keeps a continuous 110 mm bearing face; the walls are then 34.5 / 41.8 mm long and 20.1 / 16.2 mm of metal remain between the pocket corner and the joint face (thin: for Marco). The R12 at the re-entrant corner is consumed by the landing.
3. **CB-02 rows.** Tie rows at z 128.3 and 364.4 as briefed; the dowel is at z 246.3, not 240, so it meets the hexagon's z 240 dowel on the joint plane (same 256.9 mm along the leaning face).
4. **HP-01M (moved fitting, pins at z 76).** The 40 mm bore (z 56-96) does NOT overlap the seam bolt row at z 58: the nearest bolt hole (y +-88.75) is 9.7 mm of metal from the bore, and the bore is 20.5 mm above the inner gland (z 28.5-35.5). The clash is elsewhere: the moved fitting pad (200 x 60 at z 46-106, y +-100) covers the two plain bolts at y +-88.75, z 58, so their nuts sit under the fitting and the fitting's end fixing holes land on them. The two plain bolts are therefore moved to z 118 in this variant (hole edge 7.75 mm above the pad, a 16 mm washer 4.0 mm); at the brief's z 110 the hole edge would touch the pad (-0.25 mm) and the washer overlap it by 4 mm. Caution: D1 showed the seal gap grows when the bolt row moves away from the seals (z 70 failed), so a deeper plain bolt is the wrong direction for the seal; the alternatives are the plain bolts moved along the seam into the 20 mm web beside the block (y +-137.5, where the HP1M run had them) or a shorter fitting. To decide on 13 Nov.
5. **HP-01 (as drawn).** Pad at z 110-170 touches the underside of the frame seat lip (z 170); bore to lip underside 10.0 mm. Fails the HP1 seal check (hinge), kept for comparison.
6. **HP-02 fixing holes.** Two rows of three 10 mm holes cannot clear three 40 mm bores on a 60 mm deep plate; drawn as two pairs at the ends and one hole between each pair of bores (5.8 mm wall to the bore in the block). The fitting bolts are in tension under the seam pull; size to check.
7. **P-11 brace.** A flat 8 mm plate on the web cannot reach z 375 because the cap angle P-04A has a 12 mm vertical leg down the web from z 300 to 375; the plate is stepped out 12 mm at z 280-300 and runs up the outside of the angle's leg. Size is a proposal needing its own check.
8. **PL-01 closure.** The brief's 100 mm cut-back from the rib centre lines and the frame leaves the plate seated on nothing (the ledge is 4-34 mm off the centre line, the lip 50 mm wide); drawn 10 mm back like the panes, plus the apex cut r 100 about the hub and the corner cuts to the CB-02 outline. Side of the ribs is open (Q57); drawn cabin side at z 180-190. Clash at the apex: the hub fork cheeks (4.1-14.1 mm off the rib centre line, out to r 210) cross the plate's edge line between r 100 and 210; a 15 mm cut-back there or notched cheeks, open.
9. **A-03 corner node.** On the real polyhedron (edge 2,250 mm, 11,151.1 mm across) the dihedrals measured at the chosen vertex are pent-hex 142.623; pent-hex 142.623; hex-hex 138.19 deg (138.19 and 142.62 expected). Because the blocks are drawn straight, the two joint faces at each edge are 37.377, 37.377, 41.81 deg apart instead of coplanar on the radial plane; the straight blocks overlap in a prism about 75 mm on a side along each outer edge and the facing tie holes do not line up. The next step is the leaning joint face (20.905 / 16.472 deg) with the tie holes normal to it, as in C1.
10. **A-04 pentagon.** Schematic: straight frames 1,790 mm between the block ends, five ribs from r 215 to the landings (1,639 mm), 90 plain secondary segments (node cores and star plates not drawn), five CB-02, five PL-01.

## Fillets and chamfers

All blends succeeded.

## Checks

Every part's bounding box is in `checks.json` next to the intended envelope; hole counts were checked by volume before and after the cuts (tie and dowel holes on CB-01/02, pin bores on HP-01/HP-02, brace holes on P-11), all equal to the expected cylinder volumes.
