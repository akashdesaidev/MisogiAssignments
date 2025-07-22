'use client';

import { useState } from 'react';
import { BarChart, ChevronDown, ChevronUp, Maximize2, Minimize2 } from 'lucide-react';

interface Chunk {
  text: string;
  size: number;
  index: number;
  metadata?: {
    sentences?: number;
    words?: number;
    overlap?: number;
  };
}

interface ChunkVisualizationProps {
  chunks: Chunk[];
  originalText: string;
}

export const ChunkVisualization = ({ chunks, originalText }: ChunkVisualizationProps) => {
  const [selectedChunk, setSelectedChunk] = useState<number | null>(null);
  const [showStats, setShowStats] = useState(false);
  const [expandedChunks, setExpandedChunks] = useState<number[]>([]);

  const toggleChunkExpansion = (index: number) => {
    setExpandedChunks(prev => 
      prev.includes(index) 
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  const calculateStats = () => {
    const sizes = chunks.map(c => c.size);
    return {
      avgSize: Math.round(sizes.reduce((a, b) => a + b, 0) / chunks.length),
      minSize: Math.min(...sizes),
      maxSize: Math.max(...sizes),
      totalSize: sizes.reduce((a, b) => a + b, 0),
      compression: Math.round((sizes.reduce((a, b) => a + b, 0) / originalText.length) * 100)
    };
  };

  const stats = calculateStats();

  const getChunkMetadata = (chunk: Chunk, index: number) => {
    const sentences = chunk.text.split(/[.!?]+/).filter(Boolean).length;
    const words = chunk.text.split(/\s+/).filter(Boolean).length;
    const overlap = index > 0 ? findOverlap(chunks[index - 1].text, chunk.text) : 0;
    
    return {
      sentences,
      words,
      overlap
    };
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Chunks ({chunks.length})</h3>
        <button
          onClick={() => setShowStats(!showStats)}
          className="flex items-center gap-2 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
        >
          <BarChart className="w-4 h-4" />
          {showStats ? 'Hide Stats' : 'Show Stats'}
        </button>
      </div>

      {showStats && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium mb-3">Chunking Statistics</h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div>
              <p className="text-sm text-gray-600">Average Size</p>
              <p className="text-lg font-medium">{stats.avgSize} chars</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Size Range</p>
              <p className="text-lg font-medium">{stats.minSize} - {stats.maxSize} chars</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Size</p>
              <p className="text-lg font-medium">{stats.totalSize} chars</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Compression Ratio</p>
              <p className="text-lg font-medium">{stats.compression}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Number of Chunks</p>
              <p className="text-lg font-medium">{chunks.length}</p>
            </div>
          </div>
        </div>
      )}
      
      <div className="grid grid-cols-1 gap-4">
        {chunks.map((chunk, index) => {
          const metadata = getChunkMetadata(chunk, index);
          const isExpanded = expandedChunks.includes(index);
          
          return (
            <div
              key={index}
              className={`p-4 rounded-lg border transition-colors
                ${selectedChunk === index 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-200 hover:border-gray-300'}`}
            >
              <div className="flex justify-between items-start mb-2">
                <div className="text-sm font-medium text-gray-700">
                  Chunk {index + 1}
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleChunkExpansion(index)}
                    className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    {isExpanded ? (
                      <Minimize2 className="w-4 h-4 text-gray-500" />
                    ) : (
                      <Maximize2 className="w-4 h-4 text-gray-500" />
                    )}
                  </button>
                  <div className="text-xs text-gray-500">
                    {chunk.size} characters
                  </div>
                </div>
              </div>
              
              <div 
                className={`text-sm text-gray-600 whitespace-pre-wrap ${
                  isExpanded ? '' : 'line-clamp-3'
                }`}
              >
                {chunk.text}
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs text-gray-500">
                  <div>
                    <span className="font-medium">Position:</span>
                    <br />
                    {index + 1} of {chunks.length}
                  </div>
                  <div>
                    <span className="font-medium">Words:</span>
                    <br />
                    {metadata.words}
                  </div>
                  <div>
                    <span className="font-medium">Sentences:</span>
                    <br />
                    {metadata.sentences}
                  </div>
                  {index > 0 && (
                    <div>
                      <span className="font-medium">Overlap:</span>
                      <br />
                      {metadata.overlap} characters
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

function findOverlap(prev: string, current: string): number {
  let overlap = 0;
  const maxOverlap = Math.min(prev.length, current.length);
  
  for (let i = 1; i <= maxOverlap; i++) {
    if (prev.endsWith(current.slice(0, i))) {
      overlap = i;
    }
  }
  
  return overlap;
} 