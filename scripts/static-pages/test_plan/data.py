# -*- coding: utf-8 -*-
"""Content of the HCSA physical test plan (13 Nov 2026).

Every number here comes from one of these, named in SOURCES below:
the 10 Nov test budget sheet (prices, suppliers, statuses), the 23 Oct
fabrication and testing plan (methods), the Rev F release package parts 3, 4
and 5 (geometry, model results, open items), Marco's points of 9 Nov, and the
mail threads named in NEW_SINCE. Nothing is a new estimate.

Status keys used in the parts lists:
  have      in hand
  agreed    donation or loan agreed, not here yet
  offered   offered, nothing agreed or received
  free      free inside a class or the lab
  buy       has to be bought (unfunded today)
  quote     quote asked, not answered
  notpriced needed, no price yet
  later     needed only for a later test
  optional  useful, not required
  counted   counted under another test
"""

DATE = "13 November 2026"

STATUS = {
    "have": ("In hand", "ok"),
    "agreed": ("Agreed, not here yet", "loan"),
    "offered": ("Offered", "loan"),
    "free": ("Free in class", "ok"),
    "buy": ("Need to buy", "buy"),
    "quote": ("Quote pending", "pend"),
    "notpriced": ("Not priced yet", "pend"),
    "later": ("Later", "muted"),
    "optional": ("Optional", "muted"),
    "counted": ("Counted elsewhere", "muted"),
}

BASELINE = [
    ("Seam", "two butyl BA500 loops (5.33 mm cord) in 7.1 x 4.0 mm glands at z' 18 and 32, RTV566 bead at z' 42"),
    ("Seam bolt", "NAS6705U27 at 4 kN, one row at z' 58, 75 mm pitch; McMaster 5/16-24 alloy steel stand-ins in the test pieces"),
    ("Edge frame", "180 mm deep, 6061-T651 in every test piece"),
    ("Pressure", "cabin 0.8 atm; design 12.3 psia; proof 1.26 atm; ultimate 1.67 atm"),
    ("Seal requirement", "gap between the two cords no more than 0.11 mm up to 1.93 atm"),
    ("Glass", "21 mm BOROFLOAT 33, 531 mm panes; passes if the Weibull m is at least 7.0 on our route, 7.7 NASA-style"),
]

RULES = [
    "Every physical test is done on the computer first. Before it runs, its computer twin files a prediction for every gauge.",
    "A test passes when the measurement lands within 10 percent of the prediction at the first hold point. If it misses, we change the model, never the data. (Whether Prof. Henann reviews the plan and the 10 percent rule is still open, Q50.)",
    "Nothing is machined until its drawings are checked and released (Q55) and the money is there. The budget today is $0, so every line marked Need to buy is unfunded.",
]

