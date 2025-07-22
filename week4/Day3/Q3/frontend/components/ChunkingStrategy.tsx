'use client';

import * as React from 'react';
import * as Select from '@radix-ui/react-select';
import { ChevronDown, Info } from 'lucide-react';
import * as Dialog from '@radix-ui/react-dialog';

interface ChunkingStrategyProps {
  onStrategyChange: (strategy: string) => void;
  onConfigChange: (config: { chunkSize: number; overlap: number }) => void;
}

const strategies = [
  {
    id: 'fixed_size',
    name: 'Fixed Size',
    description: 'Split text into chunks of fixed size with overlap',
    details: {
      whenToUse: [
        'When consistent chunk sizes are required',
        'For simple text without complex structure',
        'When processing speed is a priority'
      ],
      tradeoffs: [
        'May break semantic units (sentences/paragraphs)',
        'Simple and fast but less context-aware',
        'Good for uniform token limits in LLM calls'
      ]
    }
  },
  {
    id: 'sentence',
    name: 'Sentence-based',
    description: 'Split text into chunks by sentences, maintaining semantic coherence',
    details: {
      whenToUse: [
        'When semantic coherence is important',
        'For question-answering tasks',
        'When dealing with well-structured text'
      ],
      tradeoffs: [
        'Variable chunk sizes',
        'Better context preservation',
        'May create very small or large chunks'
      ]
    }
  },
  {
    id: 'paragraph',
    name: 'Paragraph-based',
    description: 'Split text into chunks by paragraphs, combining small ones and splitting large ones',
    details: {
      whenToUse: [
        'For documents with clear paragraph structure',
        'When topic separation is important',
        'For summarization tasks'
      ],
      tradeoffs: [
        'Most natural content boundaries',
        'May require additional processing for large paragraphs',
        'Best semantic coherence but less size control'
      ]
    }
  },
  {
    id: 'sliding_window',
    name: 'Sliding Window',
    description: 'Split text using a sliding window approach with fixed overlap',
    details: {
      whenToUse: [
        'When context between chunks is crucial',
        'For information retrieval tasks',
        'When dealing with continuous text'
      ],
      tradeoffs: [
        'Higher storage requirements due to overlap',
        'Better context preservation across chunks',
        'Good balance of coherence and size control'
      ]
    }
  }
];

export const ChunkingStrategy = ({ onStrategyChange, onConfigChange }: ChunkingStrategyProps) => {
  const [chunkSize, setChunkSize] = React.useState(500);
  const [overlap, setOverlap] = React.useState(50);
  const [selectedStrategy, setSelectedStrategy] = React.useState<string | null>(null);
  const [showInfo, setShowInfo] = React.useState(false);

  const handleStrategyChange = (value: string) => {
    setSelectedStrategy(value);
    onStrategyChange(value);
  };

  const handleChunkSizeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    setChunkSize(value);
    onConfigChange({ chunkSize: value, overlap });
  };

  const handleOverlapChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    setOverlap(value);
    onConfigChange({ chunkSize, overlap: value });
  };

  const selectedStrategyDetails = selectedStrategy 
    ? strategies.find(s => s.id === selectedStrategy)?.details
    : null;

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium">Chunking Strategy</label>
          <Dialog.Root>
            <Dialog.Trigger asChild>
              <button className="p-1 hover:bg-gray-100 rounded-full">
                <Info className="w-5 h-5 text-gray-500" />
              </button>
            </Dialog.Trigger>
            <Dialog.Portal>
              <Dialog.Overlay className="fixed inset-0 bg-black/50" />
              <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <Dialog.Title className="text-xl font-bold mb-4">
                  Understanding Chunking Strategies
                </Dialog.Title>
                <div className="space-y-6">
                  {strategies.map((strategy) => (
                    <div key={strategy.id} className="space-y-2">
                      <h3 className="text-lg font-semibold">{strategy.name}</h3>
                      <p className="text-gray-600">{strategy.description}</p>
                      <div className="mt-2">
                        <h4 className="font-medium">When to use:</h4>
                        <ul className="list-disc pl-5 text-sm text-gray-600">
                          {strategy.details.whenToUse.map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="mt-2">
                        <h4 className="font-medium">Trade-offs:</h4>
                        <ul className="list-disc pl-5 text-sm text-gray-600">
                          {strategy.details.tradeoffs.map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
                <Dialog.Close asChild>
                  <button className="absolute top-4 right-4 p-1 hover:bg-gray-100 rounded-full">
                    ✕
                  </button>
                </Dialog.Close>
              </Dialog.Content>
            </Dialog.Portal>
          </Dialog.Root>
        </div>
        <Select.Root onValueChange={handleStrategyChange}>
          <Select.Trigger className="w-full inline-flex items-center justify-between rounded-md px-4 py-2 text-sm bg-white border border-gray-300 hover:bg-gray-50">
            <Select.Value placeholder="Select a strategy" />
            <Select.Icon>
              <ChevronDown className="h-4 w-4 opacity-50" />
            </Select.Icon>
          </Select.Trigger>
          <Select.Portal>
            <Select.Content className="overflow-hidden bg-white rounded-md shadow-lg border border-gray-200">
              <Select.Viewport className="p-1">
                {strategies.map((strategy) => (
                  <Select.Item
                    key={strategy.id}
                    value={strategy.id}
                    className="relative flex items-center px-8 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer outline-none"
                  >
                    <Select.ItemText>{strategy.name}</Select.ItemText>
                    <p className="text-xs text-gray-500 mt-1">{strategy.description}</p>
                  </Select.Item>
                ))}
              </Select.Viewport>
            </Select.Content>
          </Select.Portal>
        </Select.Root>
      </div>

      {selectedStrategyDetails && (
        <div className="bg-gray-50 p-4 rounded-lg space-y-3">
          <h4 className="font-medium">Strategy Details:</h4>
          <div>
            <h5 className="text-sm font-medium">When to use:</h5>
            <ul className="list-disc pl-5 text-sm text-gray-600">
              {selectedStrategyDetails.whenToUse.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h5 className="text-sm font-medium">Trade-offs:</h5>
            <ul className="list-disc pl-5 text-sm text-gray-600">
              {selectedStrategyDetails.tradeoffs.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label className="text-sm font-medium">Chunk Size (characters)</label>
          <input
            type="range"
            min="100"
            max="1000"
            step="50"
            value={chunkSize}
            onChange={handleChunkSizeChange}
            className="w-full mt-2"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>100</span>
            <span>{chunkSize}</span>
            <span>1000</span>
          </div>
        </div>

        <div>
          <label className="text-sm font-medium">Overlap Size (characters)</label>
          <input
            type="range"
            min="0"
            max="200"
            step="10"
            value={overlap}
            onChange={handleOverlapChange}
            className="w-full mt-2"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0</span>
            <span>{overlap}</span>
            <span>200</span>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Higher overlap helps maintain context between chunks but increases storage requirements.
          </p>
        </div>
      </div>
    </div>
  );
}; 