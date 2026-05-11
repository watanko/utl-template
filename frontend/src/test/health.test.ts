import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchHealth } from "../api/health";

describe("fetchHealth", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("A should parse a valid health response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              service_id: "00000000-0000-4000-8000-000000000001",
              name: "utl-template",
              healthy: true,
            }),
        }),
      ),
    );

    await expect(fetchHealth()).resolves.toEqual({
      service_id: "00000000-0000-4000-8000-000000000001",
      name: "utl-template",
      healthy: true,
    });
  });

  it("A should not accept failed health responses", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve({ ok: false, status: 500 })),
    );

    await expect(fetchHealth()).rejects.toThrow("Health request failed: 500");
  });
});
