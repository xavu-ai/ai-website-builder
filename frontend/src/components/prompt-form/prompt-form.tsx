"use client";

import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CharacterCounter } from "./character-counter";
import { SubmissionConfirmation } from "./submission-confirmation";
import { submitPrompt } from "@/lib/api";
import { SubmissionResponse } from "@/types/prompt";
import { Loader2, AlertCircle } from "lucide-react";

type FormState = "idle" | "submitting" | "success" | "error";

const MAX_CHARS = 2000;
const MIN_CHARS = 10;

export function PromptForm() {
  const [description, setDescription] = useState("");
  const [formState, setFormState] = useState<FormState>("idle");
  const [error, setError] = useState<string | null>(null);
  const [submissionResponse, setSubmissionResponse] = useState<SubmissionResponse | null>(null);

  const charCount = description.length;
  const isValid = description.trim().length >= MIN_CHARS && charCount <= MAX_CHARS;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValid || formState === "submitting") return;

    setFormState("submitting");
    setError(null);

    try {
      const response = await submitPrompt(description.trim());
      setSubmissionResponse(response);
      setFormState("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
      setFormState("error");
    }
  };

  const handleReset = () => {
    setDescription("");
    setFormState("idle");
    setError(null);
    setSubmissionResponse(null);
  };

  // Show confirmation screen after successful submission
  if (formState === "success" && submissionResponse) {
    return <SubmissionConfirmation response={submissionResponse} onReset={handleReset} />;
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl">AI Website Builder</CardTitle>
        <CardDescription>
          Describe the website you want to build, and our AI will generate it for you.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label
              htmlFor="description"
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Website Description
            </label>
            <Textarea
              id="description"
              name="description"
              placeholder="Describe the website you want to build..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={formState === "submitting"}
              rows={8}
              className="resize-none"
              aria-describedby="char-counter description-help"
              aria-invalid={charCount > MAX_CHARS}
              onKeyDown={(e) => {
                // Prevent Enter key from submitting when textarea is focused
                if (e.key === "Enter" && !e.metaKey && !e.ctrlKey) {
                  // Allow new lines in textarea, don't submit
                  return;
                }
              }}
            />
            <div id="char-counter">
              <CharacterCounter count={charCount} maxCount={MAX_CHARS} />
            </div>
            <p id="description-help" className="text-xs text-muted-foreground">
              Minimum {MIN_CHARS} characters required.
            </p>
          </div>

          {formState === "error" && error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button
            type="submit"
            disabled={!isValid || formState === "submitting"}
            className="w-full"
            size="lg"
            aria-label={formState === "submitting" ? "Submitting..." : "Submit request"}
          >
            {formState === "submitting" ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting...
              </>
            ) : (
              "Generate Website"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
