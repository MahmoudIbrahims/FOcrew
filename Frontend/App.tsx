import React, { useState } from 'react';
import { ProjectHeader } from './components/ProjectHeader';
import { UploadSection } from './components/UploadSection';
import { AnalysisSection } from './components/AnalysisSection';
import { ReportViewer } from './components/ReportViewer';
import { AnalysisResponse } from './types';

const App: React.FC = () => {
  const [projectId, setProjectId] = useState<string | null>(null);
  const [projectName, setProjectName] = useState<string>(""); 
  const [isUploadComplete, setIsUploadComplete] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);

  const handleProjectSelected = (id: string, name: string) => {
    setProjectId(id);
    setProjectName(name);
    setIsUploadComplete(false);
    setAnalysisResult(null);
  };

  const handleProjectDeleted = () => {
    setProjectId(null);
    setProjectName("");
    setIsUploadComplete(false);
    setAnalysisResult(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <ProjectHeader 
        projectId={projectId} 
        projectName={projectName}
        onProjectCreated={handleProjectSelected} 
        onDeleteProject={handleProjectDeleted}
      />

      <main className="flex-1 w-full p-10">
        {analysisResult ? (
          <ReportViewer data={analysisResult} onBack={() => setAnalysisResult(null)} />
        ) : (
          <div className="max-w-7xl mx-auto">
            {!projectId ? (
              <div className="text-center py-32 bg-white rounded-2xl border-2 border-dashed border-slate-200">
                <h2 className="text-2xl font-bold text-slate-800">Welcome to FOcrew</h2>
                <p className="text-slate-500 mt-2">Create or select a project from the top menu to start.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <UploadSection projectId={projectId} onUploadSuccess={() => setIsUploadComplete(true)} />
                <AnalysisSection 
                  projectId={projectId} 
                  isUploadComplete={isUploadComplete}
                  onAnalysisSuccess={(data) => { setAnalysisResult(data); window.scrollTo(0,0); }}
                />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;