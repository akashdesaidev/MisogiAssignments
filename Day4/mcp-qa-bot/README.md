# 🧠 MCP Q&A Chatbot

A specialized Q&A chatbot designed to assist developers in understanding and working with Model Context Protocol (MCP) servers. This intelligent assistant explains MCP concepts, provides implementation advice, and resolves common developer queries—without relying on RAG.

## Features

- ✅ Static knowledge base embedded at runtime (no RAG)
- ✅ Answers grounded in trusted MCP documentation
- ✅ Cites sources to avoid hallucination
- ✅ Developer-friendly UI with chat interface
- ✅ Fully responsive frontend built with Next.js 14 + Tailwind

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Technology Stack

- **Frontend**: Next.js 14 with App Router
- **UI**: TailwindCSS + Lucide Icons
- **Backend**: Next.js API Routes
- **AI**: OpenAI GPT-3.5 Turbo
- **Documentation**: Embedded MCP specifications

## Development

The chatbot uses a carefully curated set of MCP documentation embedded into the system prompt. This ensures responses are:

- Accurate and grounded in official documentation
- Free from hallucinations
- Consistent across conversations
- Focused on practical implementation advice

## License

MIT
