import React, { useState } from 'react';
import axios from 'axios';

function AgentRunner({ projectId, onAgentComplete }) {
  const [company, setCompany] = useState("");
  const [industry, setIndustry] = useState("");
  const [language, setLanguage] = useState("ENGLISH");

  const handleRunAgent = async () => {
    const body = {
      COMPANY_NAME: company,
      INDUSTRY_NAME: industry,
      Language: language,
    };

    const res = await axios.post(`/api/v1/agent/inventory/${projectId}`, body);
    if (res.data.resultS) {
      onAgentComplete(res.data.resultS);
    }
  };

  return (
    <div>
      <input type="text" placeholder="Company Name" onChange={(e) => setCompany(e.target.value)} />
      <input type="text" placeholder="Industry" onChange={(e) => setIndustry(e.target.value)} />
      <select onChange={(e) => setLanguage(e.target.value)}>
        <option value="ENGLISH">English</option>
        <option value="ARABIC">Arabic</option>
      </select>
      <button onClick={handleRunAgent}>Run Analysis</button>
    </div>
  );
}

export default AgentRunner;