# --------------------------------------------------------------------------
TESTS = [
# ==========================================================================
dict(
    id="t0", code="T0", name="Glass bars in four-point bending",
    when="Spring 2027 in ENGN 1440, or now on the 0.5 kN frame (Rick to decide, Q42)",
    state="Waiting on bars and the now-or-spring decision", state_cls="pend",
    anim_caption="A bar on two supports, pressed by two pins until it breaks. Each break gives one strength and one fracture origin; thirty or more breaks give the Weibull slope m. The points on the plot are an example, not data.",
    what=[
        "How strong our pane glass is when it is finished the way the panes will be: BOROFLOAT 33 with fine-ground edges and an arris (a small bevel).",
        "Two numbers come out: the characteristic strength and the Weibull modulus m, which says how much the strength scatters from piece to piece.",
        "Where each break starts, on the face or at the edge, because the pane edge sits on the seat and edge flaws are part of the glass chain.",
    ],
    how=[
        "Bars 1 x 1/8 inch (25.4 x 3.2 mm) sit on two supports and two loading pins press down between them, the ENGN 1440 four-point method.",
        "Each bar is loaded at a fixed stress rate until it breaks. Tape on the tension face keeps the pieces in place so the origin can be found.",
        "30 or more valid breaks per condition (ASTM C1239). Proposed conditions: the as-delivered edge, a second bar length for the size check, and a set of 20 bars broken at four stress rates for slow crack growth (ASTM C1368). That is 100 or more bars.",
        "We use the fine fixture: the standard EN 1288 fixture over-stresses the bar at its loading pin by 7.4 percent, so breaks would start at the pin.",
        "On the 0.5 kN frame, supports 80 mm apart and pins 40 mm apart reach 117 MPa at the frame's limit; if the bars are strong we order 150 mm bars for spans of 120 and 60 mm.",
    ],
    record=[
        "Load and crosshead movement for every bar, from the frame",
        "The break load, turned into stress with the measured bar width, thickness and spans",
        "The arris size on every bar (a 1 mm arris on a 3.2 mm bar reads 4.5 percent strong)",
        "The fracture origin: face or edge, found by eye, optical microscope, or the Brown SEM",
        "The stress rate of each bar; on a few bars, one or two strain gauges to check the spans and the formula",
    ],
    tells=[
        "m and the characteristic strength of our glass as it will be finished, and its edge strength.",
        "Whether the strength scales with size the way the Weibull fit says, by comparing the two bar lengths.",
        "The 21 mm pane at 0.8 atm needs m of at least 7.0 on our route and 7.7 NASA-style (7.9 and 8.8 with the hatch open). The only large-area float data has m near 6. If T0 finds m near 6, the 425 mm fallback panes become the design; a high m opens the 708 mm upside.",
        "It does not give the strength of a 531 mm pane directly (that comes from statistical scaling), and says nothing about tempered or laminated glass or years of thermal cycling.",
    ],
    why=[
        "Bars, not discs: the ring-on-ring fixture for discs would cost thousands of dollars to set up and the small frame is 0.5 kN, not the 5 to 10 kN we had assumed (Jerry Zani, 14 Oct).",
        "Bars in the ENGN 1440 size use the class's own fixture and method, so the test can run in Prof. Padture's class at no cost.",
        "30 breaks per condition is the minimum ASTM C1239 asks for a Weibull fit; fewer and m is too uncertain to size a pane.",
        "Two lengths, because glass strength depends on how much area is stressed, and we have to scale from a 25 mm bar to a 531 mm pane.",
    ],
    passes=[
        "A fit from 30 or more breaks per condition, with m and the characteristic strength for each finish",
        "The second bar length lands inside the size prediction of the first",
        "The predicted strength of the pane at a one-in-ten-thousand failure probability is above the stress the pane sees (the pass lines are being rerun for bars and the Rev F pane)",
    ],
    parts=[
        ("BOROFLOAT 33 bars, 1 x 1/8 in, fine-ground edges with arris", "100+", "Swift Glass (quote); PGO asked", "buy", 1040,
         "Swift quote about $1,000 plus UPS up to $40, valid to the end of 2026. Free if ENGN 1440 has spare bars (McMaster 8476K12): ask Prof. Padture on 18 Nov"),
        ("Four-point bend fixture and frame time", "1", "ENGN 1440 (Prof. Padture)", "free", 0,
         "$0 if run inside ENGN 1440 in spring 2027; to confirm on 18 Nov"),
        ("SEM time to find fracture origins", "about 4 h", "Brown SEM facility", "optional", 384,
         "$59 an hour plus 2 h training at $74 an hour; reduced rate asked 9 Oct; an optical microscope may be enough"),
        ("BOROFLOAT 33 discs, 50 x 3.3 mm (reference set)", "15", "Precision Glass & Optics, donated", "have", 375,
         "In hand since 13 Oct. No disc fixture, so reference only"),
        ("Sapphire discs, 60 x 5 mm (reference set)", "15", "Meller Optics, donated", "have", 2595,
         "In hand since 13 Oct; flatness not checked"),
        ("BOROFLOAT 33 discs", "60", "SCHOTT", "offered", 1500,
         "Offered; nothing has arrived"),
    ],
    have=[
        "A route to the fixture and frame: ENGN 1440, to confirm with Prof. Padture on 18 Nov at 11:30",
        "A written quote for the bars from Swift Glass, valid to the end of 2026",
        "Reference discs in hand (15 BOROFLOAT, 15 sapphire), not needed for the bar test",
    ],
    need=[
        "The decision: bars now on the 0.5 kN frame, or in ENGN 1440 in the spring (Rick, Q42)",
        "The bars: $1,040 from Swift, or spare bars from the class",
        "The test-bar drawing with the arris size, agreed with Swift (Q04), and the count and the two lengths (Q51)",
        "The pass lines rerun for bars and the Rev F pane (the old ones were written for discs)",
    ],
),
# ==========================================================================
dict(
    id="t1", code="T1", name="Seam slices, 75, 150 and 225 mm, pulled apart",
    when="Late January to February 2027, in the first Dewesoft loan batch (dates set in late November)",
    state="Drawn (TP-00 to TP-04, STEP files); not checked, not ordered", state_cls="pend",
    anim_caption="A full-size cut through the seam: frame A on the left, frame B with the two cords and the silicone bead on the right, one bolt between them. Run 1 pulls straight, run 2 pries the joint open the way cabin pressure does. Gaps are drawn about 150 times too big so they can be seen.",
    what=[
        "Whether the Rev F seam keeps its seal while it is loaded: the two butyl cords, the RTV566 bead and the bolt, at full size.",
        "The load in the bolt against the pull, the stiffness of one bolt station, and the gap between the cords at which air starts to get past.",
        "Whether one short slice speaks for the whole seam: the response per bolt has to be the same at 150 and 225 mm.",
    ],
    how=[
        "Each slice is two frames, A flat and B with the two glands, face to face, 180 mm deep, with the bolt row at z' 58. The cords go in, the bead is laid and cured, end dams close the cut ends, and the bolts go to the 4 kN design preload.",
        "Steel pull blocks, 160 mm tall, bolt into the legs of each frame with M12 screws from both faces.",
        "Run 1, the straight pull: an M24 rod through the block centre at z 90. Run 2, the prying pull: through a lug, fork and pin on the z 24 line near the outer flange, so the joint opens about its cabin-side edge the way pressure opens it (sheet RE-03 rev B).",
        "Air in the space between the two cords, read at the leak port while the load is held. Each slice gets the two runs that do not break it, then one ramp to failure.",
        "Load scale at Rev F: a plain-bay bolt carries 1.29 kN per atm in the station model, the worst bay 2.67 kN per bolt, and the seam model reaches the 0.11 mm gap at 3.75 kN per bolt, about 2.9 atm. So the holds are a few kN per bolt, far inside the 50 kN fixture and the 100 kN Instron. The hold-point table is being restated against 12.3 psia (owed); the October table of 41.5 kN per atm was the old upper bound and is withdrawn.",
    ],
    record=[
        "Load and crosshead from the Instron (analog out, on the same clock as everything else)",
        "Stroke from block to block (LVDT, 25 mm)",
        "The gap across the joint at the outer face and at the cabin face (two gap gauges, 0 to about 2 mm)",
        "The bolt load (internally gauged bolts)",
        "About 10 strain gauges on the 20 mm web near the bolts and at the leg roots (TML rosettes and single gauges)",
        "The air pressure between the cords at the M5 port, and the room temperature",
        "100 samples a second during the holds, 1,000 or more on the failure ramp; about 16 channels on the Dewesoft recorder",
    ],
    tells=[
        "Whether the seal holds under a real prying load, and the gap at which it stops holding. Today 0.11 mm is a requirement, not a measurement.",
        "The bolt load against the pull, and the stiffness of a bolt station, which goes back into the station model.",
        "What the cut ends and end dams do, by comparing the three lengths.",
        "It does not cover the corner (T3), shear along the seam, bending across the angle between panels, or thermal cycling.",
    ],
    why=[
        "Bolts, cords and glands do not scale down, so the seam is tested at full size. A whole seam is far too big for a lab frame; a slice is not.",
        "Three lengths: one bolt shows the bolt and the seal, two add the bending of the web between bolts, three give a middle bolt that sees two neighbours, like every bolt in a real seam. The October seam model put the 150 mm and long-seam bolts within 0.23 percent of each other; the test checks it at Rev F.",
        "Run 2 pries rather than pulls straight because the seam model shows pressure opens the seam by rotating it about its cabin-side edge from the first newton. Run 1 is the simple control; whether it stays in the plan is open.",
        "Prof. Henann's rule: a joint that does not break at the bolt cannot be trusted to the model alone and has to be pulled.",
    ],
    passes=[
        "At the worst-bay hold, the gap between the cords stays under 0.11 mm and the port pressure holds",
        "Above that, the readings follow the seam model within 10 percent",
        "The response per bolt is the same at 150 and 225 mm",
        "Nothing yields below the proof load (1.26 atm equivalent)",
        "We record the gap at which the port pressure starts to fall. (These lines are restated against 12.3 psia with the model rerun.)",
    ],
    parts=[
        ("Frame A with grip legs, 75, 150 and 225 mm (6061-T651)", "3", "Xometry, from the Rev F STEP pack", "buy", 2663,
         "5 Oct estimate for the old 140 mm frame: $1,005 plate + 19.5 h shop. The Rev F frame is 180 mm deep, so expect more; the quote replaces this"),
        ("Frame B with the two glands, RTV recess and leak port (6061-T651)", "3", "Xometry", "buy", 3045,
         "5 Oct estimate: $1,005 plate + 24 h shop"),
        ("Pull blocks, 160 tall, M24 thread (4140 Q&T 28-32 HRC)", "6", "Xometry or the Brown shop", "buy", 2020,
         "MSP Metals bar at $28.24 an inch + 12 h shop; estimate made before the blocks grew to 160 mm"),
        ("Lug plate, fork and pin for run 2, F-01 to F-03 (4140 Q&T)", "1 set", "Xometry or the Brown shop", "notpriced", None,
         "New with sheet RE-03 rev B; shared with the 550 article"),
        ("End dams, rubber faced (2 go to the 550 article)", "8", "Brown shop", "buy", 395,
         "6061 plate 1/2 in + EPDM; OnlineMetals list + 2 h shop"),
        ("Seam bolts 5/16-24 with nuts and washers, 2 gauged per slice", "20", "McMaster stand-ins (Marco, 9 Nov); Bossard and Cherry asked for A286", "buy", 328,
         "$328 is the A286 estimate and an upper bound for the McMaster stand-ins, which are not priced yet. The gauged bolts are not priced"),
        ("M12 class 12.9 leg screws", "60", "Bolt Depot, donated", "have", 100,
         "Arrived 14 Oct"),
        ("M8 threaded rod for the end dams", "2 m", "Bolt Depot", "buy", 23,
         "Bolt Depot 23774"),
        ("Butyl cord, Parker BA500-70, 0.210 in, two loops", "about 13 ft", "Sandem / Sealing Specialties (asked)", "quote", 59,
         "Estimate $4.50 a foot; may come as free samples"),
        ("RTV566 kit + SS4155 primer", "1", "SkyGeek list; Momentive sample asked 3 Nov (no reply)", "buy", 1192,
         "$1,063.93 + $127.84, an upper bound; a Momentive sample would make it $0"),
        ("M5 leak-port fitting, 0-60 psi gauge, tubing", "1", "Swagelok Boston (asked)", "buy", 120,
         "Estimate"),
        ("Strain gauges: 15 FRAB rosettes + 15 FLAB singles", "30", "TML, donated", "agreed", 0,
         "Confirmed 4 Nov. TML ship about 4 weeks after we confirm the lead wire (they suggest 5 m); our reply is still in Drafts. Covers T1 only"),
        ("LVDTs, 25 mm stroke (Trans-Tek 0243-00000-40)", "2", "Trans-Tek", "buy", 750,
         "$375 each (list $535); they cannot hold them and want payment in advance; our reply is in Drafts"),
        ("Gap gauges across the joint (clip gauges or LVDTs, 0-2 mm)", "2", "Dewesoft asked whether they lend sensors", "notpriced", None,
         "Not a separate line in the budget yet"),
        ("Instron 5882 time, 100 kN (BH 092)", "30 h", "Brown, Jerry Zani", "buy", 1380,
         "$46 an hour is a placeholder; the Brown rate is unknown. Ask Jerry whether student projects are charged"),
        ("Instron adapters (M24 to the frame) and a safety shield", "1 set", "Brown shop; Exolon, Curbell and Piedmont asked for polycarbonate", "notpriced", None,
         "The adapters cannot be drawn until the three frame interfaces are measured with Jerry (Q21). Shield requests out since 29 Oct, no replies"),
        ("Data recorder, 16 channels (Dewesoft SIRIUS or KRYPTON)", "1", "Dewesoft, on loan", "agreed", 4076,
         "Loan agreed in principle; batch dates set in late November. $4,076 if bought"),
    ],
    have=[
        "Drawings TP-00 to TP-04 and the STEP files for every piece (not yet checked or released, Q55; Marco reviews them on 17 Nov)",
        "60 M12 leg screws",
        "30 TML strain gauges agreed (they ship once we confirm the lead wire)",
        "The Dewesoft recorder agreed in principle",
        "The Instron, free from 18 Nov",
        "The seam model's prediction to compare against (D1, 5 Nov)",
    ],
    need=[
        "Money for the machined parts, then quotes (Xometry from the STEP pack; PCBWay if the sponsorship comes through)",
        "Cord, RTV and primer, the leak-port fitting, the LVDTs, the gap gauges",
        "The Instron rate and the three frame interfaces measured with Jerry, then the adapters drawn and made",
        "A safety shield",
        "The hold points and pass lines restated against 12.3 psia, and the seam model's prediction filed for each gauge",
        "A decision on whether run 1 stays in the plan",
    ],
),
# ==========================================================================
dict(
    id="t550", code="SA-550", name="The 550 mm joint article: squeeze, leak and the sealing gap",
    when="Leak test January 2027 (December only if machining starts by mid-November); the prying pull goes in the Dewesoft batch",
    state="Drawn (TP-03, moved fitting agreed 10 Nov); not ordered", state_cls="pend",
    anim_caption="The joint seen face on, 550 mm long: two cords along the length, the silicone bead, two seam bolts each side of a dummy hardpoint. It is tightened, sealed, pressurised between the cords, shimmed, then pried open while the leak is read against the gap.",
    what=[
        "That a straight run of the seam goes together to the drawing.",
        "The squeeze on the cords against bolt torque, and the leak rate between the cords with no load on the joint.",
        "The smallest squeeze that still seals, using shims of 0.1 and 0.2 mm under one face.",
        "The gap at which butyl stops sealing, by prying the article open while the leak is read. This is the number the whole seal design turns on.",
    ],
    how=[
        "SA-550 moved: a 550 mm seam with a dummy hardpoint on the line of the pull (z' 46 to 106), three 40 mm pins at 60 mm pitch in a 200 mm block, and two seam bolts each side. The pins are loose by design, so the seam bolts and the seals carry the load.",
        "Dry fit first, no cord: the faces must touch along the whole length (0.05 mm feeler) and the holes must line up.",
        "Cords in, bolts tightened from the middle out in small steps; at each step the face gap is read at three stations and the inner gap with a dial gauge, which gives squeeze against torque.",
        "Bead laid and cured 24 hours, end dams fitted. Air at 1 atm into the space between the cords through the port, closed off, decay logged for an hour; then 2 atm; then each cord alone by venting one side.",
        "The same with a 0.1 mm and then a 0.2 mm shim under one face. Then the article is pulled in prying through the lugs while the leak is read against the gap. Afterwards it stays assembled as the ageing sample.",
    ],
    record=[
        "Bolt torque at each step; the face gap at three stations (feeler); the inner gap (dial gauge)",
        "Pressure between the cords (transducer 0-200 kPa, as fine as possible) over each hour-long hold",
        "Room air and part temperature, because the decay is sensitive to about 1 degree C",
        "During the prying pull: load, the gap across the joint, and the port pressure, giving leak against gap",
    ],
    tells=[
        "The torque that gives the design squeeze, which every later assembly uses.",
        "Whether three seals in a row hold with no load, and the baseline leak rate to compare the loaded slices with.",
        "The minimum squeeze that still seals, which settles how tight the gland depth and the face flatness must be (Marco's tolerance point).",
        "The real sealing gap, to set against the 0.11 mm requirement.",
        "It does not say anything about the corner, or about temperature (that is the cold soak).",
    ],
    why=[
        "Leak rate is in no model: it depends on surface finish, the ends of the glands and the end dams. It has to be measured.",
        "One article with shims gives several squeezes, instead of machining several articles.",
        "The fitting is moved onto the line of the pull because, where it was drawn, the frames hinge about it and the seals open at 0.2 to 0.5 atm; Rick agreed the move on 10 Nov.",
        "550 mm is long enough to show whether a straight run goes together and seals, and it carries a dummy hardpoint, as the station seams do.",
    ],
    passes=[
        "It goes together to the drawing: faces touch along 550 mm, holes line up",
        "The squeeze is in the design band (25 percent nominal; at least 16 percent in the worst tolerance stack)",
        "The pressure between the cords holds at 1 and 2 atm with a decay below the agreed rate, and each cord holds on its own. The rate is not set yet: a question for Marco on 17 Nov. Parker's reference for butyl is about 9e-7 cc/s per inch of helium at 15 percent squeeze",
    ],
    parts=[
        ("Frame A, 550 mm, with legs (6061-T651)", "1", "Xometry", "buy", 805,
         "5 Oct estimate ($295 plate + 6 h shop); the rev B legs are not in it"),
        ("Frame B, 550 mm, grooved, with the hardpoint block (6061-T651)", "1", "Xometry", "buy", 933,
         "5 Oct estimate ($295 plate + 7.5 h shop); the dummy hardpoint is not in it"),
        ("Dummy hardpoint: three 40 mm pins", "3", "Brown shop or Xometry", "notpriced", None, "On sheet TP-03"),
        ("Pull blocks, 160 x 80 x 550 (4140, 55 kg each; or 6061-T651, 19 kg each)", "2", "Xometry or the Brown shop", "notpriced", None,
         "Not in the 10 Nov budget"),
        ("Lug plate, fork and pin, F-01 to F-03", "1 set", "Shared with T1", "counted", None, "Counted under T1"),
        ("Bolts, cord, RTV, 2 end dams", "-", "From the T1 batch", "counted", 0, "Counted under T1"),
        ("Shim stock, 0.1 and 0.2 mm", "2", "McMaster", "notpriced", None, "Small; not priced"),
        ("Pressure transducer 0-200 kPa + 2 temperature sensors", "1", "Dewesoft loan, or the Dwyer 626 shared with T2", "agreed", 0,
         "The Dwyer 626 is $305 if bought (counted in T2)"),
        ("Torque wrench, feeler gauges, dial gauge", "1 each", "To borrow (Brown shop or lab): not asked yet", "notpriced", None, "Not in the budget"),
    ],
    have=[
        "Sheet TP-03 with both fitting positions and the STEP files; the moved position agreed on 10 Nov",
        "The pressure transducer through the Dewesoft loan (agreed in principle)",
    ],
    need=[
        "Money and the machining (it comes off the machine first, with the T1 batch)",
        "The pull blocks and the dummy pins priced and made",
        "Cord, RTV, the port fitting (from T1)",
        "The pass leak rate, agreed with Marco",
        "The model rerun with the drawn bolt positions, to predict the pull at which the gap reaches 0.11 mm (D1-550, owed)",
        "Tools to borrow: torque wrench, feelers, dial gauge",
    ],
),
# ==========================================================================
dict(
    id="t2", code="T2", name="Quarter-scale panel under water pressure",
    when="February to March 2027; needs its own funding (Champlin, $19,885 asked for the water rig)",
    state="To be redrawn at Rev F; no host yet", state_cls="buy",
    anim_caption="A hexagon panel at quarter scale sits on a rubber membrane over water in a steel tub. The water pressure goes up in steps, first with the edge free to turn, then clamped. The dial on the hub and the strain gauges are read at every step. Shapes are from the 5 Oct article; the Rev F article is still to be drawn.",
    what=[
        "How the panel structure carries pressure: the stress in the ribs, how far the hub drops, the frame web near a corner and the pane centres.",
        "How stiff the edge support really is. Our two solvers disagree by 30 to 40 percent on the hub drop with a pinned edge; the dial on the hub picks between them.",
    ],
    how=[
        "One hexagon panel at 1:4, with aluminium panes that match the stiffness of the glass at that scale, sits cabin side down on a 1 mm EPDM membrane over water in a welded steel tub.",
        "First with the edge pinned (round bars under the top ring let it turn), then clamped, because the real seat is somewhere between the two.",
        "The relief valve is checked before the panel sees pressure. The pressure goes up in steps and back down, three times for each edge, then in small steps to 2 atm with everyone behind the screen. The October steps were 0.25 atm to 1 atm; they are restated against 12.3 psia when the article is redrawn.",
        "Water, not air: 165 litres of water at 2 atm stores about 1.5 joules; the same volume of air stores about 34 kilojoules.",
    ],
    record=[
        "About 8 strain rosettes and 6 single gauges (pane centres on both faces, the rib flanges, the frame web), about 30 channels",
        "Hub drop and frame movement with 4 LVDTs or dial gauges read against a bridge clamped to the panel frame, so movement of the rig drops out",
        "Water pressure (0-300 kPa) and water temperature, 10 to 50 samples a second",
    ],
    tells=[
        "The rib stress, hub drop and frame web stress at the edge condition that matches, and the stiffness of the edge support, which goes into both models.",
        "Whether the membrane rig works.",
        "Nothing about glass (the panes are aluminium), the seam (the frame bolts to a rig, not to a neighbour), temperature or vacuum, or the full-size pane seat, because the rubber strips do not scale.",
    ],
    why=[
        "At 1:4 every length scales, so at the same pressure the stresses match full size, and a panel fits a lab. Glass strength does not scale, which is why T0 exists and the panes here are aluminium.",
        "Pinned and clamped bracket the real seat, so the test brackets the model's answer.",
        "Water for safety, as above.",
    ],
    passes=[
        "Linear and repeatable over three cycles, no permanent set, no membrane leak",
        "The model within 10 percent at the matching edge condition",
        "The October gauge-by-gauge lines (pane centre 50 to 65 MPa per atm; hub 0.6 to 1.0 mm per atm pinned, 0.55 to 0.65 clamped; rib flange 10 to 25 MPa per atm) are for the 5 Oct article and are rerun for Rev F",
    ],
    parts=[
        ("Panes, 6061 sheet 5/16 in", "1 sheet", "SendCutSend or Derecktor; OSH Cut student discount", "buy", 835, "5 Oct list; to redraw for Rev F"),
        ("Six T ribs (section provisional)", "6", "CNC shop or Brown shop", "buy", 2453, "5 Oct list"),
        ("Six frame bars with corner plates", "6", "CNC shop", "buy", 2397, "5 Oct list"),
        ("Hub", "1", "Brown shop", "buy", 195, "5 Oct list"),
        ("Neoprene setting strips", "30 ft", "OnlineMetals; Rogers asked", "buy", 58, "5 Oct list"),
        ("Retaining beads with M4 screws", "18", "Brown shop", "buy", 235, "5 Oct list"),
        ("Tub walls, A36 1/2 in", "6", "Derecktor (asked)", "buy", 853, "5 Oct list"),
        ("Tub floor, A36 1 in", "1", "Derecktor (asked)", "buy", 1629, "5 Oct list"),
        ("Flange and top rings, welded", "2", "A welding shop, still to find", "buy", 1800, "5 Oct list; the tie-bolt circle has to move in first"),
        ("Membrane clamp ring", "1", "Welding shop", "buy", 390, "5 Oct list"),
        ("Welding the tub and rings", "-", "Welding shop; B E Peterson will review build and hydrotest once there is a budget", "buy", 1400, "14 h"),
        ("EPDM membrane + spare", "2", "Rubber-Cal or Home Depot", "buy", 43, ""),
        ("M16 tie bolts, nuts, washers", "30", "Bolt Depot", "buy", 129, "Check whether the Bolt Depot donation covers them"),
        ("Round bars for the pinned edge", "6", "Brown shop", "buy", 40, ""),
        ("Relief valve, 220 kPa", "1", "Swagelok Boston or IMS Supply", "buy", 431, "SS-RL3M4-S4; a $7.95 brass valve is the budget fallback"),
        ("Pressure transducer 0-50 psi (Dwyer 626)", "1", "JME", "buy", 305, ""),
        ("Fill, bleed and drain fittings, hand pump", "1", "Swagelok Boston and a hardware store", "buy", 150, "Estimate"),
        ("Strain rosettes, gauges, adhesive", "about 14", "TML (asked once the gauge map is settled), Micro-Measurements or HBK", "buy", 643, "TML's donation covers T1 only so far"),
        ("Dial indicators, bases, bridge", "2", "Mitutoyo 2416S, Fowler bases", "buy", 507, ""),
        ("Data recorder", "1", "Dewesoft, on loan", "agreed", 4076, "The same loan as T1, in a later batch"),
        ("Host site and the hydro proof of the tub", "-", "NUWC, Element or B E Peterson (asked)", "notpriced", None, "Where 700 kg at 2 atm can be tested, and who signs off safety at Brown (Q45)"),
    ],
    have=[
        "The October design of the rig and article (Breuer package, 21 Oct) to start the redraw from",
        "The Dewesoft recorder, agreed in principle",
    ],
    need=[
        "The 1:4 article redrawn on the Rev F grid with option B ribs, and the tie-bolt circle moved in",
        "A host and a safety sign-off (Q45), and a budget for B E Peterson (Q46)",
        "Funding (Champlin)",
        "The gauge map, then the gauges",
        "The model rerun on the Rev F article",
        "A written test plan, video and a process watcher (Marco)",
    ],
),
# ==========================================================================
dict(
    id="t3", code="T3", name="One corner, where three panels meet",
    when="Not before late 2027, and only after T1 and T2 agree with their models",
    state="Later; not drawn as a test article at Rev F", state_cls="muted",
    anim_caption="Seen from outside: three seam stubs meet at a corner and are pulled apart along their seats, the way the panels load the corner. The ties through the corner blocks and the opening of the corner faces are watched against their limits.",
    what=[
        "Whether the corner opens at the end of the cord when the seams pull on it the right way, and whether the corner seal holds.",
        "The force in the corner ties, the bolt force at the first station of each seam, how the load splits between the three seams, and how stiff the node is. All 60 corners are hexagon-hexagon-pentagon, so one article covers the station.",
    ],
    how=[
        "Three seam stubs meet at the vertex and are pulled apart along their seats, at the angles between the panels, never by gripping the stub ends (an end pull loads the end bolt and leaves the corner unloaded).",
        "That needs three actuators, or a fixture that reacts two of the pulls.",
        "The ties are set by measured stretch, not torque (a multi-jackbolt nut and an ultrasonic gauge are proposed). The corner is pressurised between the seals and held at stepped loads.",
    ],
    record=[
        "The gap at the vertex on both faces and at the cord end",
        "Strain on both rows of ties, and on the frame ends in the first 60 mm",
        "The bolt force at the first station of each seam",
        "The leak at the corner",
    ],
    tells=[
        "Whether the corner model holds: at 0.8 atm it puts the worst tie at 214.5 kN at proof against a 227 kN limit, and the faces open 0.55 mm against the 0.8 mm the corner seal is sized for.",
        "Whether the tie preload can come down (runs at 180 and 160 kN are on the laptop now).",
    ],
    why=[
        "The corner is where the model is least sure: its block stress has no limit set yet, and its seal (O10) is not designed.",
        "It waits for T1 and T2 because they prove the seam and the panel it is made of.",
    ],
    passes=[
        "The ties and the face opening within 10 percent of the corner model, and under their limits",
        "The corner seal holds",
        "The pass lines are written with the spring test plan",
    ],
    parts=[
        ("Corner article: blocks, stubs, ties, seal and rig (6061, Inconel 718 ties)", "1 set", "Not chosen", "later", 4785,
         "5 Oct estimate ($2,745 parts + 24 h shop, including a $1,500 rig); made before the Rev F corner node (80 kg, machined from plate)"),
    ],
    have=[
        "The corner model at Rev F (C1, 5 Nov) and the corner block drawn (CB-01)",
    ],
    need=[
        "The corner seal (O10) designed, and the seal loop corners solved in the corner block (Q92)",
        "A stress limit for the block",
        "The tie tightening method agreed (Marco)",
        "A three-pull rig",
        "T1 and T2 passed",
    ],
),
]

