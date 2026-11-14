# Appendix. Marco's points worked with numbers (9 Nov)

Marco's review of 7 November raised six things. On 8 November we answered them mostly with drawings. This note answers them with numbers, so the call can start from a position and not from a question. Everything here is a hand calculation or a catalogue figure unless it says it is a model run, and each one ends with what would prove it.

## 1. Tolerances: what the seal needs, and what it does not

The seal is a 5.33 mm butyl cord in a 4.0 mm deep gland, so it is squeezed 25 percent. Four things eat that squeeze, and they can be added up.

| What | Size | Squeeze left |
| --- | --- | --- |
| Nominal cord and gland | 5.33 in 4.00 | 25.0 % |
| Thinnest cord (5.20) in the deepest gland (4.05), the seam open 0.11 mm under load, faces flat to 0.05 each | 0.21 mm of gap | 18.1 % |
| The same with faces flat to 0.10 each (TP-00 proposal) | 0.31 mm | 16.2 % |
| The same with faces flat to 0.20 each | 0.51 mm | 12.3 % |

So going from 0.05 to 0.10 mm flatness costs two points of squeeze, and the seal still has 16 percent in the worst stack. Going to 0.20 would not be safe without Parker's word on the minimum. That is the case for the split on sheet TP-00: the gland depth (plus or minus 0.05) and the joint face flatness (0.10 over 150 mm) are the only two tight features, because they are the only two in this sum. Everything else on the frame, the bolt holes, the leg holes, the length, the flange, can be ordinary shop tolerance, since none of it changes the squeeze.

What would prove it: Parker's minimum squeeze for BA500 in a face seal (asked, not yet answered), and the leak test on the 550 article with shims of 0.1 and 0.2 mm under one face.

## 2. Material: 6061 for the test pieces, a 7000-series alloy where the flight frame yields

Marco suggested 7000-series aluminium. For the test pieces the answer is still 6061-T651: they are only pulled, the load is low, every shop stocks it, and T651 plate is stretched, so it moves least when it is cut. The way to keep it flat is in the cutting order, not the alloy: rough both sides, let it rest, then finish the joint face and the glands in one setting.

For the flight frame his suggestion has a real case. The hardpoint run with the moved fitting (HP1M) puts 235 MPa in the frame at 1.9 atm and 291 MPa at 2.5 atm, against a yield of 240 MPa for 6061-T6. A stronger alloy turns that from marginal to comfortable.

| Alloy and temper | Yield, MPa | Ultimate, MPa | Notes |
| --- | --- | --- | --- |
| 6061-T651 plate | 240 | 290 | Cheap, everywhere, welds; the test-piece choice |
| 2219-T851 plate | 320 to 350 | 430 to 450 | The pressure-vessel alloy, welds, good cold; the flight baseline |
| 7075-T7351 plate | 390 | 475 | Strong, the T73 temper resists stress corrosion; does not weld |
| 7050-T7451 plate | 440 | 510 | Made for thick sections, keeps its strength through 150 mm and more; does not weld |

The values are typical handbook figures and must be replaced by the design allowables before anything is sized. None of these needs heat treatment after machining, which is Marco's other point. The bolted grid was chosen on 7 November, so nothing in the frame is welded, and the usual objection to 7000-series is gone. Proposal for Rick and Marco: keep 6061-T651 for every test piece, and carry 7050-T7451 as the flight alloy for the frame members and the corner blocks, in place of 2219.

## 3. The corner block: machine it from plate, do not cast it, do not forge it

The block weighs 22.9 kg with its leaning faces. Cut from a 2219 or 7050 billet sawn along the lean it starts at about 95 kg, so three quarters is chips. That sounds wasteful and is still the right answer, for three reasons.

- The block carries seal loops on two faces. A casting has porosity, and porosity on a sealing face is a leak path. A casting also carries a casting factor on its strength, 1.25 or more, on a part that is already near its limit.
- A forging needs a die. There are 180 blocks on the station, 120 of one kind and 60 of the other, and a die does not pay for that number. A hand forging is only a better billet.
- Plate in 7050-T7451 is made thick with its strength guaranteed through the thickness, so the 400 mm depth would be cut along the plate, not through it. Every surface of the block is a plane or an R10 corner parallel to the vertex line, which suits one set-up on a rotary axis.

The stud seat is fine in a wrought alloy. The 45 mm washer on the 23.5 mm hole bears on 1,157 square millimetres, which is 171 MPa at the 198 kN preload and 196 MPa at the 227 kN limit.

A correction to our own count: there are 60 corner nodes but 180 corner blocks, three at each vertex. The 8 November text said 60 blocks in two places. A node is 80 kg, so the 60 nodes are 4.8 t.

What would prove it: a quote for one CB-01 from the STEP file, which Xometry can give this week.

## 4. Tightening the ties: the force is reasonable, the wrench is not

Marco called several forces achievable but unreasonable. For the corner tie the stress is ordinary: 198 kN in a 7/8-14 stud is 603 MPa, and 691 MPa at the limit, in Inconel 718 that yields above 1,000 MPa. What is unreasonable is the wrench: 650 to 900 N m on a nut, by an astronaut, to within one percent.

