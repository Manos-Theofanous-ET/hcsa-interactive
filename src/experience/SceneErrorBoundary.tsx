import { Component, type ReactNode } from "react";

type Props = { fallback: ReactNode; children: ReactNode };
type State = { failed: boolean };

/** If the 3D scene fails (WebGL unavailable, model or lighting file cannot
 *  load), show the still-image fallback instead. Without this, a thrown
 *  loader error unmounts the whole React tree and the page goes blank,
 *  text included. */
export class SceneErrorBoundary extends Component<Props, State> {
  override state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  override componentDidCatch(error: unknown) {
    // eslint-disable-next-line no-console
    console.error("[hcsa] 3D scene failed, showing still images instead:", error);
  }

  override render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}
