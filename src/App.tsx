import { Experience } from "@/experience/Experience";
import { Overlay } from "@/overlay/Overlay";
import { PhaseRail } from "@/overlay/PhaseRail";
import { SiteBar } from "@/overlay/SiteBar";
import { RevealController } from "@/overlay/RevealController";

export function App() {
  return (
    <>
      <Experience />
      <Overlay />
      <PhaseRail />
      <SiteBar />
      <RevealController />
    </>
  );
}
