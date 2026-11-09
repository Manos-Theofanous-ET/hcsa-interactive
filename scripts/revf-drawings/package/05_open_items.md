# 5. What is still open, by subsystem

*Written 7 November, brought up to date on 9 November: items the 8 November drawings and solids closed are marked done, and the sheet numbers are the Rev F ones.*

This chapter pulls together the open questions register (rows Q01 to Q101), the Rev F open items of 5 November, the hardpoint and pane results of 6 and 7 November, Marco's comments of 7 November, and the "what is not yet proven" lists in TRUTH Rev D for launch, plants, air, water, thermal and radiation. Each item says who decides and what it holds up. Items that Marco can help with on Friday are marked **(Marco)**.

## 1. Decisions waiting on Rick, Tuesday 10 November

- Sign the 0.8 atm cabin with 26 percent oxygen, docked to a 1 atm commercial station through a hatch-shut transfer lock (Q70, Q97 to Q99).
- Withdraw leak before break as a requirement, since in the plain bays the metal yields before the seals open (Q93).
- The safety factors: 2.0 at ultimate and 1.5 at proof on the 12.3 psia design pressure, 145 MPa allowable on 6061-T6 (Q68).
- The hardpoint fitting: move it onto the line of the pull (the HP1M study), add a tie on the space side of the seals, or bigger bolts next to the fitting. This changes sheet RF-07 and the TP3 envelope.
- Glass bars now on the 0.5 kN frame, or in ENGN 1440 in the spring (Q42); his endorsements for Thornton Tomasetti, Research at Brown and ASTM (Q63 to Q65).

## 2. Structure

| Item | What is open | Who, when | Holds up |
| --- | --- | --- | --- |
| Hardpoint position | As drawn the hardpoint seal fails (0.22 atm free, 0.47 held, against 1.93). Moved onto the pull line it holds. The nearest seam bolts are 131 to 141 mm from the hardpoint centre, clear of the 200 mm fitting. The fitting solids in the parts library are an envelope only and must be redrawn from the C3 model (a plate in two cheeks with the pins in double shear) | Manos and Rick decide; Claude redraws; HP1 rerun with real pins and bores | RF-07, the TP3 envelope, the 550 article's dummy hardpoint pockets |
| Plain bolt next to the hardpoint | Its seal band reaches 0.11 mm at 1.87 atm, just under 1.93. A closer bolt (115 mm from the centre) and a higher preload (6 kN) are both running on the laptop, 9 Nov | Claude, laptop | RF-07 |
| Corner node, machinability **(Marco)** | Marco: as drawn it cannot be machined; inside corners need radii an end mill can cut; it could be cast, which may change the material. Also the tie-to-fillet clash (Q29), the O10 corner seal section (Q27), the units on Heintges' 4-6 lap (Q28), and the way the main rib flanges enter the block | Manos with Marco Friday; Fusion | RE-06-2, T3 |
| Corner block stress limit | 95th percentile 236 MPa at proof at 0.8 atm, 255 MPa with the hatch open; no limit has been set | Manos, Rick, Henann | Signing the corner |
| Corner tie tightening | 198 kN by measured stretch. The band of 196.5 to 198.1 kN and the 0.7 kN hatch-open margin are both tighter than any tightening method can hold or any model can promise, so either the preload comes down (runs at 180 and 160 kN queued 9 Nov) or the hatch-open case is ruled out by the lock. A multi-jackbolt nut would set it with a hand wrench | Manos, with Marco on the method | RF-08, T3 |
| Corner block stock | 2219-T852 hand forging was proposed (Q85); we now propose machining from 7050-T7451 or 2219-T851 plate (9 Nov note); no quotes yet (Q58 for ties and titanium) | Manos, suppliers | Cost |
| Main rib bracing | The star-plate node must hold the main rib's cabin flange sideways every 562 mm (Q95). Drawn as P-11, a proposal with no check behind it | Claude | RF-08, parts A-01 |
| Rib joints | 1,620 rib joints inside the pressure boundary and the main rib splice are not designed; the bolted star-plate grid is now the way (Marco, 7 Nov, by serviceability) | Manos | RF-06, cost |
| Hardpoint bore chamfers | 194 to 197 MPa at 1.5 x proof against 160 (Q18): accept, bush or thicken | Manos | Hardpoint drawing |
| Pane clamp | How the panes are held is a proposal (OPEN-11): the clamp bar, the strip squeeze, the bolt spacing, the 531 or 517 mm cut (OPEN-10), the setting strip hardness (Q13) | Manos | RF-01, RF-06, P-08 |
| Glass | The Weibull m from T0 decides 21 mm and the pane size (708 upside, 425 fallback); SCHOTT still owes flatness, wedge and sag data for 21 mm (Q03, Q06, Q77) | T0 (spring 2027), SCHOTT | Every glass number |
| Backup pane | A second glass pane or an unloaded acrylic pane behind L7 (Q14); the 1/200 deflection rule (Q15) | Manos, Rick, Henann, after T0 | Stack mass |
| Launch **(Marco)** | Only quasi-static stand-in loads are checked. Random vibration and the 137.7 dB sound field need a model; pack the panels outer face up or rate the clamps (Q96); SpaceX's V3 load factors and spectrum are not public | Claude for the model; Manos asks SpaceX | Packing plan, pane clamps |
| Flight alloy | Every check in part 4 is against 6061-T6 (145 MPa allowable, 240 yield). Whether the flight frames, ribs and blocks stay 6061 or go to 2219 or 7050-T7451 is open; 7050 is our proposal of 9 Nov | Rick, with Marco | Materials section, the corner block stress limit |
| Shell pre-camber and misalignment | The pre-cambered shell (Q52) and the 0.2 mm misalignment case (Q24) have not run | Claude | T1 run 2 |

