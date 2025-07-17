import React from 'react';

function ReportViewer({ report }) {
  return (
    <div>
      <h2>📄 Report Output</h2>
      <pre style={{ backgroundColor: "#f4f4f4", padding: "1em" }}>{report}</pre>
    </div>
  );
}

export default ReportViewer;
