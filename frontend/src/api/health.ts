import { z } from "zod";
import type { components } from "./generated/schema";

export type HealthResponse = components["schemas"]["HealthResponse"];

const healthResponseSchema = z.object({
  service_id: z.string().uuid(),
  name: z.string().min(1),
  healthy: z.boolean(),
});

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch("/health");
  if (!response.ok) {
    throw new Error(`Health request failed: ${response.status}`);
  }

  const body: unknown = await response.json();
  return healthResponseSchema.parse(body);
}
