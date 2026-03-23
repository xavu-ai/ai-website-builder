// types/prompt.ts
export interface PromptSubmission {
  description: string;
  submittedAt: Date;
}

export interface SubmissionResponse {
  success: boolean;
  queueId?: string;
  queuePosition?: number;
  estimatedWaitMinutes?: number;
  error?: string;
}
