import React from 'react';
import { FolderGit2 } from 'lucide-react';

interface ProjectHeaderProps {
  projectId: number;
  setProjectId: (id: number) => void;
}

export const ProjectHeader: React.FC<ProjectHeaderProps> = ({ projectId, setProjectId }) => {
  return (
    <div className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Increased height to h-20 to accommodate larger logo comfortably */}
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            {/* Logo Container: Replaces the old Database icon container */}
            <div className="flex-shrink-0 flex items-center justify-center">
              <img src="/logo.png" alt="FOcrew Logo" className="h-20 w-auto object-contain" />
            </div>
            
            {/* Text Container */}
            <div className="ml-4">
              <h1 className="text-2xl font-bold text-slate-900 leading-tight">FOcrew Data Analysis Agent</h1>
              <p className="text-xs text-slate-500 font-medium tracking-wide">AI-POWERED ANALYTICS</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <label htmlFor="projectId" className="text-sm font-medium text-slate-600 hidden sm:block">
              Active Project ID:
            </label>
            <div className="relative rounded-md shadow-sm">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <FolderGit2 className="h-4 w-4 text-slate-400" />
              </div>
              <input
                type="number"
                name="projectId"
                id="projectId"
                min={1}
                className="block w-24 rounded-md border-slate-300 pl-10 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 border text-slate-800"
                value={projectId}
                onChange={(e) => setProjectId(Number(e.target.value))}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};