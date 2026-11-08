# 2. The flight parts, drawn and in 3D

Nine A3 sheets follow this page. They are drawn from the Rev F parameter file, not traced from CAD, and nobody has checked them for machining yet; that is what Friday is for. The same parts are in the parts library on the website, each with a STEP file, a GLB for the browser and four drawing views, and the whole facility is in the master model.

## The sheets

| Sheet | What it shows | Status |
| --- | --- | --- |
| RF-01 | The main rib, option B, and the secondary rib, cut through, with the 21 mm panes seated and the glass bite on each. The two new requirements are in the notes: the nodes must hold the main rib sideways, and the panes need an answer for launch | Ribs DECIDED; brace PROPOSAL; pane at launch OPEN |
| RF-02 | A seam cut through at a plain bolt: the 180 mm frame, the two glands, the RTV bead, the bolt at 4 kN, and the study of the seal loop corners against Parker's R16 minimum | Frame, gland, bolt DECIDED; loop corners OPEN |
| RF-03 | The T1 seam slices and the 550 mm article at 180 mm deep. Superseded in detail by the TP sheets in part 3, kept for the record | For reference |
| RF-04 | The transfer lock between the 0.8 atm module and a 1 atm host, as a concept: the hatch that stays shut while the pressures differ, the equalising valves and our relief valve | Concept, not sized |
| RF-05 | A hexagon-to-hexagon seam cut at the first bolt, 271 mm from the corner, with every feature on the joint face by z', both hardpoint positions as envelopes, and the table that turns z' into panel depth for the hexagon and the pentagon mitres | Seam DECIDED; hardpoint position OPEN; outer glass layers OPEN |
| RF-06 | The hexagon panel from the cabin side: 6 main ribs, 108 secondary rib segments, 96 panes, 18 six-way nodes, 18 hardpoints, the 16 bolts on one edge, and the parts list with masses | Layout DECIDED |
| RF-07 | The hardpoint at both positions, as drawn and moved onto the line of the pull, with what the HP1 model found and the clash of the moved fitting with the bolt row | PROPOSAL; position decided Tuesday |
| RF-08 | The corner node in plan and on the joint face, the C1 results, Marco's machining points (inside radii, a landing for the main rib, the material), and the P-11 brace | Block PROPOSAL; ties DECIDED |
| RF-09 | The pentagon panel from the cabin side, with its roles, the closure plate as five triangles, and the solar stand-off | Ribs and frame DECIDED; closure side OPEN (Q57) |

## The parts library

Every part below is at hcsa-site.vercel.app/parts, with STEP, GLB and four views. Masses are from the solids; the frame and ribs are 2219 for flight and 6061 for the test pieces.

| Part | What it is | Each | Per hexagon | Per pentagon |
| --- | --- | --- | --- | --- |
| P-06 | Edge frame member, 180 deep, 2,250 long, with the glands, bolt holes and seat lip | 27.9 kg | 6 | 5 |
| P-04 | Main rib, option B, I 400 x 100 x 25, web 8 | 33.2 kg | 6 | 5 |
| P-04A | Main rib cap angle, one of the two that make the inner flange | 12.8 kg | 12 | 10 |
| P-05 | Hub core, 160 mm, with six forks for the main rib webs; the pentagon needs a five-fork version, not drawn | 28.3 kg | 1 | 1, five forks |
| P-05A | Hub star plate, 25 mm | 14.2 kg | 2 | 2 |
| P-01 | Secondary rib segment, I 180 x 60 x 10, web 5, 562.5 pitch | 2.5 kg | 108 | 90 |
| P-02 | Node star plate | 1.8 kg | 36 | 30 |
| P-03 | Node web core | 4.4 kg | 18 | 15 |
| P-07 | Pressure pane, 21 mm BOROFLOAT 33, 531 mm | 5.5 kg | 96 | none |
| P-08 | Pane corner clamp | 0.2 kg | 18 | none |
| P-09 | One seam bolt station, as an assembly | | 16 per seam | 16 per seam |
| P-14 | Seam bolt NAS6705U27 with KFN670 nut | 0.03 kg | 48 | 40 |
| CB-01 | Corner block, hexagon corner, 120 degrees, 2219-T852 forging machined; eight tie holes, dowel holes, a landing for the main rib, R10 inside corners | 21.5 kg | 6 | none |
| CB-02 | Corner block, pentagon corner, 108 degrees | 20.7 kg | none | 5 |
| HP-01 | Hardpoint block in the frame, 50 thick, fitting as drawn (pins at z 140) | 6.4 kg | 18 | 15 |
| HP-01M | The same block with the fitting moved onto the pull line (pins at z 76); one or the other after Tuesday | 6.4 kg | alternative | alternative |
| HP-02 | Hardpoint fitting half, titanium Ti-6Al-4V, three bores, 200 x 60 x 30 | 1.0 kg | 18 | 15 |
| HP-03 | Hardpoint pin, 40 mm, 160 long, A286, dry-film lubricated | 1.6 kg | 3 per hardpoint | 3 per hardpoint |
| P-11 | Main rib lateral brace at a node, 7075-T7351, as a pair | 1.1 kg | 18 | 15 |
| PL-01 | Pentagon closure plate, one of five triangles, 10 mm 6061-T6 | 44.9 kg | none | 5 |
| A-01 | The node assembly: star plates, core, rib ends | | 18 | 15 |
| A-02B | The hexagon panel assembly | | 1 | |
| A-03 | The corner node assembly: two hexagon blocks and one pentagon block at a vertex, 12 ties and 6 dowels | 76.6 kg | | |
| A-04 | The pentagon panel assembly, schematic: five frames, five main ribs, the hub, 90 secondary ribs, five blocks, the closure plate | 922 kg | | 1 |

