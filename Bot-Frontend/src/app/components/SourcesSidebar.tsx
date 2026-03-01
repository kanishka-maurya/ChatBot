import { FileText, Plus, X } from "lucide-react";

interface Source {
  id: string;
  name: string;
  type: string;
  pages?: number;
}

interface SourcesSidebarProps {
  sources: Source[];
  onAddSource: () => void;
  onRemoveSource: (id: string) => void;
}

export function SourcesSidebar({ sources, onAddSource, onRemoveSource }: SourcesSidebarProps) {
  return (
    <div className="w-80 border-r border-gray-200 bg-white flex flex-col h-screen">
      <div className="p-6 border-b border-gray-200">
        <h2 className="font-semibold text-lg mb-4">Sources</h2>
        <button
          onClick={onAddSource}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Source
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {sources.length === 0 ? (
          <div className="text-center text-gray-500 mt-8 px-4">
            <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p className="text-sm">No sources yet. Add documents to start chatting.</p>
          </div>
        ) : (
          sources.map((source) => (
            <div
              key={source.id}
              className="group relative p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-start gap-3">
                <FileText className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-sm truncate">{source.name}</h3>
                  <p className="text-xs text-gray-500 mt-0.5">
                    {source.type}
                    {source.pages && ` • ${source.pages} pages`}
                  </p>
                </div>
                <button
                  onClick={() => onRemoveSource(source.id)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-gray-200 rounded"
                >
                  <X className="w-4 h-4 text-gray-600" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