# Proposed tests that are not yet in the plan, so no parts list is priced.
PROPOSED = [
dict(
    id="tap", code="Tap", name="Tap test of one pane in its clamp",
    when="Proposed for the 17 Nov call with Marco",
    state="Proposed", state_cls="muted",
    anim_caption="A small hammer taps the clamped pane; an accelerometer records the ring. How fast it rings gives the first mode, and how fast the ring dies away gives the damping.",
    what=["The first natural frequency of a pane in its clamp and the damping of the rubber strip."],
    how=["Tap the pane with an instrumented hammer and read an accelerometer glued to it; repeat at a few points."],
    record=["The hammer force and the acceleration against time, then the frequency spectrum"],
    tells=["Two numbers that replace the guesses in the launch vibration hand model: about 600 Hz and a damping factor Q of 10. With the NASA general spectrum the clamp sees 6.6 to 10.4 kN against the 9.1 kN it holds, so the damping decides whether the 0.3 mm squeeze is enough."],
    why=["It is the cheapest launch-vibration test a university lab can do, and it needs no launcher data."],
    needs="A pane (or a stand-in of the same glass and size), the clamp, a hammer and an accelerometer. Not priced; to agree with Marco.",
),
dict(
    id="cold", code="Cold", name="Cold soak of the 550 article to minus 40 C",
    when="Not scheduled: there is no chamber",
    state="Proposed", state_cls="muted",
    anim_caption="The assembled 550 article goes into a dry-ice box with the port line brought out. As it cools, the bolt load and the pressure between the cords are read.",
    what=["Whether the seal holds at the cold end, with the bolt load as predicted."],
    how=["A dry-ice cold box around the 550 article (proposal), port line brought out; read through the cool-down and back."],
    record=["Bolt strain, the port pressure, the gap across the joint, part and air temperature"],
    tells=["Whether the cold limit is set by the rubber, not by the squeeze."],
    why=["Butyl hardens in the cold; the squeeze model says the squeeze holds, so the rubber is the question."],
    needs="A chamber or a dry-ice box, and the cold model (D6) rerun with butyl before a prediction is filed.",
),
]

