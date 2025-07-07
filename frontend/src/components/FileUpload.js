import React, { useState } from 'react';
import axios from 'axios';

function FileUpload({ projectId, onUploadSuccess }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`/api/v1/data/upload/${projectId}`, formData);
    if (res.data.file_id) {
      onUploadSuccess(res.data); // send back file details
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept=".csv,.xlsx" />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default FileUpload;