There is a catalogue part made for this. A multi-jackbolt tensioner replaces the nut with a ring of small screws that each push on a hardened washer. Nord-Lock's Superbolt MT series reaches 145 kN on an M24 thread with eight screws at 14 N m each, and 215 kN on an M27 thread with six screws at 36 N m. So the tie can be set with a small hand torque wrench. The two questions it raises are size and accuracy: our 198 kN is above the standard M24 nut's capacity of 185 kN, so it needs either the high-strength series or a 1 inch stud, and the scatter of a jackbolt nut is better than a plain nut but not the one percent the hatch-open case wants. The stretch can still be read by an ultrasonic gauge on the stud end, and that reading, not the torque, is the record.

The other half of the answer is to need less force. Two corner runs at 180 and 160 kN preload, at 0.8 atm, finished on 14 November. In both the faces stay under 0.8 mm at proof (0.574 and 0.604 mm), and the worst tie drops to 198.9 and 181.5 kN. So the preload can come down, and so does everything that follows from it; the hatch-open case has to be run at the new preload before we pick it.

## 5. Launch vibration: a first model that needs no data from SpaceX

Marco said vibration is the hard case and asked for a real model. This is the first rung of one, for the pane, done by hand so that the finite element run has something to be checked against.

- The pane is a 531 mm triangle of 21 mm glass, 5.7 kg. On rigid simple supports its first mode is about 985 Hz. On the two EPDM strips of the proposal clamp it also bounces as a whole at about 780 Hz. Together the first mode is near 600 Hz.
- With no spectrum from the launcher, the usual placeholder is NASA Goddard's general component level (GSFC-STD-7000, GEVS): 0.16 g squared per hertz from 50 to 800 Hz, 14.1 g rms overall, for qualification. It is meant for parts under 22.7 kg bolted to a spacecraft, and the standard lowers it for heavier items, so for a pane sitting on a 1.5 t panel it is an upper bound.
- Miles' equation then gives the pane's response at its own frequency. With a damping factor Q of 10, which is fair for a pane on rubber, it is 39 g rms, so 117 g at three sigma. With Q of 25 it is 186 g.
- At 117 g the pane pushes on its supports with 6.6 kN, the same as 54 kPa of pressure spread over it, and the glass sees about 3.5 MPa. At 186 g it is 10.4 kN, 85 kPa and 5.5 MPa. The cabin pressure itself is 81 kPa and gives 5.2 MPa by the same formula, so the glass is not the problem.
- The clamp is. The 6 November pane model clamps the pane with 9.1 kN at 0.3 mm of squeeze. That holds against 6.6 kN and does not hold against 10.4 kN. So the squeeze on the clamp strip is set by vibration, not by the steady launch load, and the damping of the strip decides whether 0.3 mm is enough.
- Noise acting directly on the pane is small. The Starship guide gives 137.7 dB overall in the payload bay, which is 153 Pa rms, against 81,000 Pa of cabin pressure. Noise matters through the panel it shakes, not through the pane.

What this model does not have is the panel. The pane rides on a 1.5 t ribbed panel stacked twenty deep for launch, and the panel's own modes decide what reaches the pane. That is the next rung: a modal run of one hexagon as packed, then a random response with the GEVS level at the stack supports. The first test a university lab can do is a tap test of one pane in its clamp, with an accelerometer, to measure the frequency and the damping. Those two numbers replace the 600 Hz and the Q of 10 above.

## 6. Hardware from McMaster for the test pieces

The test pieces do not need NAS bolts. At 4 kN the seam bolt is at a small fraction of any 5/16-24 bolt's strength, so what matters is its stiffness, and steel and A286 are the same stiffness to within one percent. An alloy steel 5/16-24 socket screw and nut from McMaster stands in for the NAS6705 in every test, with a note on the sheet. The M12 and M24 fixture screws are catalogue parts already. The flight parts list keeps the NAS numbers.

## 7. The hardpoint: what the check found

The independent check on 9 November found that our 8 November hardpoint solids were wrong, and recovering the real fitting from the October model showed it does not fit the 180 mm frame. That is set out on sheet RF-07 and in part 2, and it is question 5 for the call.

## What changes in the package

- Part 3 gets the squeeze table next to the tolerance table, and the McMaster note.
- Part 6 asks Marco to agree or disagree with four positions (plate not casting, 7050 for flight, the tolerance split, a jackbolt nut on the ties) and keeps three open questions.
- Part 5 gets launch vibration as its own item with the first numbers, and the clamp squeeze tied to it.
- The count of corner blocks is corrected to 180 wherever it said 60.

*Written 9 November 2026. Sources: Marco Cross's emails of 7 November; the HP1 and PR1 notes of 6 and 7 November; the parts solids of 8 November; GSFC-STD-7000 (GEVS) table 2.4-3 as reproduced by Vibration Research; the Starship Users Guide acoustic table; Nord-Lock's Superbolt MT dimension sheet. Plate properties are typical handbook values, not design allowables.*
