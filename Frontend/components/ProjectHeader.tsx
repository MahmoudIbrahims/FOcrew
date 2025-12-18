import React, { useState, useEffect } from 'react';
import { FolderGit2, Plus, Trash2, ChevronDown, Loader2 } from 'lucide-react';


interface ProjectHeaderProps {
  projectId: string | null;
  projectName: string;
  onProjectCreated: (id: string, name: string) => void;
  onDeleteProject: () => void;
}

export const ProjectHeader: React.FC<ProjectHeaderProps> = ({
  projectId,
  projectName,
  onProjectCreated,
  onDeleteProject
}) => {
  const [projects, setProjects] = useState<any[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [loading, setLoading] = useState(false);

  // Function to fetch the projects list
  const fetchProjects = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/project/list/all');
      const data = await response.json();
      setProjects(data.projects || []);
    } catch (e) {
      console.error("Error fetching projects:", e);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, [projectId]);

  // Handle creating a new project
  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/project/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_name: newProjectName
        }),
      });

      if (!response.ok) throw new Error("Failed to create project");

      const data = await response.json();
      onProjectCreated(data.project_id, data.project_name);
      setIsModalOpen(false);
      setNewProjectName("");
    } catch (e) {
      alert("Error: Failed to create project. Please check if the server is running.");
    } finally {
      setLoading(false);
    }
  };

  // Handle deleting a project from the Backend
  const handleDelete = async () => {
    if (!projectId) return;

    const confirmDelete = window.confirm(`Are you sure you want to delete "${projectName}"? This action cannot be undone.`);
    if (!confirmDelete) return;

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/project/${projectId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        alert("Project deleted successfully.");
        onDeleteProject(); // Reset state in App.tsx
        fetchProjects();   // Refresh the dropdown list
      } else {
        throw new Error("Failed to delete project");
      }
    } catch (e) {
      alert("Error: Could not delete the project. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          
          {/* Logo Section */}
          <div className="flex items-center">
            <div className="mr-3">
              <img 
                src="/logo.png" 
                alt="FOcrew Logo" 
                className="h-20 w-auto object-contain" 
              />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900 leading-tight">FOcrew Data Analysis Agent</h1>
              <p className="text-[10px] text-slate-500 font-bold tracking-widest uppercase">Analytics Agent</p>
            </div>
          </div>

          {/* Actions Section */}
          <div className="flex items-center space-x-3">
            
            {/* Dropdown Menu */}
            <div className="relative group">
              <div className="flex items-center bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 cursor-pointer hover:border-indigo-400 transition-all">
                <span className="text-sm font-medium text-slate-700 min-w-[120px]">
                  {projectId ? projectName : "Select Project"}
                </span>
                <ChevronDown className="h-4 w-4 text-slate-400 ml-2" />
              </div>
              
              <div className="absolute right-0 mt-2 w-64 bg-white border border-slate-200 rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 p-2">
                {projects.length === 0 ? (
                  <div className="px-3 py-2 text-xs text-slate-400">No projects available</div>
                ) : (
                  projects.map((p) => (
                    <button
                      key={p.project_id}
                      onClick={() => onProjectCreated(p.project_id, p.project_name)}
                      className="w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors"
                    >
                      {p.project_name}
                    </button>
                  ))
                )}
              </div>
            </div>

            {/* Create Button */}
            <button
              onClick={() => setIsModalOpen(true)}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-bold flex items-center transition-colors"
            >
              <Plus className="h-4 w-4 mr-1" /> Create Project
            </button>

            {/* Delete Button (Active only when a project is selected) */}
            {projectId && (
              <button
                onClick={handleDelete}
                disabled={loading}
                className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                title="Delete Project"
              >
                {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Trash2 className="h-5 w-5" />}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Modal for Creating Project */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center z-[100] p-4">
          <div className="bg-white rounded-2xl w-full max-w-md shadow-2xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold text-slate-900">Create New Project</h3>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <Plus className="h-6 w-6 rotate-45" />
              </button>
            </div>
            
            <form onSubmit={handleCreate}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-slate-700 mb-1">Project Name</label>
                <input
                  autoFocus
                  required
                  className="w-full px-4 py-3 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                  placeholder="e.g., Q4 Financial Analysis"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                />
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-bold flex items-center justify-center transition-colors"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin mr-2" />
                    Creating...
                  </>
                ) : (
                  "Start Project"
                )}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};