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

const CHAPTERS = [
  { id: "habitat", idx: 2, title: "The Habitat", kicker: "11.151 m · 32 faces · 629 m³", Body: Habitat },
  { id: "assembly", idx: 3, title: "Earth-Built, Orbit-Assembled", kicker: "Fabricate · Stack · Launch · Snap · Weld", Body: Assembly },
  { id: "interior", idx: 4, title: "Inside the Shell", kicker: "~520 m³ habitable · 8 zones", Body: Interior },
  { id: "panel", idx: 5, title: "The Panel", kicker: "v3 joint · 7-layer glazing · NAS9306C-06", Body: Panel },
  { id: "bio", idx: 6, title: "Living Systems", kicker: "Bioregenerative ECLSS", Body: Bio },
  { id: "thermal", idx: 7, title: "Thermal & Water", kicker: "15 L/day distillation · closed loop", Body: Thermal },
  { id: "validate", idx: 8, title: "Coupon → Habitat", kicker: "P1 → P7 · currently P5", Body: Validation },
  { id: "contact", idx: 9, title: "Get Involved", kicker: "Research · Sponsorship · Alliance", Body: Contact },
] as const;

export function Overlay() {
  return (
    <main className="hcsa-overlay-layer">
      <HeroChapter />
      {CHAPTERS.map(({ id, idx, title, kicker, Body }) => (
        <ChapterStub key={id} id={id} index={idx} title={title} kicker={kicker}>
          <Body />
        </ChapterStub>
      ))}
      <footer className="px-8 py-24 text-center md:px-16">
        <p className="data text-[10px] uppercase tracking-[0.3em] text-white/35">
          HCSA Interactive · Brown University · 2026
        </p>
      </footer>
    </main>
  );
}
