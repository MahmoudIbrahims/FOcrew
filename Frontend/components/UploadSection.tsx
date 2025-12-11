import React, { useState, useRef } from 'react';
import { UploadCloud, FileSpreadsheet, CheckCircle, AlertCircle, Loader2, X } from 'lucide-react';
import { UploadStatus, UploadResponse } from '../types';
import { uploadFile } from '../services/apiService';

interface UploadSectionProps {
  projectId: number;
  onUploadSuccess: () => void;
}

export const UploadSection: React.FC<UploadSectionProps> = ({ projectId, onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<UploadStatus>(UploadStatus.IDLE);
  const [progress, setProgress] = useState<number>(0);
  const [uploadData, setUploadData] = useState<UploadResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
      setStatus(UploadStatus.IDLE);
      setErrorMessage('');
      setUploadData(null);
      setProgress(0);
    }
  };

  const handleClearFile = () => {
    setFile(null);
    setStatus(UploadStatus.IDLE);
    setProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setStatus(UploadStatus.UPLOADING);
    setProgress(0);
    try {
      const data = await uploadFile(projectId, file, (percent) => {
        setProgress(percent);
      });
      setUploadData(data);
      setStatus(UploadStatus.SUCCESS);
      onUploadSuccess();
    } catch (error: any) {
      setStatus(UploadStatus.ERROR);
      setErrorMessage(error.message || 'An unknown error occurred during upload.');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col">
      <div className="p-6 border-b border-slate-100 bg-slate-50/50">
        <h2 className="text-lg font-semibold text-slate-800 flex items-center">
          <UploadCloud className="w-5 h-5 mr-2 text-indigo-600" />
          Data Ingestion
        </h2>
        <p className="text-sm text-slate-500 mt-1">Upload your CSV or Excel dataset to begin.</p>
      </div>

      <div className="p-6 flex-1 flex flex-col">
        {!file && (
          <div 
            className="flex-1 border-2 border-dashed border-slate-300 rounded-lg flex flex-col items-center justify-center p-8 hover:bg-slate-50 transition-colors cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mb-4">
              <FileSpreadsheet className="w-6 h-6" />
            </div>
            <p className="text-sm font-medium text-slate-700">Click to select a file</p>
            <p className="text-xs text-slate-500 mt-1">CSV, Excel, or Sheet files supported</p>
          </div>
        )}

        {file && (
          <div className="bg-slate-50 rounded-lg p-4 border border-slate-200 mb-6 relative group">
            <div className="flex items-center">
              <FileSpreadsheet className="w-8 h-8 text-indigo-600 mr-3" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-900 truncate">{file.name}</p>
                <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(2)} KB</p>
              </div>
              {status !== UploadStatus.UPLOADING && status !== UploadStatus.SUCCESS && (
                <button 
                  onClick={handleClearFile}
                  className="p-1 hover:bg-slate-200 rounded-full text-slate-400 hover:text-slate-600 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>
        )}

        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".csv,.xlsx,.xls"
          className="hidden" 
        />

        {status === UploadStatus.ERROR && (
          <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-md text-sm flex items-start">
            <AlertCircle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        {status === UploadStatus.SUCCESS && uploadData && (
          <div className="mt-4 p-3 bg-green-50 text-green-700 rounded-md text-sm">
            <div className="flex items-center mb-2 font-medium">
              <CheckCircle className="w-4 h-4 mr-2" />
              File Uploaded Successfully
            </div>
            <ul className="text-xs space-y-1 text-green-800 opacity-90 pl-6 list-disc">
               <li>UUID: {uploadData.file_uuid}</li>
               <li>Rows: {uploadData.rows}</li>
               <li>Columns: {uploadData.columns}</li>
            </ul>
          </div>
        )}

        <div className="mt-auto pt-6">
          {status === UploadStatus.UPLOADING && (
            <div className="mb-4">
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Uploading...</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                <div 
                  className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300 ease-out" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={!file || status === UploadStatus.UPLOADING || status === UploadStatus.SUCCESS}
            className={`w-full py-2.5 px-4 rounded-lg font-medium text-sm flex items-center justify-center transition-all ${
              !file || status === UploadStatus.SUCCESS
                ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                : status === UploadStatus.UPLOADING
                  ? 'bg-indigo-400 text-white cursor-wait opacity-80'
                  : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-md hover:shadow-lg'
            }`}
          >
            {status === UploadStatus.UPLOADING ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Processing...
              </>
            ) : status === UploadStatus.SUCCESS ? (
              'Upload Complete'
            ) : (
              'Upload Data'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};