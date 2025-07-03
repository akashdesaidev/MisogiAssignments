import { ChatInterface } from "@/components/chat-interface";
import { Bot } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Bot className="w-12 h-12 text-blue-500" />
          </div>
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
            MCP Q&A Assistant
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Your intelligent assistant for understanding and working with the
            Model Context Protocol (MCP). Ask questions, get clarifications, and
            explore MCP concepts with ease.
          </p>
        </div>
        <ChatInterface />
      </div>
    </main>
  );
}
