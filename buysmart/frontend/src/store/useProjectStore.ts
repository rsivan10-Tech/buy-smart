import { create } from 'zustand';

type Project = {
  id: number;
  name: string;
  city: string;
  area_sqm?: number;
  price_ils?: number;
  created_at: string;
};

type ProjectState = {
  projects: Project[];
  selectedProjectId: number | null;
  loading: boolean;
  error: string | null;
  setProjects: (projects: Project[]) => void;
  addProject: (project: Project) => void;
  selectProject: (id: number | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
};

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  selectedProjectId: null,
  loading: false,
  error: null,
  setProjects: (projects) => set({ projects }),
  addProject: (project) => set((state) => ({ projects: [project, ...state.projects] })),
  selectProject: (id) => set({ selectedProjectId: id }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
