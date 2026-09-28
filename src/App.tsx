import { Experience } from "@/experience/Experience";
import { Overlay } from "@/overlay/Overlay";
import { PhaseRail } from "@/overlay/PhaseRail";
import { SiteBar } from "@/overlay/SiteBar";

export function App() {
  return (
    <>
      <Experience />
      <Overlay />
      <PhaseRail />
      <SiteBar />
    </>
  );
}
