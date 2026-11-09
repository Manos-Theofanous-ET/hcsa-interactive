# HCSA Rev F release package, on one page

For Marco Cross and Rick Fleeter, for the fabrication review on Friday 13 November at 1:00. It is the release of drawings in our schedule and replaces the Master Document of 27 October (Rev E). Rev F is the working baseline of November 2026: nothing is released for manufacture, and the test pieces are for quotation. Manos Theofanous and the HCSA team, 9 November 2026.

## What is in it

Forty-two pages in seven parts, fourteen A3 sheets behind the text, the STEP files of every test piece and new flight part, and the master 3D model on the website. Part 0 is what changed since October; 1 the facility, with the spec card and stills of the model taken apart; 2 every flight part, on sheets RF-01 to RF-09 and in 3D in the parts library; 3 the test pieces a shop quotes from, sheets TP-00 to TP-04 with the tolerance table and bill of materials; 4 what the computer tests found; 5 what is still open, by subsystem; 6 the questions for the call, in order; 7 where every file lives.

## The design in one paragraph

A truncated icosahedron 11,151 mm across: 20 glass hexagons and 12 solid pentagons with 2,250 mm edges, 90 seams, 60 corners. The cabin runs at 0.8 atm with 26 percent oxygen, a module for a 1 atm commercial station, joined through a transfer lock. Main ribs are I-beams 400 by 100 mm, secondary ribs 180 by 60 mm on a 562.5 mm grid, so about 61 percent of each window is glass: 21 mm BOROFLOAT 33 in 531 mm panes, 96 to a hexagon. Each seam is a 180 mm deep frame with two butyl loops in 7.1 by 4.0 mm glands, an RTV bead behind them and sixteen NAS6705 bolts at 4 kN that only clamp the seals; the pull across the seam goes through three pinned hardpoints. Each corner is a machined block tied to its two neighbours by 7/8-14 Inconel ties at 198 kN. The structure is about 36 t.

## What the computer tests say

At 0.8 atm the corners pass with about 12 kN of room on the worst tie, 214.5 against 227 kN at proof, and still pass by 0.7 kN if the hatch is left open and the cabin goes to 1 atm; the seams pass with about 40 percent margin. The hardpoint as drawn does not work: the fitting sits 64 mm deeper than the line of the pull, the frames hinge about it and the seals open at 0.2 to 0.5 atm. Moved onto the pull line it holds to 2.5 atm. The panes hold at launch with a clamp.

## What building the solids found

Every part is drawn straight, but the real joint face leans with the seam plane (20.9 degrees on a hexagon, 16.5 on a pentagon), so the real corner block is a wedge and three straight blocks overlap at a vertex; the leaning face is the next cut. The tie columns moved out to 136 and 192 mm to clear the rib landing, which leaves 20 mm of metal to the joint face. The moved hardpoint clears the bolt row, but its pad covers the two bolts beside it, and moving them deeper is wrong because the seal opens as the bolts move away from it. A corner node is 77 kg and a hardpoint about 20 kg: 4.6 t of nodes and 5.3 t of hardpoints, neither yet in the 36 t.

## What is still open

Rick signs the 0.8 atm cabin, the withdrawal of leak before break and the factors on Tuesday, and decides the hardpoint position. Without an answer yet: how the seal loops turn their corners at R16, how the panes are held at launch, the pass leak rate for the 550 article, and which side of the frame the pentagon closure plate sits on. Life support, water, power and radiation are at concept level.

## The three questions for Marco

Whether the corner block, with R10 inside radii and a rib landing 20 mm from a sealing face, is a part he would machine from a forging or cast. Whether the tolerance split on the test pieces is right (flatness 0.10 over 150 mm, 0.15 over 550) and whether the pull blocks should be 6061, not 4140. Which way out for the moved hardpoint: bolts moved along the seam, a shorter fitting, or no bolts under the pad.

## Where it lives

Drive, UPDATES, Week 10: the package PDF, the sheets, the STEP zips. Website hcsa-site.vercel.app: /blueprints, /parts, /model and /explore for the facility taken apart, /downloads for the files; all on pull request 6, waiting to be merged.
