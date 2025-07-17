import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import AgentRunner from './components/AgentRunner';
import ReportViewer from './components/ReportViewer';

function App() {
  const [projectId] = useState(1); // ثابت الآن
  const [report, setReport] = useState(null);

  return (
    <div>
      <h1>Inventory Agent Platform</h1>
      <FileUpload projectId={projectId} onUploadSuccess={(data) => console.log("File uploaded", data)} />
      <AgentRunner projectId={projectId} onAgentComplete={(result) => setReport(result)} />
      {report && <ReportViewer report={report} />}
    </div>
  );
}

export default App;