NEW_SINCE = [
    ("SendCutSend", "11 Nov: $500 of cutting services through their STEM programme, as a gift code that does not expire. Not used yet. It could pay for cut plate parts, for example the end dams or the T2 panes."),
    ("TML", "4 Nov: 15 rosettes and 15 single gauges donated, for T1 only. They ship about 4 weeks after we confirm the lead wire length (they suggest 5 m). Our reply is still in Drafts."),
    ("Trans-Tek", "3 Nov: the two LVDTs at $375 each cannot be held, and Brown would have to pay in advance. Our reply is in Drafts."),
    ("Parker", "2-3 Nov: the cord needs about 22 lb per inch at 25 percent squeeze (their FEA), and a non-circular groove wants an inside corner radius of at least three times the cord, ideally six."),
    ("Marco", "7-9 Nov: McMaster 5/16-24 alloy steel bolts stand in for the NAS6705 in every test piece; the flight parts list keeps the NAS numbers."),
    ("Rick", "10 Nov: the moved hardpoint agreed, so SA-550 moved is the article we make."),
    ("New parts with no price yet", "the run 2 lug, fork and pin (F-01 to F-03), the two 550 pull blocks, the dummy pins, shims, the gap gauges, the Instron adapters and shield. The frames grew from 140 to 180 mm deep after the October estimates, so the machining lines will go up."),
]

