import { HeroChapter } from "@/chapters/HeroChapter";
import { ChapterStub } from "@/chapters/ChapterStub";
import Habitat from "@content/chapters/02-habitat.mdx";
import Assembly from "@content/chapters/03-assembly.mdx";
import Interior from "@content/chapters/04-interior.mdx";
import Panel from "@content/chapters/05-panel.mdx";
import Bio from "@content/chapters/06-bio.mdx";
import Thermal from "@content/chapters/07-thermal.mdx";
import Validation from "@content/chapters/08-validation.mdx";
import Contact from "@content/chapters/09-contact.mdx";

/** Corner-anchored chapters. Statement + why live as structured props here
 *  (one source of truth). MDX bodies are ONLY the tiny spec table — the
 *  prose that used to fill the middle is gone on purpose (igloo pacing).
 *  Any phase that needs more detail later can get a "deep dive" drawer. */
const CHAPTERS = [
  {
    id: "habitat",
    idx: 2,
    title: "Habitat",
    statement: "Twenty hexagons.\nTwelve pentagons.\nOne joint, thirty-two times.",
    why: "One validated joint unlocks every panel.",
    Body: Habitat,
  },
  {
    id: "assembly",
    idx: 3,
    title: "Assembly",
    statement: "Earth-built.\nOrbit-assembled.",
    why: "Same joint 32×. One tool. One gasket SKU.",
    Body: Assembly,
  },
  {
    id: "interior",
    idx: 4,
    title: "Interior",
    statement: "Observation at the shell.\nMachines at the core.",
    why: "Reconfigurable without breaching the hull.",
    Body: Interior,
  },
  {
    id: "panel",
    idx: 5,
    title: "Panel V3",
    statement: "Seven layers.\nVacuum to crew.",
    why: "Remove any layer — the panel only works in one failure mode.",
    Body: Panel,
  },
  {
    id: "bio",
    idx: 6,
    title: "Living Systems",
    statement: "One pentagon per zone.\nThree trays. Full-spectrum.",
    why: "Bio takes the baseline; physico-chemical takes the peaks.",
    Body: Bio,
  },
  {
    id: "thermal",
    idx: 7,
    title: "Thermal / Water",
    statement: "Red carries heat out.\nBlue returns distillate.",
    why: "The core isn't hidden plumbing. It's the spine.",
    Body: Thermal,
  },
  {
    id: "validate",
    idx: 8,
    title: "Validation",
    statement: "P1 to P7.\nCurrently P5.",
    why: "Until a coupon matches the model, the model is a hypothesis.",
    Body: Validation,
  },
  {
    id: "contact",
    idx: 9,
    title: "Get Involved",
    statement: "Brown University.\nLooking for collaborators.",
    why: "We want pushback. Reach through Brown.",
    Body: Contact,
  },
] as const;

export function Overlay() {
  return (
    <main className="hcsa-overlay-layer">
      <HeroChapter />
      {CHAPTERS.map(({ id, idx, title, statement, why, Body }) => (
        <ChapterStub
          key={id}
          id={id}
          index={idx}
          title={title}
          statement={statement}
          why={why}
        >
          <Body />
        </ChapterStub>
      ))}
      <footer className="relative z-10 px-8 py-16 text-center md:px-16">
        <p className="data text-[10px] uppercase tracking-[0.3em] text-white/35">
          HCSA · Brown University · {new Date().getFullYear()}
        </p>
      </footer>
    </main>
  );
}
