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
import { NUMERICS as N, PLAIN } from "@content/numerics";
import { AboutSection } from "@/sections/AboutSection";
import { GallerySection } from "@/sections/GallerySection";
import { SponsorSection } from "@/sections/SponsorSection";
import { TeamSection } from "@/sections/TeamSection";

/** Corner-anchored chapters. Statement + why live as structured props here
 *  (one source of truth). MDX bodies are ONLY the tiny spec table (igloo
 *  pacing). Copy is written for sponsors and non-engineers: plain words,
 *  every number pulled from content/numerics.ts. */
const CHAPTERS = [
  {
    id: "habitat",
    idx: 2,
    title: "The Station",
    statement: `A glass and aluminium ball,\n${N.diameter.display} across.`,
    why: "Windows on every side, so visitors can see Earth and the stars from almost anywhere inside.",
    Body: Habitat,
  },
  {
    id: "assembly",
    idx: 3,
    title: "How It Gets Built",
    statement: "Made on Earth.\nPut together in orbit.",
    why: `All ${N.face_count.display} panels connect the same way, so one tool and one set of spare parts covers the whole station.`,
    Body: Assembly,
  },
  {
    id: "interior",
    idx: 4,
    title: "Inside",
    statement: "People by the windows.\nMachines in the middle.",
    why: "One open room with many uses. It can be rearranged without touching the outer shell.",
    Body: Interior,
  },
  {
    id: "panel",
    idx: 5,
    title: "The Window Panel",
    statement: `Each panel is a\n${N.panel_layers.display}-layer sandwich.`,
    why: `The air inside pushes on each large panel with the weight of about ${PLAIN.hex_force_tonnes} tonnes. The frame carries that load so the glass does not have to.`,
    Body: Panel,
  },
  {
    id: "bio",
    idx: 6,
    title: "Gardens",
    statement: "Plants clean the air\nand grow fresh food.",
    why: "Gardens make oxygen and bring daylight and green into the room. Machines cover the rest.",
    Body: Bio,
  },
  {
    id: "thermal",
    idx: 7,
    title: "Heat and Water",
    statement: "Sunlight cleans\nthe water.",
    why: "One side faces the sun, the other faces cold space. That difference boils and condenses water with almost no electricity.",
    Body: Thermal,
  },
  {
    id: "validate",
    idx: 8,
    title: "Testing",
    statement: `${N.roadmap_total.display} steps from idea to orbit.\nWe are on step ${N.roadmap_current.display}.`,
    why: "We test every idea on real hardware before we trust it.",
    Body: Validation,
  },
  {
    id: "contact",
    idx: 9,
    title: "Get Involved",
    statement: "Help us build\nthe next step.",
    why: "Keep scrolling to see our work, what your support pays for, and how to reach us.",
    Body: Contact,
  },
] as const;

export function Overlay() {
  return (
    <main className="hcsa-overlay-layer">
      {/* #film is the scroll-driven 3D story. ScrollProgress and PhaseRail
          measure progress against this element only, so the sections
          after it do not stretch the nine-phase timeline. */}
      <div id="film">
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
      </div>
      <div className="hcsa-after-film">
        <AboutSection />
        <GallerySection />
        <SponsorSection />
        <TeamSection />
        <footer className="px-6 py-16 text-center md:px-16">
          <p className="data text-[11px] uppercase tracking-[0.3em] text-white/65">
            Human-Centric Space Architecture, Brown University, {new Date().getFullYear()}
          </p>
        </footer>
      </div>
    </main>
  );
}
