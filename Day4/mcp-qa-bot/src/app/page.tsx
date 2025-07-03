import { ChatInterface } from "@/components/chat-interface";

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          MCP Q&A Assistant
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Ask questions about the Model Context Protocol (MCP)
        </p>
        <ChatInterface />
      </div>
    </main>
  );
}
