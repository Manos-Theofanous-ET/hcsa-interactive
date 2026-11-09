# 0. Read this first

This is the Rev F release package for Marco Cross, for the call on Friday 13 November at 1:00. It replaces the Master Document of 27 October, which described Rev E. It is shorter, and it leads with the things the call is about: the parts, how they are made, and the test pieces a shop has to quote.

## What changed since the 27 October document

Rev E became Rev F in the first week of November. Eight decisions did it.

| Date | Decision | Why |
| --- | --- | --- |
| 2&nbsp;Nov | Secondary ribs I 180 x 60 x 10, web 5, a custom extrusion | Thinner ribs, more open glass; checked in the rib study |
| 2&nbsp;Nov | Corner tie preload 198 kN, held to 196.5 to 198.1 kN, was 203 | The corner model with the real rib loads |
| 4&nbsp;Nov | Main rib option B, I 400 x 100 x 25, web 8, with bolted cap angles | 3.8 t lighter than option A, with about 61 percent of each window open glass |
| 4&nbsp;Nov | Cabin at 0.8 atm with 26 percent oxygen; a module for a 1 atm commercial station, joined through a transfer lock | Takes a fifth of the load off the structure; the same oxygen pressure as at sea level |
| 5&nbsp;Nov | Pressure pane 21 mm BOROFLOAT 33, in 531 mm panes, 96 to a hexagon; was 22 mm | SCHOTT makes 21 mm as a standard 1,700 x 1,300 sheet; 22 mm would need container loads |
| 5&nbsp;Nov | Edge frame 180 mm deep; glands 7.1 x 4.0 mm; seam bolt NAS6705U27 with a KFN670 nut at 4 kN | The seam model at 180 mm passes with about 40 percent margin |
| 5&nbsp;Nov | Seam bolt row stays at z' 58 | Moving it to z' 70, to give the seal loops rounder corners, failed the seam model |
| 5&nbsp;Nov | We stop quoting 35 MPa as the glass allowable until our own bars measure it | SCHOTT's figure is 25 MPa, a 5 percent fractile on abraded glass, with no Weibull data |

Rick still has to sign three things on Tuesday 10 November: the 0.8 atm cabin with its transfer lock, which is in the table, and two that go with it, withdrawing leak before break and the safety factors of 1.5 at proof and 2.0 at ultimate. Where the package depends on them it says so.

## What the computer tests found, in two sentences

At 0.8 atm the corners pass with about 12 kN of room on the worst tie, and still pass, by 0.7 kN, if the hatch is left open and the cabin goes to 1 atm; the seams pass with about 40 percent margin. The hardpoint as drawn does not work, because the fitting sits 64 mm deeper than the line of the pull and the two frames hinge about it, so the seals open at 0.2 to 0.5 atm; moved onto the line of the pull the seal at the fitting holds to 2.5 atm, with the bolt beside it 3 percent short of its requirement, and that move is the decision for Tuesday.

## How to read the package

- Part 1 is the facility as a whole, taken apart, with the spec card. Part 2 is every flight part, drawn and in 3D. Part 3 is the test pieces, with the drawings and STEP files a shop quotes from. Part 4 is what the computer tests say. Part 5 is everything still open, by subsystem. Part 6 is the questions for the call, in order. Part 7 says where every file lives.
- The sheets are A3 and sit behind the text of their part. Every sheet has a status line in its title block. LOCKED is spec, DECIDED is a decision Manos has taken, PROPOSAL is drawn to carry a load from the models but not yet tested or signed, OPEN is a decision not taken, with the default stated.
- Depths. On the panels, z runs from the outer face at 0 to the cabin seat plane at 180 mm, measured square to the panel. On the joint face of a seam, which is mitred, the same features sit at z', and the table on sheet RF-05 converts one to the other for the hexagon (times 0.934) and the pentagon (times 0.959).
- Every number in the text has a source in the project notes or the parameter file, and the sheets are drawn from that file. Where a number is a model result it says which run.

## Words

Frame A and frame B are the two halves of a seam: A has the flat joint face, B has the glands. A gland is the groove the butyl cord sits in. The corner block is the machined node at each panel corner, and the ties are the bolts that hold three blocks together. The hardpoint is the pinned fitting along a seam that carries the pull across it, so the seam bolts only clamp the seals. Proof is 1.26 atm and ultimate 1.67 atm, on a design pressure of 12.3 psia with our own relief valve. The 550 article is the 550 mm long test piece of a seam with a dummy hardpoint; the T1 slices are the 75, 150 and 225 mm pieces pulled apart in the 100 kN frame.
