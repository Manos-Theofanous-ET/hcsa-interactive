# 6. Questions for Marco, in the order of the call

The call is 45 minutes, so the questions are in the order that matters most for making things, and the first two are the ones we most need answered. Each question says which sheet it is on.

## 1. The corner node (RF-08, and CB-01 in the parts library)

The block is a machined 2219 forging as drawn, 120 degrees on a hexagon and 108 on a pentagon, with four 7/8-14 tie holes per face, dowel holes and a landing for the main rib, 21.5 kg. After your email we put an R10 radius in every inside corner and R12 at the re-entrant corner at the vertex. The solid in the parts library is still drawn straight; the real joint face leans 20.9 degrees with the seam plane, so the real section is a parallelogram with the ties normal to the leaning face, and that is the next cut.

- Are those radii enough for an end mill, and which corners would you still change?
- Machined from a forging, or cast? If cast, which alloy, and what does that do to the 198 kN tie seat?
- The landing for the main rib leaves only 20 mm of metal to the joint face on the hexagon block and 16 mm on the pentagon block, and the first tie column had to move out to 136 mm from the vertex to clear it. Is a pocket that close to a sealing face something you would machine, or should the rib land on the block's cabin face instead?
- With the leaning face, the block is a wedge, 153 mm of lean over its 400 mm depth. Does that change forging against casting for you?
- The ties are tightened by measured stretch, because a torque wrench scatters about 25 percent and the hatch-open case leaves 0.7 kN. Is stretch measurement on a 7/8 Inconel tie something a crew can do in orbit, or should the ties be set on the ground and the seam design live with it?

## 2. The test pieces (TP-00 to TP-04)

- The tolerance table splits tight from normal. Is the split right, and is 0.10 over 150 mm and 0.15 over 550 the right flatness for a seal face?
- Material: the frames are 6061-T651 and the pull blocks 4140. Would you make the blocks in 6061 too, and if so, do the M12 threads need inserts? You suggested 7000-series for the frames; what would it buy on a test piece that is only pulled?
- Fixturing: how would you hold frame B to cut the glands and the joint face in one setting, so the glands are square to the face?
- The 40 mm bores at plus 0.10 and minus nothing, with 40 mm pins: ream, or bore, and is a dry-film lubricant on the pins enough against galling?
- Anything else that makes these cheaper or quicker. We are getting Xometry quotes this weekend and will have them on the call.

## 3. The hardpoint at the moved position (RF-07)

The model says the fitting has to sit on the line of the pull, at z' 46 to 106. The solid shows the bores clear the bolt row by 9.7 mm, but the 200 mm pad covers the two plain bolts beside the fitting, so their nuts would sit under it. The ways out are to move those two bolts along the seam into the web beside the block, make the fitting shorter, or drop them and let the fitting clamp the seals there; drawing them deeper is out, because the seam model says the seal opens as the bolts move away from it.

- Can two titanium fitting halves with three 40 mm pins each be made and fitted the way we draw them, and what would you change?
- Which of the three ways out would you take?
- The fitting's own fixing bolts, two pairs at the ends and one between each pair of bores, are in tension under the seam pull. Is that a fixing you would accept, or should the fitting be captive in the block?
- Every hardpoint as drawn is about 20 kg of blocks, fitting halves and pins, so the 270 of them are 5.3 t. Where would you take that weight out: fewer pins, a shorter pin, or fewer hardpoints?

## 4. The forces you called achievable but unreasonable

198 kN in each corner tie, 4 kN in each seam bolt, about 109 kN per atmosphere through each hardpoint, and a 0.2 mm tolerance on the 2,250 mm edge of a panel.

- Which of these would you attack first, and how? Our own order is the edge tolerance, then the ties.

## 5. Launch vibration (RF-01, PR1 in part 4)

You said launch is the hard case for the panes, not pressure. The pane model at launch ran with a clamp and holds with room, and the clamp force comes from tightening. We do not have SpaceX's spectrum.

- How would you set up the model and the test without it? Which published envelope would you use as a placeholder, and which test does a university lab do first?

## 6. If there is time

- The pentagon closure plate: which side of the frame, and fixed how (RF-09, Q57).
- The cold soak: there is no chamber for the 550 article at minus 40 degrees. What is the cheapest way to get one seam piece cold in the 100 kN frame?
- The pass leak rate for the 550 article, and how a shop would pressure test a seam of this kind.
- The seal loop corners at R16, which have to be solved in the corner block (RF-02, Q92).
