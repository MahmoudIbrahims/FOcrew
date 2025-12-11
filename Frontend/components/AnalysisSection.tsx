// import React, { useState, useEffect } from 'react';
// import { Bot, Sparkles, AlertCircle, FileText, Activity } from 'lucide-react';
// import { AnalysisStatus, LanguageEnum, AnalysisRequestPayload, AnalysisResponse } from '../types';
// import { runAnalysis } from '../services/apiService';

// interface AnalysisSectionProps {
//   projectId: number;
//   isUploadComplete: boolean;
// }

// export const AnalysisSection: React.FC<AnalysisSectionProps> = ({ projectId, isUploadComplete }) => {
//   const [payload, setPayload] = useState<AnalysisRequestPayload>({
//     Language: LanguageEnum.ARABIC,
//     COMPANY_NAME: '',
//     INDUSTRY_NAME: '',
//   });
//   const [status, setStatus] = useState<AnalysisStatus>(AnalysisStatus.IDLE);
//   const [progress, setProgress] = useState<number>(0);
//   const [result, setResult] = useState<AnalysisResponse | null>(null);
//   const [errorMsg, setErrorMsg] = useState('');

//   // Simulate progress when processing
//   useEffect(() => {
//     let interval: ReturnType<typeof setInterval>;
    
//     if (status === AnalysisStatus.PROCESSING) {
//       setProgress(0);
//       interval = setInterval(() => {
//         setProgress(prev => {
//           // Fast initial progress
//           if (prev < 30) return prev + 2;
//           // Steady middle progress
//           if (prev < 70) return prev + 0.5;
//           // Slow crawl near the end
//           if (prev < 95) return prev + 0.1;
//           // Cap at 95% until complete
//           return prev;
//         });
//       }, 200);
//     } else if (status === AnalysisStatus.SUCCESS) {
//       setProgress(100);
//     } else {
//       setProgress(0);
//     }

//     return () => {
//       if (interval) clearInterval(interval);
//     };
//   }, [status]);

//   const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
//     const { name, value } = e.target;
//     setPayload(prev => ({ ...prev, [name]: value }));
//     setStatus(AnalysisStatus.IDLE); // Reset status on edit
//   };

//   const handleAnalyze = async () => {
//     setStatus(AnalysisStatus.PROCESSING);
//     setErrorMsg('');
//     setResult(null);

//     try {
//       const data = await runAnalysis(projectId, payload);
//       setResult(data);
//       setStatus(AnalysisStatus.SUCCESS);
//     } catch (err: any) {
//       setStatus(AnalysisStatus.ERROR);
//       setErrorMsg(err.message || 'Analysis failed. Ensure a file is uploaded for this project.');
//     }
//   };

//   return (
//     <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col">
//       <div className="p-6 border-b border-slate-100 bg-slate-50/50">
//         <h2 className="text-lg font-semibold text-slate-800 flex items-center">
//           <Bot className="w-5 h-5 mr-2 text-indigo-600" />
//           Agent Configuration
//         </h2>
//         <p className="text-sm text-slate-500 mt-1">Configure the AI agent context and language.</p>
//       </div>

//       <div className="p-6 flex-1 flex flex-col space-y-5">
        
//         {/* Company Name */}
//         <div>
//           <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
//             Company Name
//           </label>
//           <input
//             type="text"
//             name="COMPANY_NAME"
//             value={payload.COMPANY_NAME}
//             onChange={handleInputChange}
//             placeholder="e.g. Breadfast"
//             disabled={!isUploadComplete}
//             className="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
//           />
//         </div>

//         {/* Industry Name */}
//         <div>
//           <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
//             Industry Name
//           </label>
//           <input
//             type="text"
//             name="INDUSTRY_NAME"
//             value={payload.INDUSTRY_NAME}
//             onChange={handleInputChange}
//             placeholder="e.g. Online Grocery Delivery"
//             disabled={!isUploadComplete}
//             className="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
//           />
//         </div>

//         {/* Language Selection */}
//         <div>
//           <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
//             Report Language
//           </label>
//           <select
//             name="Language"
//             value={payload.Language}
//             onChange={handleInputChange}
//             disabled={!isUploadComplete}
//             className="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
//           >
//             {Object.values(LanguageEnum).map((lang) => (
//               <option key={lang} value={lang}>{lang}</option>
//             ))}
//           </select>
//         </div>

