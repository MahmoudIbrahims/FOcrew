// import React, { useState } from 'react';
// import { ProjectHeader } from './components/ProjectHeader';
// import { UploadSection } from './components/UploadSection';
// import { AnalysisSection } from './components/AnalysisSection';

// const App: React.FC = () => {
//   const [projectId, setProjectId] = useState<number>(1);
//   const [isUploadComplete, setIsUploadComplete] = useState<boolean>(false);

//   return (
//     <div className="min-h-screen bg-slate-50 flex flex-col">
//       <ProjectHeader 
//         projectId={projectId} 
//         setProjectId={(id) => {
//           setProjectId(id);
//           setIsUploadComplete(false); // Reset upload state if project changes
//         }} 
//       />

//       <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-full items-start">
          
//           {/* Left Column: File Upload */}
//           <div className="h-full">
//             <UploadSection 
//               projectId={projectId} 
//               onUploadSuccess={() => setIsUploadComplete(true)} 
//             />
//           </div>

//           {/* Right Column: Agent Configuration */}
//           <div className="h-full">
//             <AnalysisSection 
//               projectId={projectId} 
//               isUploadComplete={isUploadComplete} 
//             />
//           </div>

//         </div>
//       </main>

//       <footer className="bg-white border-t border-slate-200 mt-auto">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
//           <p className="text-center text-xs text-slate-400">
//             &copy; {new Date().getFullYear()} FOcrew Data Analysis Agent. Powered by CrewAI & FastAPI.
//           </p>
//         </div>
//       </footer>
//     </div>
//   );
// };

// export default App;  


//======================
import React, { useState } from 'react';
import { ProjectHeader } from './components/ProjectHeader';
import { UploadSection } from './components/UploadSection';
import { AnalysisSection } from './components/AnalysisSection';
import { ReportViewer } from './components/ReportViewer';
import { AnalysisResponse } from './types';

const App: React.FC = () => {
  const [projectId, setProjectId] = useState<number>(1);
  const [isUploadComplete, setIsUploadComplete] = useState<boolean>(false);
  
  // State for managing the views (Dashboard vs Report)
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);

  const handleAnalysisSuccess = (data: AnalysisResponse) => {
    setAnalysisResult(data);
    // Scroll to top when switching views
    window.scrollTo(0, 0);
  };

  const handleBackToDashboard = () => {
    setAnalysisResult(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <ProjectHeader 
        projectId={projectId} 
        setProjectId={(id) => {
          setProjectId(id);
          setIsUploadComplete(false); // Reset upload state if project changes
          setAnalysisResult(null); // Reset report view if project changes
        }} 
      />

      <main className="flex-1 w-full">
        {analysisResult ? (
          // View 2: Report Viewer
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 h-full">
             <ReportViewer data={analysisResult} onBack={handleBackToDashboard} />
          </div>
        ) : (
          // View 1: Dashboard (Upload + Analysis Config)
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-full items-start">
              
              {/* Left Column: File Upload */}
              <div className="h-full">
                <UploadSection 
                  projectId={projectId} 
                  onUploadSuccess={() => setIsUploadComplete(true)} 
                />
              </div>

              {/* Right Column: Agent Configuration */}
              <div className="h-full">
                <AnalysisSection 
                  projectId={projectId} 
                  isUploadComplete={isUploadComplete}
                  onAnalysisSuccess={handleAnalysisSuccess}
                />
              </div>

            </div>
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-slate-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-xs text-slate-400">
            &copy; {new Date().getFullYear()} FOcrew Data Analysis Agent.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;