## 3. Seals

| Item | What is open | Who, when | Holds up |
| --- | --- | --- | --- |
| Seal loop corners | Parker wants an inside radius of 16 mm at least, 32 ideally; the racetrack end as drawn is R4.3. Moving the bolt row is ruled out, so the loop turns around the end bolt or the flange widens at the corner block. Needs Parker's answer on "two loops" and Fusion (Q92) | Manos, Parker, Fusion | RF-02, the T1 slices, the 550 article, the O10 seal |
| The sealing gap | 0.11 mm is a requirement, not a measurement. Nobody has measured the gap at which butyl stops sealing; the 550 article pulled in prying is what measures it | Test, December to February | The seam requirement wording (Q94) |
| Butyl life | No stress-relaxation or recovery data for butyl from Parker (Q39); what life test we run | Nobody assigned | TRUTH 10.8 |
| Leak detection | Should each panel have leak detection between the seals (Q38)? With leak before break gone, the ports and the relief valve are the warning | Manos, Rick | TRUTH 14.2 |
| RTV on the ground | Cure the RTV566 bead on the ground in one frame (Q80); venting the outer gap to space against section 6.5 (Q37) | Manos, Rick | Assembly sequence |
| Seal supply | Two spliced BA500 loops through Sandem or Sealing Specialties; RTV566 sample from Momentive or the SkyGeek kit | Manos, after the funding decision | The 550 article |

## 4. Fabrication and the test pieces

| Item | What is open | Who, when | Holds up |
| --- | --- | --- | --- |
| A shop **(Marco)** | Blackhawk and JEPIS declined. Marco says Xometry. The STEP files of the frames at 180 mm and the pull blocks exist since 8 Nov | Manos, quotes this week | Everything |
| Tolerances **(Marco)** | Marco: do not hold 0.05 or even 0.1 mm on every dimension; 7 C of temperature moves 550 mm of aluminium by 0.09 mm; design the part so the machinist does not have to be a hero. The table is on sheet TP-00, and the squeeze sum behind it is in part 3: only the gland depth and the joint face flatness are tight | Marco reviews | The release to the shop |
| Material **(Marco)** | 6061-T651 as drawn, or a 7000-series alloy that needs no heat treatment after machining, as Marco suggests; and the fixturing that holds the part flat. Our position is in part 6 | Marco | The RFQ |
| Design for manufacture **(Marco)** | Marco wants to go through the parts for changes that make them less scary for a shop; the thin walls round the M24 threads in the pull blocks are gone with the 160 mm block | Marco | TP-01 to TP-04 |
| Parts from McMaster **(Marco)** | Spec the test-article hardware from McMaster-Carr; the flight bolts stay NAS parts. The parts memo for NAS6705U27 and its ratings is still owed (Q17) | Manos | The parts order |
| T1 slices and the 550 article | Done 8 Nov as sheets TP-00 to TP-04 and 21 solids; no sheet is checked or released yet (Q55) | Marco's review | The order |
| Instron adapter | Cannot be drawn until the three frame interfaces are measured with Jerry; the Instron is free from 18 November (Q21) | Manos, Jerry | T1 |
| T0 bars | The test-bar drawing and the arris size from Swift (Q04); two bar sizes and the count (Q51); order after the funding decision | Manos, Swift, Rick | T0 |
| T2 water panel | Redraw the 1:4 article on the Rev F grid with option B ribs and the tie-bolt circle moved in; a host and a safety sign-off (Q45); a budget for B E Peterson (Q46); the gauge map. Marco says do it, with a written plan, video and a process watcher | Manos, Breuer | T2 in February or March |
| Pentagon closure **(Marco)** | Which side of the ribs the 10 mm closure plate goes on and how it is held and sealed as five triangles (Q57) | Manos, Marco | RF-09 |
| Printed fit checks | PLA arrives Tuesday 10 November; the PCBWay files still have to be uploaded; the 1:20 model should show option B ribs | Manos | Fit checks |
| Cold soak | No chamber for the 550 article at -40 C **(Marco)**; D6 not rerun with butyl | Manos | D6 |

