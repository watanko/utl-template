import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../ui/App";

const healthResponse = {
  service_id: "00000000-0000-4000-8000-000000000001",
  name: "utl-template",
  healthy: true,
};

describe("App", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(healthResponse),
        }),
      ),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("A should render backend health", async () => {
    render(<App />);

    expect(await screen.findByText("utl-template")).toBeInTheDocument();
    expect(screen.getByText("Healthy")).toBeInTheDocument();
  });

  it("A should render backend health errors", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve({ ok: false, status: 503 })),
    );

    render(<App />);

    expect(
      await screen.findByText("Health request failed: 503"),
    ).toBeInTheDocument();
  });

  it("A should render unknown health errors", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.reject("broken")),
    );

    render(<App />);

    expect(
      await screen.findByText("Unknown health error."),
    ).toBeInTheDocument();
  });

  it("A should not update state after unmount", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.reject(new Error("late failure"))),
    );

    const view = render(<App />);
    view.unmount();
    await Promise.resolve();

    expect(screen.queryByText("late failure")).not.toBeInTheDocument();
  });
});
