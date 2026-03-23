import { PromptForm } from "@/components/prompt-form/prompt-form";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 md:px-6 lg:px-8 py-12 md:py-16 lg:py-24">
        <div className="max-w-2xl mx-auto">
          <PromptForm />
        </div>
      </main>
    </div>
  );
}
