# HCSA Rev F release package, on one page

For Marco Cross and Rick Fleeter, for the fabrication review on Friday 13 November at 1:00. It is the release of drawings in our schedule and replaces the Master Document of 27 October (Rev E). Rev F is the working baseline of November 2026: nothing is released for manufacture, and the test pieces are for quotation. Manos Theofanous and the HCSA team; checked and corrected 9 November 2026.

## What is in it

About fifty pages in eight parts, with fourteen A3 sheets, the STEP files of every test piece and new flight part, and the master 3D model on the website: what changed since October; the facility taken apart, with the spec card; every flight part, drawn (RF-01 to RF-09) and in 3D; the test pieces a shop quotes from (TP-00 to TP-04); what the computer tests found; what is still open; the positions and questions for the call; where every file lives (Drive, Week 10, and hcsa-site.vercel.app).

## The design in one paragraph

A truncated icosahedron 11,151 mm across: 20 glass hexagons and 12 solid pentagons with 2,250 mm edges, 90 seams, 60 corners. The cabin runs at 0.8 atm with 26 percent oxygen, a module for a 1 atm commercial station, joined through a transfer lock. Main ribs are I-beams 400 by 100 mm, secondary ribs 180 by 60 mm on a 562.5 mm grid, so about 61 percent of each window is glass: 21 mm BOROFLOAT 33 in 531 mm panes, 96 to a hexagon. Each seam is a 180 mm deep frame with two butyl loops in 7.1 by 4.0 mm glands, an RTV bead behind them and sixteen NAS6705 bolts at 4 kN that only clamp the seals; the pull across the seam goes through three pinned hardpoints. Each corner is a machined block tied to its two neighbours by 7/8-14 Inconel ties at 198 kN. The structure is about 36 t.

## What the computer tests say

At 0.8 atm the corners pass with about 12 kN of room on the worst tie, 214.5 against 227 kN at proof; with the hatch open at 1 atm they pass by 0.7 kN and the main rib by under 1 percent, so that case is the design point. The plain seams pass with about 40 percent to spare. The hardpoint where it was drawn fails: the frames hinge about it and the seals open at 0.2 to 0.5 atm. On the line of the pull the seal at the fitting holds to 2.5 atm, and the bolt beside it is 3 percent short of its 1.93 atm; runs with that bolt closer and tighter, and with the tie preload at 180 and 160 kN, are on the laptop now. The panes hold under steady launch loads; vibration is a hand estimate only.

## What the solids and the check found

The corner node now fits: the blocks have their real leaning joint faces, and three of them at a vertex share no volume with all 12 tie holes on axis. The ties sit 130 and 186 mm from the vertex line and the rib landing leaves 17 to 20 mm of metal to the joint face. The hardpoint part does not fit yet. The real fitting is a titanium lug in a two-cheek clevis with pins along the depth; its slot clears the seals and the bolts, but in the 180 mm frame it runs into the flange and the ribs and its pins cannot be put in. The parts lists add up to more than the model's 36 t (about 40 t before the nodes and fittings), and that is not reconciled.

## What is still open

Rick signs the 0.8 atm cabin, the withdrawal of leak before break and the factors on Tuesday, and decides the hardpoint position. Without an answer yet: a hardpoint fitting that fits the frame, the flight alloy (6061 analysed, 7050 proposed), how the seal loops turn their corners at R16, the clamp that holds the panes through vibration, the mass, and which side the pentagon closure plate sits on. Life support, water, power and radiation are at concept level.

## For Marco: positions and questions

Four positions to agree or knock down: the corner block machined from plate, not cast; 6061 for test pieces and 7050-T7451 for flight; only gland depth and face flatness held tight; the ties set with a jackbolt nut and read by stretch. Three questions: how to build a stiff pinned joint for 110 kN per atmosphere that a crew can close inside 180 mm of depth; whether NASA's general spectrum and a tap test are the right start on vibration; and how to hold the frame to cut glands and face in one setting.