DATES = [
    ("15 Nov", "PCBWay sponsorship application due"),
    ("17 Nov, 10:00", "Fabrication review with Marco Cross (Zoom): the drawings, the tolerances, the leak pass rate"),
    ("17 Nov, 12:00", "Weekly meeting with Rick; still open with him: glass bars now or in spring (Q42), endorsements"),
    ("18 Nov, 11:30", "Prof. Padture: bars in ENGN 1440, spare bars, the fixture"),
    ("22 Nov", "Spring test plan due"),
    ("Late Nov", "Dewesoft loan dates and units"),
    ("About 1 Dec", "Thornton Tomasetti proposal to the foundation through OSP (about $14,700, all test hardware)"),
    ("11 Dec", "Fall report due"),
]

FUNDING = [
    ("Thornton Tomasetti Foundation", "about $14,700 for test hardware; package with Kelly da Ponte (OSP), submission about 1 Dec"),
    ("Research at Brown", "up to $500"),
    ("Champlin Foundation", "$19,885 for the water rig (T2)"),
    ("NASA Rhode Island Space Grant", "spring 2027"),
    ("In kind", "SendCutSend $500 credit; OSH Cut student discount; PCBWay sponsorship applied for; TML gauges; Dewesoft recorder loan; Bolt Depot screws"),
]

