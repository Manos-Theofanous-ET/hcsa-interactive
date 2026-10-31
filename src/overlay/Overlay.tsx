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
    title: "The station",
    statement: `It is a ball of glass and\naluminium, ${N.diameter.display} across.`,
    why: "There are windows on every side, so visitors can see Earth and the stars from almost anywhere inside.",
    Body: Habitat,
  },
  {
    id: "assembly",
    idx: 3,
    title: "How it gets built",
    statement: "We make it on Earth\nand put it together in orbit.",
    why: `All ${N.face_count.display} panels connect the same way, so one tool and one set of spare parts work for the whole station.`,
    Body: Assembly,
  },
  {
    id: "interior",
    idx: 4,
    title: "Inside",
    statement: "People stay by the windows.\nMachines stay in the middle.",
    why: "It is one open room with many uses, and we can rearrange it without touching the outer shell.",
    Body: Interior,
  },
  {
    id: "panel",
    idx: 5,
    title: "The window panel",
    statement: `Each window panel is a\nsandwich of ${N.panel_layers.display} layers.`,
    why: `The air inside pushes on each six-sided panel as hard as a weight of about ${PLAIN.hex_force_tonnes} tonnes would. The frames, the corner nodes and the hardpoints carry that push.`,
    Body: Panel,
  },
  {
    id: "bio",
    idx: 6,
    title: "Gardens",
    statement: "Plants clean the air\nand grow fresh food.",
    why: "The gardens make oxygen and bring daylight and green into the room. Machines do the rest.",
    Body: Bio,
  },
  {
    id: "thermal",
    idx: 7,
    title: "Heat and water",
    statement: "Sunlight cleans\nthe water.",
    why: "One side faces the sun and the other faces cold space. The difference in heat boils the water and condenses it again, with almost no electricity.",
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
    title: "Get involved",
    statement: "Help us build\nthe next step.",
    why: "Keep scrolling to see our work, what your support pays for and how to reach us.",
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
        <footer className="hcsa-footer">
          <div className="hcsa-footer-grid">
            <div>
              <p className="font-serif text-2xl text-white">Human-Centric Space Architecture</p>
              <p className="mt-2 max-w-sm text-[15px] leading-relaxed text-white/60">
                HCSA is a student research project at Brown University, developed with the Rhode Island School of Design.
              </p>
            </div>
            <nav aria-label="Footer">
              <p className="hcsa-footer-head">Project</p>
              <ul>
                <li><a href="/plan/">The plan</a></li>
                <li><a href="/blueprints/">Blueprints</a></li>
                <li><a href="/downloads/HCSA-Rev-S-drawings-explained-26-Sep-2026.pdf">Earlier Rev S drawings (PDF)</a></li>
              </ul>
            </nav>
            <nav aria-label="On this page">
              <p className="hcsa-footer-head">On this page</p>
              <ul>
                <li><a href="#work">Our work</a></li>
                <li><a href="#sponsor">Sponsor the project</a></li>
                <li><a href="#team">The team</a></li>
              </ul>
            </nav>
            <div>
              <p className="hcsa-footer-head">People</p>
              <ul>
                <li>Prof. Rick Fleeter, faculty advisor</li>
                <li>Manos Theofanous, project lead</li>
                <li>Brown University School of Engineering</li>
              </ul>
            </div>
          </div>
          <p className="hcsa-footer-base">© {new Date().getFullYear()} Human-Centric Space Architecture, Brown University</p>
        </footer>
      </div>
    </main>
  );
}
