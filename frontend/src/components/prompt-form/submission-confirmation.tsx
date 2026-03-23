// components/prompt-form/submission-confirmation.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { SubmissionResponse } from "@/types/prompt";
import { Clock, Hash, ListOrdered, Sparkles } from "lucide-react";

interface SubmissionConfirmationProps {
  response: SubmissionResponse;
  onReset: () => void;
}

export function SubmissionConfirmation({ response, onReset }: SubmissionConfirmationProps) {
  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader className="text-center">
        <div className="mx-auto w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
          <Sparkles className="w-6 h-6 text-green-600" />
        </div>
        <CardTitle className="text-2xl">Submission Received!</CardTitle>
        <CardDescription>
          Your website generation request has been added to the queue.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {response.queueId && (
            <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
              <Hash className="w-5 h-5 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Queue ID</p>
                <p className="font-medium">{response.queueId}</p>
              </div>
            </div>
          )}
          {response.queuePosition !== undefined && (
            <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
              <ListOrdered className="w-5 h-5 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Position</p>
                <p className="font-medium">#{response.queuePosition}</p>
              </div>
            </div>
          )}
          {response.estimatedWaitMinutes !== undefined && (
            <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
              <Clock className="w-5 h-5 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Est. Wait</p>
                <p className="font-medium">{response.estimatedWaitMinutes} min</p>
              </div>
            </div>
          )}
        </div>

        <Button onClick={onReset} className="w-full" size="lg">
          Submit Another
        </Button>
      </CardContent>
    </Card>
  );
}