//         {/* Status Messages */}
//         {status === AnalysisStatus.ERROR && (
//           <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm flex items-start">
//             <AlertCircle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
//             <span>{errorMsg}</span>
//           </div>
//         )}

//         {status === AnalysisStatus.SUCCESS && result && (
//            <div className="p-4 bg-indigo-50 border border-indigo-100 rounded-lg">
//              <div className="flex items-center text-indigo-800 font-semibold mb-2">
//                <Sparkles className="w-4 h-4 mr-2" />
//                Analysis Complete
//              </div>
//              <div className="space-y-2 text-sm text-indigo-700">
//                <div className="flex justify-between">
//                  <span className="opacity-75">Agent:</span>
//                  <span className="font-medium">{result.Agent_name}</span>
//                </div>
//                <div className="flex justify-between">
//                  <span className="opacity-75">Generated:</span>
//                  <span className="font-medium">{new Date(result.created_at).toLocaleTimeString()}</span>
//                </div>
//                <div className="pt-2 mt-2 border-t border-indigo-200">
//                  <p className="text-xs text-center opacity-80">Report generation successful.</p>
//                </div>
//              </div>
//            </div>
//         )}

//         {/* Action Button and Progress */}
//         <div className="mt-auto pt-4">
//           {status === AnalysisStatus.PROCESSING && (
//             <div className="mb-4">
//               <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
//                 <span>Generating Analysis...</span>
//                 <span>{Math.floor(progress)}%</span>
//               </div>
//               <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
//                 <div 
//                   className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2.5 rounded-full transition-all duration-300 ease-out" 
//                   style={{ width: `${progress}%` }}
//                 ></div>
//               </div>
//               <p className="text-xs text-slate-400 mt-2 text-center animate-pulse">
//                 This process may take up to a minute. Please do not close the tab.
//               </p>
//             </div>
//           )}

//           <button
//             onClick={handleAnalyze}
//             disabled={!isUploadComplete || status === AnalysisStatus.PROCESSING || !payload.COMPANY_NAME || !payload.INDUSTRY_NAME}
//             className={`w-full py-3 px-4 rounded-lg font-bold text-sm flex items-center justify-center transition-all ${
//               !isUploadComplete || !payload.COMPANY_NAME || !payload.INDUSTRY_NAME
//                 ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
//                 : status === AnalysisStatus.PROCESSING
//                   ? 'bg-indigo-100 text-indigo-400 cursor-wait'
//                   : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
//             }`}
//           >
//              {status === AnalysisStatus.PROCESSING ? (
//               <>
//                 <Activity className="w-5 h-5 mr-2 animate-spin" />
//                 Processing Request...
//               </>
//             ) : (
//               <>
//                 <FileText className="w-5 h-5 mr-2" />
//                 Generate Analysis Report
//               </>
//             )}
//           </button>
//           {!isUploadComplete && (
//             <p className="text-center text-xs text-slate-400 mt-2">
//               Please upload a dataset first.
//             </p>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };  


import React, { useState, useEffect } from 'react';
import { Bot, Sparkles, AlertCircle, FileText, Activity } from 'lucide-react';
import { AnalysisStatus, LanguageEnum, AnalysisRequestPayload, AnalysisResponse } from '../types';
import { runAnalysis } from '../services/apiService';

interface AnalysisSectionProps {
  projectId: number;
  isUploadComplete: boolean;
  onAnalysisSuccess: (data: AnalysisResponse) => void;
}

