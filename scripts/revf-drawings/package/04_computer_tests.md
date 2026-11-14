# 4. What the computer tests say, Rev F - every run, what it found, and the final picture

*Written 7 November, corrected 9 November after an independent check of every number. The corrections are marked where they change a verdict.*

This chapter covers every digital test we have run on the Rev F design: the whole station in the shell model, and the corner, the seam, the hardpoint and the pane in Ansys. Nothing here has been tested on real hardware. Every number is from a model, and the glass numbers rest on published data until the bar tests run.

The design the runs describe: main rib option B (I 400 x 100 x 25, web 8), secondary ribs I 180 x 60 x 10, edge frames 180 mm deep, 21 mm BOROFLOAT 33 panes on the 531 mm grid, two butyl loops in 7.1 x 4.0 mm glands plus RTV566, seam bolts NAS6705U27 at 4 kN in one row at z' 58, corner ties at 198 kN. The cabin is 0.8 atm (81 kPa, 26 percent oxygen); the design pressure is 12.3 psia, set by our own relief valve; proof is 1.5 times that (1.26 atm) and ultimate 2.0 times (1.67 atm). The seals are asked to stay shut to 1.93 atm, which is the ultimate pressure times a further 1.15 (the seal requirement set on 4 November). The hatch-open case, where the cabin reaches the host station's 15.2 psia, is checked on top. The allowable for 6061-T6 is 145 MPa.

## The short version

1. **The structure passes at 0.8 atm, with room.** The worst member is the hexagon main rib at 103 MPa against 145, and 120 MPa with the temperature band and a warm pentagon added. Nothing yields below the 1.67 atm ultimate; the first yield is at 1.96 atm.
2. **The corner passes, and with the hatch open it is right on its limit.** At 0.8 atm the worst tie is 214.5 kN at proof against 227. If the hatch is left open and the cabin rises to 1 atm, it is 226.3 kN, 0.7 kN under the limit. So the 198 kN preload cannot drift upward. Runs on 14 November show it can come down instead: at 180 kN of preload the worst tie at proof is 198.9 kN, and at 160 kN it is 181.5 kN, while the corner faces open 0.57 and 0.60 mm against 0.8. The hatch-open case has not been run at the lower preloads yet.
3. **The plain seam passes.** The seal gap at the worst bay load is 0.070 mm against the 0.11 mm limit, and the load at which it reaches the limit is about 40 percent above the worst bay load. Moving the bolt row to make room for the seal corners does not work, so the bolts stay at z' 58.
4. **The hardpoint as drawn fails, and we know the fix.** The fitting sits 64 mm deeper than the line of the pull, so the two frames hinge about it and the seals open at 0.2 to 0.5 atm instead of 1.93. Moved onto the line of the pull, the seal at the hardpoint itself holds past 2.5 atm, but the seal band at the plain bolt beside it reaches the limit at 1.87 atm, just short of the 1.93 atm required, so the fix is not complete until that bolt is dealt with. Two runs to settle it were set up on 9 November and restarted on 13 November after the laptop shut down. The first finished that night: moving the plain bolt closer to the fitting (115 mm from its centre instead of 137.5) makes it worse, 0.11 mm at about 1.76 atm. The second, with that bolt at 6 kN instead of 4, finished on 14 November and just clears it: 0.11 mm at about 1.95 atm. So the fix is a higher preload on the bolts beside each hardpoint, set by measured stretch, because the margin is about 1 percent. The fitting in that run is a spring between rigid pads, not the real pins. Rick agreed the move on 10 November, and it changes the hardpoint sheet.
5. **The panes hold under the steady launch loads.** Even a snug clamp holds the 21 mm pane at 6 g. That is the easy case. A first hand estimate of random vibration (part 6, and the note of 9 November) puts 6.6 to 10.4 kN on a clamp that holds 9.1 kN, so vibration is what sizes the clamp, and it is not yet run in a model.
6. **Leak before break is gone.** The metal yields at 1.96 atm, and the seals in the plain bays open later, at about 2.9 atm. (Beside a moved hardpoint the seal band reaches its limit at 1.87 atm, so there the order is not yet settled.) So the warning comes from the relief valve, the pressure control and the leak ports, not from the seals.
7. **The glass is the one number we do not have.** 21 mm at 0.8 atm passes if the glass's Weibull m is at least 7.0 on our route and 7.7 NASA-style. Only the bar tests can give that number.
8. **Two requirements came out of the checks:** the main rib must be braced sideways at every secondary rib crossing (unbraced it buckles at 0.79 of its load), and the panes should be packed or clamped so launch cannot lift them off their seats.

