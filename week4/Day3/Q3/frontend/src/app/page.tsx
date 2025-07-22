'use client';

import { useState } from 'react';
import { FileUpload } from '../../components/FileUpload';
import { ChunkingStrategy } from '../../components/ChunkingStrategy';
import { ChunkVisualization} from '../../components/ChunkVisualization';
import { AlertCircle } from 'lucide-react';
import './globals.css';
interface ChunkConfig {
  chunkSize: number;
  overlap: number;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [originalText, setOriginalText] = useState<string>('');
  const [chunks, setChunks] = useState<Array<{ text: string; size: number; index: number }>>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chunkConfig, setChunkConfig] = useState<ChunkConfig>({
    chunkSize: 500,
    overlap: 50
  });

  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);
    setChunks([]);
    setError(null);
    setOriginalText('');
  };

  const handleStrategyChange = async (strategy: string) => {
    if (!selectedFile) return;
    
    try {
      setLoading(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('strategy', strategy);
      formData.append('chunk_size', chunkConfig.chunkSize.toString());
      formData.append('overlap', chunkConfig.overlap.toString());

      const response = await fetch('http://localhost:8000/chunk', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to process file');
      }

      const data = await response.json();
      setOriginalText(data.original_text || '');
      setChunks(data.chunks.map((text: string, index: number) => ({
        text,
        size: text.length,
        index
      })));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold mb-4">RAG Text Chunking Visualizer</h1>
          <p className="text-gray-600">
            Upload a PDF document and explore different text chunking strategies for RAG systems.
            Each strategy offers unique trade-offs between chunk size and semantic coherence.
          </p>
        </div>

        <FileUpload onFileSelect={handleFileSelect} />

        {selectedFile && (
          <div className="space-y-8">
            <ChunkingStrategy
              onStrategyChange={handleStrategyChange}
              onConfigChange={setChunkConfig}
            />

            {loading && (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
                <p className="mt-2 text-gray-600">Processing document...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center gap-2 text-red-600">
                  <AlertCircle className="w-5 h-5" />
                  <p>{error}</p>
                </div>
              </div>
            )}

            {chunks.length > 0 && (
              <ChunkVisualization 
                chunks={chunks} 
                originalText={originalText}
              />
            )}
          </div>
        )}
      </div>
    </main>
  );
} 