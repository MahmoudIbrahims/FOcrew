import { AnalysisRequestPayload, AnalysisResponse, UploadResponse } from '../types';

// FastAPI backend base URL
// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const API_BASE_URL = 'http://localhost:8000/api/v1';
// const API_BASE_URL = 'http://localhost/api/v1';

/* -----------------------------------
   Upload File (unchanged - JSON)
----------------------------------- */
export const uploadFile = async (
  projectId: number,
  file: File,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const url = `${API_BASE_URL}/data/upload/${projectId}`;

    xhr.open('POST', url, true);

    // Track upload progress
    if (onProgress) {
      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percentComplete = (event.loaded / event.total) * 100;
          onProgress(percentComplete);
        }
      };
    }

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText);
          resolve(response);
        } catch {
          reject(new Error('Invalid JSON response from upload API'));
        }
      } else {
        try {
          const errorData = JSON.parse(xhr.responseText);
          reject(new Error(errorData.message || `Upload failed with status ${xhr.status}`));
        } catch {
          reject(new Error(`Upload failed with status ${xhr.status}`));
        }
      }
    };

    xhr.onerror = () => {
      reject(new Error('Network error occurred during file upload'));
    };

    const formData = new FormData();
    formData.append('file', file);
    xhr.send(formData);
  });
};

export const runAnalysis = async (
  projectId: number,
  payload: AnalysisRequestPayload
): Promise<string> => {  
  const response = await fetch(
    `${API_BASE_URL}/agent/DataAnalysis/${projectId}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    }
  );

  if (!response.ok) {
    let message = `Analysis failed with status ${response.status}`;
    try {
      const errorData = await response.json();
      message = errorData.message || message;
    } catch {}
    throw new Error(message);
  }

  const pdfBlob = await response.blob();
  const pdfUrl = URL.createObjectURL(pdfBlob);
  
  return pdfUrl;
};