## The table

| What | Result | Limit | Verdict | Model, date |
| --- | --- | --- | --- | --- |
| Hexagon main rib, 0.8 atm | 103 MPa | 145 MPa | Pass, 41 % margin | Shell model, 4 Nov |
| Same, with the ±120 C band and the pentagon 15 K warmer | 120 MPa | 145 MPa | Pass, 21 % | Shell model, 4 Nov |
| Hexagon frame, same loads | 102 MPa | 145 MPa | Pass, 42 % | Shell model, 4 Nov |
| Secondary rib, same loads | 97 MPa | 145 MPa | Pass, 49 % | Shell model, 4 Nov |
| Pentagon main rib, same loads | 104 MPa | 145 MPa | Pass, 39 % | Shell model, 4 Nov |
| First yield against ultimate | 1.96 atm | 1.67 atm | Pass, 17 % | Shell model, 4 Nov |
| Main rib at proof, no yield | 172 MPa | 240 MPa | Pass | Shell model, 4 Nov |
| Hatch open, cabin at 1 atm: main rib, pressure only | 127 MPa | 145 MPa | Pass, 14 % | Shell model, 4 Nov |
| Same with the band and warm pentagon added (plus 17 MPa, as in the 0.8 atm row) | about 144 MPa | 145 MPa | Pass by under 1 % | Sum, 9 Nov |
| Frame bow with the band | 0.75 mm (0.85 at 1 atm) | 1.0 mm | Pass | Shell model, 4 Nov |
| Main rib sideways buckling, braced every 562 mm | 8.4 times | 1.0 | Pass if braced | Hand calc, 4 Nov |
| Same, unbraced over 2.25 m | 0.79 times | 1.0 | Fail: bracing is now a requirement | Hand calc, 4 Nov |
| Worst corner load | 235 kN at the 12.3 psia design pressure, 290 kN at the host's 15.2 psia | | | Shell model, 5 Nov |
| Corner tie at proof, 0.8 atm | 214.5 kN | 227 kN | Pass | Ansys C1, 5 Nov |
| Same, ties preloaded to 180 kN | 198.9 kN; faces open 0.574 mm | 227 kN; 0.8 mm | Pass, 28 kN to spare | Ansys C1, 14 Nov |
| Same, ties preloaded to 160 kN | 181.5 kN; faces open 0.604 mm | 227 kN; 0.8 mm | Pass, 45 kN to spare | Ansys C1, 14 Nov |
| Same, pentagon 15 K warmer | 213.3 kN | 227 kN | Pass | Ansys C1, 5 Nov |
| Corner tie at proof, hatch open at 1 atm | 226.3 kN | 227 kN | Pass by 0.7 kN | Ansys C1, 5 Nov |
| Corner faces open at proof | 0.55 mm (0.74 at 1 atm) | 0.8 mm | Pass | Ansys C1, 5 Nov |
| Corner block stress, 95th percentile, at proof | 236 MPa (255 at 1 atm) | none set | Open | Ansys C1, 5 Nov |
| Plain seam, gap at the worst bay load (2.67 kN per bolt), bolt row z' 58 | 0.070 mm | 0.11 mm | Pass, about 40 % | Ansys D1, 5 Nov |
| Plain seam, bolt row moved to z' 70 | 0.123 mm at 2.67 kN per bolt (0.111 mm at 2.48 kN, the 1.93 atm load) | 0.11 mm | Fail: bolts stay at z' 58 | Ansys D1, 5 Nov |
| Plain seam, pressure where the gap reaches 0.11 mm | about 2.9 atm (3.75 kN per bolt) | 1.93 atm | Pass | Ansys D1, 5 Nov |
| Hardpoint seal as drawn, frames free to turn | 0.11 mm at 0.22 atm | 1.93 atm | Fail | Ansys HP1, 6 Nov |
| Hardpoint seal as drawn, frames held at the grips | 0.11 mm at 0.47 atm | 1.93 atm | Fail | Ansys HP1R, 7 Nov |
| Hardpoint seal with the fitting moved onto the pull line | 0.064 mm at 1.93 atm, under 0.11 to 2.5 atm | 0.11 mm | Pass (study) | Ansys HP1M, 7 Nov |
| Seal band at the plain bolt next to the moved fitting | 0.11 mm at 1.87 atm | 1.93 atm | Short by 3 % | Ansys HP1M, 7 Nov |
| Same, plain bolt moved to 115 mm from the fitting centre | 0.11 mm at about 1.76 atm | 1.93 atm | Worse: a closer bolt is not the fix | Ansys HP1M, 13 Nov |
| Same, plain bolt back at 137.5 mm, preloaded to 6 kN | 0.11 mm at about 1.95 atm | 1.93 atm | Pass, about 1 % | Ansys HP1M, 14 Nov |
| Hardpoint pin, 40 mm | 119 MPa | 655 MPa | Pass | Ansys C3, Oct |
| Hardpoint bore chamfers at 1.5 x proof | 194 to 197 MPa on 5 to 7 % of points | 160 MPa | Open (Q18); about 19 % lower at 0.8 atm | Ansys C3, Oct |
| Pane at launch, 6 g, snug clamp | holds; pane lifts 0.012 mm | clamp holds | Pass | Ansys PR1, 6 Nov |
| Pane at launch, clamp strip squeezed 0.3 mm | 9.1 kN clamp, launch changes it by 124 N | | Pass | Ansys PR1, 6 Nov |
| Glass stress in the pane at launch | 0.25 to 0.67 MPa | 6 MPa | Pass | Ansys PR1, 6 Nov |
| Pane mean stress with the band | 8.8 MPa (10.8 at 1 atm) | set by m | | Shell model, 5 Nov |
| Weibull m the 21 mm pane needs at 0.8 atm | 7.0 our route, 7.7 NASA-style | T0 measures m | Open until T0 | Fit of the 16 Oct table, 4 and 5 Nov |
| Same, with the hatch open | 7.9 and 8.8 | | | Same |
| Launch, 6 g along the axis, ribs as cantilevers from the corners | about 10 MPa | 145 MPa | Pass (stand-in loads) | Hand calc, 4 Nov |
| Hexagon-to-pentagon temperature difference | 2.3 to 4.6 K; bad cases about 14 to 15 K | 15 K design case | At the limit in the bad cases unless the fans run 20 % faster | Orbital thermal model, 1 and 4 Nov |
| Relief valve against a stuck 1 inch equalising valve | needs about 5 cm² | | Pass if sized | Orifice flow, 4 Nov |
| Station structure mass | 36.1 t in the shell model; the parts lists add up to more (see part 2) | | To reconcile | Shell model, 5 Nov |