## 5. Tests and instruments

- Dewesoft loan dates and units, late November (Q44); the spring test plan is due 22 November.
- Trans-Tek LVDTs, yes or no on 12 November (Q48). TML gauges: reply with the 5 m lead wire and the counts (Q47). Chenjie's ENGN 0310 recorder as a backup (Q49).
- Whether a borrowed recorder can sit beside Jerry's frame (Q22); the safety shield; the gauged bolts (not priced).
- The T1 load tables are written per atmosphere at 1 atm and should be restated against 12.3 psia.
- Whether Prof. Henann reviews the test plan (Q50), and the 10 percent pass rule.
- The pass leak rate between the two cords on the 550 article **(Marco)**.

## 6. Air and fire (life support)

Nobody on this semester's team owns air, water or thermal; Skye and Lauren wrote these sections in the spring. Gerasimos owns the plants.

- At 81 kPa the fans need about 20 percent more airflow to hold the hexagon-pentagon difference, and every fan, avionics box, laptop and medical device has to be checked for cooling at 81 kPa (Q98). Water boils at about 94 C.
- Fire: 26 percent oxygen at 81 kPa is our interpolation inside the ISS fire data; every fabric, cushion, pouch, plant and plastic needs NASA-STD-6001 testing at the real mix.
- From TRUTH Rev D 5.9: the scrubber, fan and isolation hardware are first-order estimates scaled from ISS parts; the 24-hour safe-haven window is a planning assumption with no fault tree; the mode switching (unoccupied, visit, safe haven) is not specified; the emergency oxygen and nitrogen tanks are not specified; the plant contribution in an emergency is not credited.
- The TRUTH 5.3 setpoints still say 1 atm and ISS practice; they change to 81 kPa and 26 percent oxygen in Rev F.

## 7. Water and thermal

- From TRUTH Rev D 6.7: the evaporator and condenser pentagons must face sun and shadow, which depends on the orbit and attitude; the ring beam length depends on where the greenhouse pentagons sit; the thermal balance uses guessed emissivity and sink temperature; the inner pane may drop below the dew point in eclipse with the plants transpiring; the distillation loop's start and stop across eclipse is not worked out; the pump is not chosen; there is no backup water path if the loop fails.
- The 3 November research page says the condenser takes up to about 36 kg a day of humidity and a dehumidifier does the rest; the condensation reasoning behind the outer gap being vented to space has to be checked again.
- A time-varying thermal model of the whole station, and who builds it (Q87). The 1 November orbital model covers the hexagon-pentagon difference only.
- Solar cells must stand off the pentagon structure on an insulating blanket, or the hexagon-pentagon difference could reach about 100 K.

## 8. Power, the pentagons and the column

- Which pentagons carry which roles (eleven identical and one dock, as Manos set on 25 October, against the earlier split in TRUTH and the model), and which way the column runs (Q88).
- Whether the inflatable shield only holds shape or must hold breathable air as a repair balloon; at breathable pressure it pulls hundreds of kN on its pentagon (Q89).
- Stabilising thrusters in or out (Q90).
- The greenhouses get no daylight: 6 to 9 kW of LED, and the LEDs are not qualified for LEO thermal cycling (TRUTH 4.9). The solar array and battery sizing for that load is not in TRUTH.
- The column carries no pressure load and must slide at one end; TRUTH disagrees with itself on where it ends.

## 9. Docking and the transfer lock

- The transfer lock is a concept, not sized (RF-04): the relief valve of at least 5 cm², the 2.3 to 2.9 mm equalising orifice, who owns the vestibule valves (Q97).
- Whether a commercial station operator (Orbital Reef or another) accepts a hatch-shut interface (Q99); Stellar Amenities is the first contact. If not, the module runs at 1 atm, where the structure passes with 14 percent margin and the corner sits on its limit (Q100).
- From TRUTH Rev D 5.9: each candidate host has a different docking and ECLSS interface; the ISS-era "shared atmosphere" wording has to go.

