# 3. The test pieces

These are the parts a shop quotes and makes this winter. The five TP sheets follow this page, and the STEP files for every piece are in the zip that goes with the package (HCSA-Rev-F-test-pieces-STEP-9-Nov-2026.zip, also at hcsa-site.vercel.app/downloads). They were built from the Rev F parameter file the same way the parts library was, so the seam in the test piece is the seam on the flight sheets: 180 mm deep, glands 7.1 x 4.0 at z' 18 and 32, the RTV recess at z' 42, the bolt row at z' 58 on a 75 mm pitch.

## What the pieces are

| Article | What it is | Pieces | Material | Mass |
| --- | --- | --- | --- | --- |
| T1-075 | A 75 mm slice of a seam: one bolt, the two cords and the RTV bead, pulled apart in the 100 kN frame | Frame A, frame B, 2 pull blocks | Frames 6061-T651, blocks 4140 QT | 3.0 kg of frames, 14.4 kg of blocks |
| T1-150 | A 150 mm slice, two bolts | The same | The same | 6.1 and 29.5 kg |
| T1-225 | A 225 mm slice, three bolts | The same | The same | 9.1 and 44.4 kg |
| SA-550 | The 550 mm article: a seam with a dummy hardpoint, three 40 mm pins at 60 mm pitch in a 200 mm block, and 2 + 2 seam bolts beside it. The pins are loose by design and the article is pulled in prying through the lugs, so the seam bolts and the seals carry it | Frame A, frame B with the hardpoint block, 2 pull blocks | Frames 6061-T651, blocks 4140 QT | 21.9 kg of frames, 109 kg of blocks |
| SA-550 moved | The same article with the dummy fitting moved onto the line of the pull (z' 46 to 106 instead of 110 to 170). This is the one we make: Rick agreed the moved fitting on 10 November. Sheet TP-03 draws both positions and the STEP zip has both | The same | The same | The same |
| F-01 to F-03 | The pinned fixture that puts the article in the frame: the lug plate, the fork with its 20 mm pin, and the adapter to the machine | 3 pieces | 4140 QT | See TP-04 |

Each frame has legs 200 mm long so the pull block can bolt to it from both bearing faces with M12 screws. Run 1 pulls straight through the block centre at z 90 with an M24 rod, run 2 pulls through a pin on the z 24 line, near the outer flange, which pries the seam open the way pressure does. The pull blocks are tall (160 mm) because the seat lip at the cabin face moved the frame to 180 mm deep; the old problem of a 2 mm wall round the M24 thread is gone.

## The tolerances, tight only where the seal or the fit needs it

Marco's point on 7 November was that our 0.05 mm everywhere would make every part a precision part. The table on TP-00 proposes two classes. Tight: gland depth 4.0 plus or minus 0.05, because that sets the squeeze on the cord; gland width 7.1 plus or minus 0.10; gland position plus or minus 0.15; the joint face flat to 0.10 over 150 mm and 0.15 over the 550; the three 40 mm bores at plus 0.10 and minus nothing. Normal: the bolt holes drilled 8.5, positioned to plus or minus 0.2; the leg holes 14.0, positioned to plus or minus 0.2 on the pattern; the block faces parallel to 0.10; and ISO 2768-m for everything else. The 7 degree swing of a shop floor moves 550 mm of aluminium by about 0.09 mm, so the measurements that matter are taken at 20 degrees.

### Why only two features are tight

The cord is 5.33 mm in a 4.0 mm gland, a squeeze of 25 percent. What eats that squeeze can be added up.

| Stack | Gap added | Squeeze left |
| --- | --- | --- |
| Nominal cord and gland | none | 25.0 % |
| Thinnest cord (5.20) in the deepest gland (4.05), seam open 0.11 mm under load, each face flat to 0.05 | 0.21 mm | 18.1 % |
| The same with each face flat to 0.10, the TP-00 proposal | 0.31 mm | 16.2 % |
| The same with each face flat to 0.20 | 0.51 mm | 12.3 % |

Relaxing the flatness from 0.05 to 0.10 costs two points of squeeze. Nothing else on the frame is in this sum, which is why nothing else is tight. Parker's minimum squeeze for this cord is asked and not yet answered; the leak test on the 550 article with a 0.1 and a 0.2 mm shim under one face would measure it.

### Hardware

The test pieces use catalogue hardware from McMaster-Carr. At 4 kN the seam bolt is far below the strength of any 5/16-24 bolt, so its stiffness is what matters, and alloy steel and A286 are equally stiff to within one percent. An alloy steel 5/16-24 screw and nut stands in for the NAS6705 in every test. The flight parts list keeps the NAS numbers.

## Two options for the shop

- The blocks in 6061-T651 instead of 4140. On the 550 article each block is then 19 kg instead of 55, and aluminium is quicker to machine. The M12 threads then want inserts.
- Legs 120 mm instead of 200 on the slices. The 150 mm slice with short legs is in the STEP zip as T1-150-DFMlegs120, so a shop can quote both.

## What a shop needs from us

The STEP files and the TP sheets, the quantities (one of each slice, one 550 article, two blocks per article, one fixture set), the material and heat treatment, the tolerance table, and the surface finish on the joint face and the glands, Ra 0.8. This zip is what goes to Xometry for instant quotes, as Manos told Marco.

## Still open on the test pieces

- Settled on 10 November: we cut SA-550 moved, with the dummy fitting on the line of the pull.
- Whether run 1, the straight pull, stays in the plan now that run 2 pulls at the right depth.
- The leak test on the 550 article: the pass rate, and the port and fittings for it.
- The M24 pull in run 1 is 14 mm off the pull line of the slices (z 90 against z 76); we have noted it and think it does not matter for a straight pull, but it is a question for Marco.
- The T0 glass bars and the T2 quarter panel are not drawn at Rev F yet. The bars follow the ENGN 1440 four-point method, 1 inch by 1/8 inch, and their drawing and arris size are still owed (Q04); the quarter panel waits on the pane clamp.