SOURCES = [
    "HCSA test budget sheet, 10 Nov 2026 (prices, suppliers, statuses)",
    "Fabrication and testing plan, 23 Oct 2026 (methods, instruments, the T2 rig)",
    "Rev F release package, 13 Nov 2026: part 3 (test pieces), part 4 (computer tests), part 5 (open items), the appendix on Marco's points",
    "Sheets TP-00 to TP-04 and the test-piece STEP files, 9 Nov 2026",
    "Mail: TML (4 Nov), Trans-Tek (3 Nov), Parker (2-3 Nov), SendCutSend (11 Nov), Marco Cross (7-11 Nov), Kelly da Ponte (9 Nov)",
]

# Who makes or supplies what, across the tests
FAB = [
    ("Xometry (instant quote from the STEP pack)", "T1 frames A and B (3 lengths), the 550 frames A and B, pull blocks; PCBWay instead if the sponsorship comes through", "T1, SA-550", "Need to buy; quote once funded"),
    ("Brown shop", "End dams, the T2 hub, retaining beads and round bars, the Instron adapters; pull blocks or the run 2 fixture if cheaper", "T1, SA-550, T2", "Need to buy; adapters wait on measuring the Instron with Jerry"),
    ("Swift Glass", "BOROFLOAT 33 test bars with fine-ground edges and arris", "T0", "Quote in hand, about $1,040; free if ENGN 1440 has spares"),
    ("A welding shop (not found yet); Derecktor for plate", "The T2 steel tub, rings and clamp ring; hydrotest of the empty tub (B E Peterson would review)", "T2", "Need to buy; the tub has to be redrawn first"),
    ("SendCutSend or OSH Cut", "Cut plate: the T2 aluminium panes; possibly the end dams", "T2, T1", "SendCutSend $500 credit in hand; OSH Cut student discount"),
    ("Catalogue parts", "Butyl cord (Sandem), RTV566 and primer (SkyGeek or a Momentive sample), port fittings and relief valve (Swagelok Boston), bolts (McMaster, Bolt Depot), shims, EPDM, neoprene, Dwyer transducer, dial gauges", "All", "Need to buy, except the 60 M12 screws in hand"),
    ("Donated or lent instruments", "TML strain gauges (30, for T1), the Dewesoft recorder (loan), Trans-Tek LVDTs (to buy, $750)", "T1, SA-550, T2", "Gauges and recorder agreed, not here yet"),
]
