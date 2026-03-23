// components/prompt-form/character-counter.tsx
import { cn } from "@/lib/utils";

interface CharacterCounterProps {
  count: number;
  maxCount: number;
}

export function CharacterCounter({ count, maxCount }: CharacterCounterProps) {
  const isOverLimit = count > maxCount;

  return (
    <div
      className={cn(
        "text-sm text-right transition-colors duration-150",
        isOverLimit ? "text-red-500 font-medium" : "text-muted-foreground"
      )}
      aria-live="polite"
      aria-atomic="true"
    >
      {count}/{maxCount}
    </div>
  );
}
