import { useEffect, useState } from "react";
import { type HealthResponse, fetchHealth } from "../api/health";

type LoadState =
  | { readonly kind: "loading" }
  | { readonly kind: "ready"; readonly health: HealthResponse }
  | { readonly kind: "failed"; readonly message: string };

export function App(): JSX.Element {
  const [state, setState] = useState<LoadState>({ kind: "loading" });

  useEffect(() => {
    const controller = new AbortController();

    fetchHealth()
      .then((health) => setState({ kind: "ready", health }))
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }
        const message =
          error instanceof Error ? error.message : "Unknown health error.";
        setState({ kind: "failed", message });
      });

    return () => controller.abort();
  }, []);

  return (
    <main className="app-shell">
      <section className="status-panel" aria-labelledby="status-title">
        <p className="eyebrow">Full-stack project template</p>
        <h1 id="status-title">UTL Template</h1>
        {state.kind === "loading" ? (
          <p className="status-text">Checking backend...</p>
        ) : null}
        {state.kind === "failed" ? (
          <p className="status-text error">{state.message}</p>
        ) : null}
        {state.kind === "ready" ? (
          <dl className="health-grid">
            <div>
              <dt>Service</dt>
              <dd>{state.health.name}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{state.health.healthy ? "Healthy" : "Unavailable"}</dd>
            </div>
          </dl>
        ) : null}
      </section>
    </main>
  );
}