P-10 and A-02A, the option A rib and panel, are kept in the library as superseded. The shutters, the outer glass layers and the pentagon equipment are not in the library yet; they are not sized.

## What the new solids told us (8 November)

Building the corner block, the hardpoint and the pentagon as solids found ten things the sheets had not, and they are the first items for Friday. They are written in full in the README that goes with the parts library.

1. **The joint faces lean, and the solids do not yet.** Every part in the library is drawn straight along the panel's own depth, like the frame member P-06. The real joint face lies on the radial plane through the shell edge and leans 20.9 degrees (hexagon) or 16.5 degrees (pentagon) to the panel normal, so the real block section is a parallelogram and the ties are normal to the leaning face. Put three straight blocks at a vertex (A-03) and they overlap in a prism about 75 mm on a side and the tie holes do not line up. The corner model C1 has the leaning face; the solids will get it next.
2. **Tie columns moved.** With the ties 87 and 143 mm from the vertex, as briefed, the first hole breaks into the pocket where the main rib lands. They are drawn at 136 and 192 mm, the nearest place where a 45 mm washer clears the landing on both blocks. C1 has them where they were and has to be rerun.
3. **The main rib landing cannot go 30 mm into the block** from the re-entrant corner: the block is only 96 mm (hexagon) or 88 mm (pentagon) wide there and a 110 mm pocket would break through the joint faces. The pocket bottom sits 55 or 60 mm from the vertex, which leaves 20 and 16 mm of metal to the joint face, thin, and uses up the R12 at the vertex. A question for Marco.
4. **The moved hardpoint does not hit the bolt row after all**, but its pad does cover the two plain bolts beside it. The bore at z 56 to 96 leaves 9.7 mm of metal to the nearest bolt hole and 20 mm to the inner gland. The 200 by 60 mm pad at z 46 to 106 sits over the two plain bolts at z 58, so their nuts would be under the fitting. In the solid HP-01M those two bolts are drawn deeper, at z 118, only to make a solid that closes; the seam model says the seal opens as the bolts move away from it, so that is the wrong answer. The real choices are to move those two bolts along the seam into the web beside the block, where the hardpoint model had them, or a shorter fitting. Sheet RF-07 is to be read with this.
5. **The fitting as drawn** (pads at z 110 to 170) touches the underside of the seat lip, with 10 mm from the bore to the lip, and fails the seal check as a hinge. It is kept for comparison.
6. **The fitting's own fixing holes**: two rows of three cannot clear three 40 mm bores on a 60 mm plate, so they are two pairs at the ends and one hole between each pair of bores, 5.8 mm from the bore in the block. Those bolts are in tension under the seam pull and are not sized.
7. **The brace P-11** cannot be a flat 8 mm plate on the web, because the cap angle has a 12 mm leg down the web from z 300 to 375; it steps out 12 mm at z 280 to 300 and runs up the outside of the leg. Its size is a proposal with no check behind it yet.
8. **The closure plate** cut 100 mm back from the rib centre lines, as briefed, would sit on nothing; it is cut 10 mm back like the panes, with an apex cut round the hub and corner cuts to the block outline. The hub's fork cheeks cross its edge between 100 and 210 mm from the centre, which needs a notch or a 15 mm cut-back there. Which side of the frame it sits on is still Q57; it is drawn on the cabin side.
9. **The pentagon dowel** is at z 246.3 on the pentagon block, not 240, so that it meets the hexagon's dowel on the joint plane.
10. **The mass of the new parts** has not been put into the 36.1 t. A corner node is 77 kg, so the 60 nodes are 4.6 t, and a hardpoint with its two blocks, two fitting halves and three pins is about 20 kg, so 270 of them are 5.3 t. Both are heavier than the mass budget assumed, and they are the two places to take weight out once the position and the pin count are settled.