export const AnalysisSection: React.FC<AnalysisSectionProps> = ({ projectId, isUploadComplete, onAnalysisSuccess }) => {
  const [payload, setPayload] = useState<AnalysisRequestPayload>({
    Language: LanguageEnum.ARABIC,
    COMPANY_NAME: '',
    INDUSTRY_NAME: '',
  });
  const [status, setStatus] = useState<AnalysisStatus>(AnalysisStatus.IDLE);
  const [progress, setProgress] = useState<number>(0);
  const [errorMsg, setErrorMsg] = useState('');

  // Simulate progress when processing
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    
    if (status === AnalysisStatus.PROCESSING) {
      setProgress(0);
      interval = setInterval(() => {
        setProgress(prev => {
          // Fast initial progress
          if (prev < 30) return prev + 2;
          // Steady middle progress
          if (prev < 70) return prev + 0.5;
          // Slow crawl near the end
          if (prev < 95) return prev + 0.1;
          // Cap at 95% until complete
          return prev;
        });
      }, 200);
    } else if (status === AnalysisStatus.SUCCESS) {
      setProgress(100);
    } else {
      setProgress(0);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [status]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setPayload(prev => ({ ...prev, [name]: value }));
    setStatus(AnalysisStatus.IDLE); // Reset status on edit
  };

  const handleAnalyze = async () => {
    setStatus(AnalysisStatus.PROCESSING);
    setErrorMsg('');

    try {
      const data = await runAnalysis(projectId, payload);
      setStatus(AnalysisStatus.SUCCESS);
      
      // Delay slightly to show 100% progress before switching view
      setTimeout(() => {
        onAnalysisSuccess(data);
      }, 500);
      
    } catch (err: any) {
      setStatus(AnalysisStatus.ERROR);
      setErrorMsg(err.message || 'Analysis failed. Ensure a file is uploaded for this project.');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col">
      <div className="p-6 border-b border-slate-100 bg-slate-50/50">
        <h2 className="text-lg font-semibold text-slate-800 flex items-center">
          <Bot className="w-5 h-5 mr-2 text-indigo-600" />
          Agent Configuration
        </h2>
        <p className="text-sm text-slate-500 mt-1">Configure the AI agent context and language.</p>
      </div>

      <div className="p-6 flex-1 flex flex-col space-y-5">
        
        {/* Company Name */}
        <div>
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
            Company Name
          </label>
          <input
            type="text"
            name="COMPANY_NAME"
            value={payload.COMPANY_NAME}
            onChange={handleInputChange}
            placeholder="e.g. Breadfast"
            disabled={!isUploadComplete}
            className="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
          />
        </div>

        {/* Industry Name */}
        <div>
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
            Industry Name
          </label>
          <input
            type="text"
            name="INDUSTRY_NAME"
            value={payload.INDUSTRY_NAME}
            onChange={handleInputChange}
            placeholder="e.g. Online Grocery Delivery"
            disabled={!isUploadComplete}
            className="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
          />
        </div>

        {/* Language Selection */}
        <div>
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
            Report Language
          </label>
          <select
            name="Language"
            value={payload.Language}
            onChange={handleInputChange}
            disabled={!isUploadComplete}
            className="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {Object.values(LanguageEnum).map((lang) => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>
        </div>

        {/* Status Messages */}
        {status === AnalysisStatus.ERROR && (
          <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm flex items-start">
            <AlertCircle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {status === AnalysisStatus.SUCCESS && (
           <div className="p-3 bg-green-50 text-green-700 rounded-md text-sm flex items-center animate-pulse">
             <Sparkles className="w-4 h-4 mr-2" />
             <span>Analysis complete! Generating report view...</span>
           </div>
        )}

        {/* Action Button and Progress */}
        <div className="mt-auto pt-4">
          {status === AnalysisStatus.PROCESSING && (
            <div className="mb-4">
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Generating Analysis...</span>
                <span>{Math.floor(progress)}%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2.5 rounded-full transition-all duration-300 ease-out" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-xs text-slate-400 mt-2 text-center animate-pulse">
                This process may take up to a minute. Please do not close the tab.
              </p>
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={!isUploadComplete || status === AnalysisStatus.PROCESSING || !payload.COMPANY_NAME || !payload.INDUSTRY_NAME}
            className={`w-full py-3 px-4 rounded-lg font-bold text-sm flex items-center justify-center transition-all ${
              !isUploadComplete || !payload.COMPANY_NAME || !payload.INDUSTRY_NAME
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                : status === AnalysisStatus.PROCESSING
                  ? 'bg-indigo-100 text-indigo-400 cursor-wait'
                  : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
            }`}
          >
             {status === AnalysisStatus.PROCESSING ? (
              <>
                <Activity className="w-5 h-5 mr-2 animate-spin" />
                Processing Request...
              </>
            ) : (
              <>
                <FileText className="w-5 h-5 mr-2" />
                Generate Analysis Report
              </>
            )}
          </button>
          {!isUploadComplete && (
            <p className="text-center text-xs text-slate-400 mt-2">
              Please upload a dataset first.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};