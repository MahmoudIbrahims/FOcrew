// // Enums
// export enum LanguageEnum {
//   ARABIC = 'Arabic',
//   ENGLISH = 'English',
//   FRENCH = 'French',
//   SPANISH = 'Spanish'
// }

// export enum UploadStatus {
//   IDLE = 'IDLE',
//   UPLOADING = 'UPLOADING',
//   SUCCESS = 'SUCCESS',
//   ERROR = 'ERROR'
// }

// export enum AnalysisStatus {
//   IDLE = 'IDLE',
//   PROCESSING = 'PROCESSING',
//   SUCCESS = 'SUCCESS',
//   ERROR = 'ERROR'
// }

// // API Responses
// export interface UploadResponse {
//   message: string;
//   file_id: string;
//   file_uuid: string;
//   original_filename: string;
//   file_size: number;
//   rows: number;
//   columns: number;
//   s3_key: string;
// }

// export interface AnalysisResponse {
//   signal: string;
//   Agent_name: string;
//   created_at: string;
// }

// // API Requests
// export interface AnalysisRequestPayload {
//   Language: string;
//   COMPANY_NAME: string;
//   INDUSTRY_NAME: string;
// }

// Enums
export enum LanguageEnum {
  ARABIC = 'Arabic',
  ENGLISH = 'English',
  FRENCH = 'French',
  SPANISH = 'Spanish'
}

export enum UploadStatus {
  IDLE = 'IDLE',
  UPLOADING = 'UPLOADING',
  SUCCESS = 'SUCCESS',
  ERROR = 'ERROR'
}

export enum AnalysisStatus {
  IDLE = 'IDLE',
  PROCESSING = 'PROCESSING',
  SUCCESS = 'SUCCESS',
  ERROR = 'ERROR'
}

// API Responses
export interface UploadResponse {
  message: string;
  file_id: string;
  file_uuid: string;
  original_filename: string;
  file_size: number;
  rows: number;
  columns: number;
  s3_key: string;
}

// export interface AnalysisResponse {
//   signal: string;
//   Agent_name: string;
//   created_at: string;
//   report_url?: string; // Added to support PDF link
// } 

export interface AnalysisResponse {
  signal: string;
  Agent_name: string;
  created_at: string;
  pdfUrl: string;  
}

// API Requests
export interface AnalysisRequestPayload {
  Language: string;
  COMPANY_NAME: string;
  INDUSTRY_NAME: string;
}