## What each model is, and what it found

**The whole station (shell model).** A beam-and-plate model of all 32 panels in OpenSees, rebuilt in the cloud on 4 November and checked against the 2 November runs to the digit. It is linear, so its results scale with pressure. Three runs are added for the worst case: the direct run at 12.3 psia, the ±120 C frame band, and a run with every pentagon frame and rib 15 K warmer than the hexagons. Adding them is an upper bound. The worst member is the hexagon main rib at 120 MPa, and no member yields below the 1.67 atm ultimate. The model also gives the loads the detailed models use: 280.7 kN on the worst corner at 14.7 psia (235 kN at the 12.3 psia design pressure, 290 kN at the host's 15.2 psia), 108.7 kN per atmosphere on a hardpoint, 1.29 kN per atmosphere on a plain-bay bolt.

**The corner, C1.** The Ansys model of the three corner blocks with their twelve Inconel 718 ties, rebuilt to Rev F on 5 November with option B rib stubs and the real option B loads. At 198 kN of preload the worst tie is 214.5 kN at proof at 0.8 atm, 213.3 kN with the pentagon 15 K warmer, and 226.3 kN with the hatch open at 1 atm. The faces open 0.55 mm at proof (0.74 at 1 atm) against the 0.8 mm the corner seal is sized for. The block stress has no limit set yet: 236 MPa at the 95th percentile at proof, 255 MPa at 1 atm. Still simplified: the rib stubs were reshaped rather than remeshed, the washers are bonded (with an 8 percent allowance on block stress), and the pins, dowels and the O10 corner seal are not in it. With the ties preloaded to 180 kN instead of 198 (14 November) the worst tie at proof is 198.9 kN and the faces open 0.574 mm; at 160 kN it is 181.5 kN and 0.604 mm. So the preload can come down a long way before the faces near their 0.8 mm; the hatch-open case still has to be run at the lower preload before we pick it.

**The seam, D1.** A slice of the plain seam, 180 mm deep, with the two butyl glands, the bolt at 4 kN, and Parker's measured seal force, pulled in prying as the pressure really loads it. The seam opens by rotating about its cabin-side edge from the first newton; there is no parting point, so the bolt preload only shifts the curve a little. With the bolt row at z' 58 the gap between the two cords is 0.070 mm at the worst bay load of 2.67 kN per bolt, and reaches the 0.11 mm limit at 3.75 kN per bolt, about 2.9 atm. With the bolt row moved to z' 70 (to make room for an R16 seal corner) the gap is 0.123 mm, so that move is ruled out and the seal corners have to be solved at the corner block.

**The hardpoint, HP1.** A 350 mm slice with 75 mm of plain seam on each side of the 200 mm hardpoint, pulled with the real station load through pinned grips. As drawn, the TP3 fitting sits at 110 to 170 mm deep while the pull comes in at about 76 mm, so the fitting acts as a hinge: the frames swing open about it, the seals on the far side open first, and the gap between the cords reaches 0.11 mm at 0.22 atm with the frames free and 0.47 atm with them held at the grips. The plain bolts next to the fitting carry about 60 kN at 1.96 atm, well above what a 5/16 bolt holds (about 41 to 45 kN; the rating memo is still owed), and the frame yields around their holes from about 0.5 atm. In a study run with the fitting moved up onto the line of the pull (pads at 46 to 106 mm deep) the hardpoint seal gap is 0.064 mm at 1.93 atm and never reaches 0.11 mm up to 2.5 atm; the fitting takes nearly all the pull, the plain bolts stay at 13 kN, and the frames turn ten times less. One place is still marginal: the seal band at the plain bolt next to the fitting reaches 0.11 mm at 1.87 atm, just under 1.93. Moving that bolt in to 115 mm from the fitting centre (13 November) brings the limit forward to about 1.76 atm, so the closer bolt is ruled out; in that run the last 60 mm of the slice beyond the bolt has no bolt, which a real seam would, so it may read a little pessimistic. The run with the bolt at 6 kN instead of 4 (14 November) just clears it: 0.11 mm at about 1.95 atm, with the bolt carrying 9.1 kN at 1 atm and 14.4 kN at 1.9 atm, and the seal at the fitting itself at 0.083 mm at 2.5 atm. So the two bolts beside each hardpoint get the higher preload, set by measured stretch because the margin is about 1 percent. The fitting in these runs is a spring between rigid pads, not pins and bores, so the real part has to be drawn and rerun. The 2 November figures of 2.9 to 3.4 atm for the hardpoint seals counted only the fitting's stretch and are withdrawn.

**The pane at launch, PR1.** One 21 mm, 531 mm pane on its seat with a proposal clamp (a 25 x 8 mm bar on each edge through a 1.5 mm rubber strip), at 6 g and 2 g along the launch axis both ways and 2 g sideways. The pane weighs 56 N as an uncut triangle (54 N as cut), so 6 g is 336 N in total, about 0.2 N per mm of edge. A snug clamp holds it at every load; with the strip squeezed 0.3 mm the clamp carries 9.1 kN and launch changes that by about 1.4 percent. The glass sees 0.25 to 0.67 MPa. So launch does not size the pane or the clamp; tightening does. Steady loads only: random vibration and the 137.7 dB sound field still need a model, and the clamp itself is still a proposal.

**The hardpoint fitting, C3 (October).** The fitting is a plate from one frame held between two cheeks on the other by three 40 mm pins in double shear. A 40 mm pin holds easily (119 MPa against 655), and the fitting's stiffness, 2.876 million N/mm, is what HP1 uses. At 1.5 times proof a few percent of the points on the aluminium bore chamfers read 194 to 197 MPa against 160; at 0.8 atm they come down about 19 percent. Accept the local yield, bush the bores or thicken them is still Manos's call (Q18).

**The glass.** We fitted the 16 October thickness table and took the shell factor from the station model. A 21 mm pane at 0.8 atm passes if the Weibull m of the glass is at least 7.0 on our route and 7.7 on the NASA-style route; with the hatch open it needs 7.9 and 8.8. SCHOTT's published 25 MPa fractile gives a factor of 2.8 at the design pressure. We stopped quoting 35 MPa as the glass allowable on 5 November, because nothing SCHOTT publishes backs it. The only large-area float data has an m of about 6, which is why T0 matters more than any other test.

**Thermal and launch.** The orbital thermal model of 1 November gives a hexagon-to-pentagon difference of 2 to 4 K pressurised and up to 12 K in bad cases; the 15 K design case covers it. At 0.8 atm the fans move thinner air, so the difference grows to 2.3 to 4.6 K (up to 15 K in bad cases) unless the fans run about 20 percent faster. The launch checks use stand-in load factors from the Falcon user's guide (+6/−2 g along the axis, ±2 g sideways), because the Starship guide does not publish them: the ribs see about 10 MPa at 6 g as cantilevers from the corner blocks. Vibration and acoustics are not modelled, and Marco is right that vibration is the launch case that matters.

## The final picture, in one paragraph

At 0.8 atm the Rev F structure holds its pressure with a fifth to a half of its strength to spare, nothing yields before ultimate, the corner passes, the plain seams pass, and the panes hold under steady launch loads. Two things are not settled by the models. The glass passes only if the bar tests find a consistent enough glass (m of 7.7 or more), and the hardpoint has to move onto the line of the pull, with the two bolts beside it at 6 kN, which changes a drawing and needs a rerun with the real fitting. On top of those, three things are not modelled yet: launch vibration and acoustics, the corner block stress limit, and the seal loop corners through the corner block.

## What still has to run

1. HP1 with the real pins and bores at the new fitting position, after Fusion draws it, and the C3 fitting model rerun for its stiffness there.
2. The corner at 160 or 180 kN of tie preload with the hatch open (1 atm), to pick the new preload. (The bolt beside the hardpoint is settled: at 6 kN it clears 1.93 atm, 14 November.)
3. The pane under a launch vibration spectrum (modal plus random), once SpaceX gives Starship V3 numbers; otherwise with a stand-in spectrum.
4. A stress limit for the corner block, then the block checked against it.
5. D6, the cold seam, with butyl instead of fluorosilicone; D1-550 with the drawn bolt positions; the pre-cambered shell and the 0.2 mm misalignment case.
6. T0 bars (physical): the Weibull m that every glass number waits on.

*Sources: "Does option B at 0.8 atm survive (4 Nov)", "Option B at 0.8 atm (4 Nov)", "Rebuild to Rev F (4-5 Nov)", "Decisions and updates (5 Nov)", "TRUTH Rev F draft (5 Nov)" section 9.5, "The hardpoint seal HP1 (6-7 Nov)", "Pane at launch PR1 (6 Nov)", "Orbital thermal model (1 Nov)", "Glass at 21 mm (4 Nov)", the HCSA Master Document (27 Oct) chapters 14 to 18 for the C3 and Monte Carlo results. Written 7 November 2026.*