## 10. Radiation and the MMOD shields

- From TRUTH Rev D 7.8: no Monte Carlo dose model yet; the 1 to 2 cm HDPE layer is a first-order pick; the deployment mechanism of the pentagon-localised inflatable shields is not designed; the standoff struts and their thermal cycling are not designed; shields at 360 to 630 kg against a 250 kg placeholder; crew dose tracking is operations work.
- The storm shelter was dropped; visitors go back to the host station on a solar particle event warning.

## 11. Plants

- From TRUTH Rev D 4.9: automated care between visits is not validated at six-alcove scale; plant survival through launch vibration is untested; nutrient dosing reliability, pests, cross-contamination between alcoves, seed viability and crop-loss contingency are open research topics.
- The tasting trays, the drinks ring and the plant placement on the mast (5 November interior) are not in TRUTH yet.

## 12. Interior

- Marina to confirm the six pods: size, shape, count, and whether the mouths face out or toward the mast.
- Pod shell material and mass, the strut mounts, how the pods come off for launch and service; the fire rating of cushions and pouches at 26 percent oxygen.
- The ramp and cycling track from Marina's images: in or out (Q61). The circulation lengths redone on the Rev F interior.
- The 67-question interior brief of 25 October: construction, sizes, masses, attachment and ownership of every interior piece.
- The front-page loop video still shows the older, larger pods; it needs rendering again on the laptop GPU.

## 13. Assembly in orbit and operations

- From TRUTH Rev D 3.7: magnetic self-alignment has not been shown at 2.25 m panel scale; the assembly time (70 to 190 hours in different places) is not validated; shirtsleeve assembly inside Starship is not an established practice.
- Zero-clearance pins against magnet-guided alignment to 1 to 2 cm: tapered or expanding pins are a proposal **(Marco)**.
- How the panels are repaired in orbit, which Marco says should drive the frame build; a damaged rib segment is one part to replace in the bolted grid.
- A ground trial: the docking pentagon with its first ring of five hexagons.
- The Starship V3 payload envelope drawing, which we still do not have; the 20 flat layers with the column upright beside them (Q79).

## 14. Documents, website and the paper

- TRUTH Rev F exists only as replacement text; there is no assembled Rev E or Rev F document. Rev D (14 October) is the last full one. Manos signs Rev F once Rick has answered Q68, Q70 and Q93 (Q76).
- The 47 items on the Rev E fix list of 24 October are not applied. The team pages still show the spring team (Q73); the Heintges credit wording (Q74); the case for the shape (Q69); some meetings have no notes (Q71).
- The Master Document of 27 October is Rev E; this package is its Rev F addendum until it is rebuilt.
- The website carries Rev F since 5 November; the parts library still lacks the corner block, the hardpoint, the pentagon, the shutters and the outer layers; the pane files at 21 mm need regenerating. Marco's "PhD" comes off the credits.
- A conference entry for any talk other than Space Horizons 2026; a Rev E spacewalk and robot assembly time for TRUTH.

## 15. Money and schedule

- No purchasing budget until the funding decision, expected around Thursday 12 November. Then: Trans-Tek, the Swift bars, the cord, the RTV and the A286 bolts.
- Thornton Tomasetti ($13,612 for T1), Research at Brown (up to $500) and Champlin ($19,885 for the water rig) are open; the NASA Rhode Island Space Grant is spring 2027.
- The 550 article leak test needs machining to start by mid-November to make 7 to 14 December; the T1 slices are needed before the late-January Dewesoft loan; the fall report is due 11 December.
- The flight cost estimate ($8M to $26M for the structure) has no quotes behind most lines; Marco thinks many of our force values add cost without need.

*Sources: Open questions register (4 Nov), TRUTH Rev F draft (5 Nov) open items, What is open (4 Nov), The hardpoint seal HP1 (6-7 Nov), Pane at launch PR1 (6 Nov), Marco's review (7 Nov), Interior update (5 Nov), Conference gap list (3 Nov), the HCSA Master Document (27 Oct) chapters 11, 18, 20 and 24, and TRUTH Rev D sections 3.7, 4.9, 5.9, 6.7 and 7.8 (read from the Drive copy; the text export stops at section 8.3, so sections 8 to 16 were not re-read for this list). Written 7 November 2026.*
