// lib/api.ts
import { SubmissionResponse } from "@/types/prompt";

const API_BASE = ""; // Empty = relative paths, rewrites handle routing

export async function submitPrompt(description: string): Promise<SubmissionResponse> {
  const response = await fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Submission failed" }));
    throw new Error(error.error || "Submission failed");
  }

  return response.json();
}
