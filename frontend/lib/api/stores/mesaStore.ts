/**
 * MESA (Medical Expert System Assistant) Store
 * State management for the Medical Expert System interface
 */

import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";
import type {
  MesaMode,
  ChatMessage,
  Symptom,
  PatientInfo,
  LabResult,
  DehydrationSign,
  DiagnosisResponse,
  SymptomInfo,
  DiseaseInfo,
  ModelInfo,
} from "../types/mesa.types";
import { MesaService } from "../services/MesaService";

/* ----------------------------- STATE INTERFACE ----------------------------- */

interface MesaState {
  // Mode
  mode: MesaMode;
  
  // Loading & Error
  isLoading: boolean;
  error: string | null;
  
  // Chat state
  conversationHistory: ChatMessage[];
  selectedModel: string;
  extractedSymptoms: string[];
  suggestedDiseases: string[];
  
  // Expert system state
  selectedSymptoms: Symptom[];
  patientInfo: PatientInfo;
  labResults: LabResult[];
  dehydrationSigns: DehydrationSign[];
  diagnosisResult: DiagnosisResponse | null;
  
  // Voice state
  isVoiceActive: boolean;
  isVoicePlaying: boolean;
  
  // Metadata
  availableSymptoms: SymptomInfo[];
  availableDiseases: DiseaseInfo[];
  availableModels: ModelInfo[];
  defaultModel: string;
  
  // Initialization
  isInitialized: boolean;
}

/* ----------------------------- ACTIONS INTERFACE ----------------------------- */

interface MesaActions {
  // Mode
  setMode: (mode: MesaMode) => void;
  
  // Initialization
  initialize: () => Promise<void>;
  
  // Chat actions
  sendMessage: (message: string) => Promise<void>;
  clearConversation: () => void;
  setSelectedModel: (model: string) => void;
  
  // Expert system actions
  addSymptom: (symptom: Symptom) => void;
  removeSymptom: (symptomName: string) => void;
  updateSymptom: (symptomName: string, updates: Partial<Symptom>) => void;
  clearSymptoms: () => void;
  setPatientInfo: (info: Partial<PatientInfo>) => void;
  addLabResult: (result: LabResult) => void;
  removeLabResult: (test: string) => void;
  addDehydrationSign: (sign: DehydrationSign) => void;
  removeDehydrationSign: (signType: string) => void;
  runDiagnosis: () => Promise<void>;
  clearDiagnosis: () => void;
  
  // Voice actions
  activateVoiceMode: () => void;
  deactivateVoiceMode: () => void;
  setVoicePlaying: (playing: boolean) => void;
  
  // Error handling
  setError: (error: string | null) => void;
  clearError: () => void;
  
  // Reset
  resetAll: () => void;
}

/* ----------------------------- INITIAL STATE ----------------------------- */

const initialState: MesaState = {
  mode: "chat",
  isLoading: false,
  error: null,
  conversationHistory: [],
  selectedModel: "llama-3.3-70b-versatile",
  extractedSymptoms: [],
  suggestedDiseases: [],
  selectedSymptoms: [],
  patientInfo: {},
  labResults: [],
  dehydrationSigns: [],
  diagnosisResult: null,
  isVoiceActive: false,
  isVoicePlaying: false,
  availableSymptoms: [],
  availableDiseases: [],
  availableModels: [],
  defaultModel: "llama-3.3-70b-versatile",
  isInitialized: false,
};

/* ----------------------------- STORE ----------------------------- */

export const useMesaStore = create<MesaState & MesaActions>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        /* -------- Mode -------- */
        setMode: (mode) => set({ mode }),

        /* -------- Initialization -------- */
        initialize: async () => {
          if (get().isInitialized) return;
          
          // Mark initialized immediately so UI doesn't block
          // Data will load in background
          set({ isInitialized: true, isLoading: true, error: null });
          
          try {
            // Fetch all metadata in parallel
            const [symptoms, diseases, modelsResponse] = await Promise.all([
              MesaService.getSymptoms().catch(() => []),
              MesaService.getDiseases().catch(() => []),
              MesaService.getModels().catch(() => ({
                models: [{
                  id: "llama-3.3-70b-versatile",
                  name: "Llama 3.3 70B",
                  description: "Default model",
                  context_window: 128000,
                }],
                default_model: "llama-3.3-70b-versatile",
              })),
            ]);

            set({
              availableSymptoms: symptoms,
              availableDiseases: diseases,
              availableModels: modelsResponse.models,
              defaultModel: modelsResponse.default_model,
              selectedModel: modelsResponse.default_model,
              isLoading: false,
            });
          } catch (error) {
            // Don't block UI on initialization failure
            console.warn("MESA initialization warning:", error);
            set({ isLoading: false });
          }
        },

        /* -------- Chat Actions -------- */
        sendMessage: async (message) => {
          const { conversationHistory, selectedModel, patientInfo } = get();
          
          set({ isLoading: true, error: null });
          
          try {
            const response = await MesaService.sendChatMessage(
              message,
              conversationHistory,
              {
                model: selectedModel,
                includeExpertContext: true,
                patientContext: Object.keys(patientInfo).length > 0 ? patientInfo : undefined,
              }
            );

            set({
              conversationHistory: response.conversation_history,
              extractedSymptoms: response.extracted_symptoms,
              suggestedDiseases: response.suggested_diseases,
              isLoading: false,
            });
          } catch (error) {
            const message = error instanceof Error ? error.message : "Failed to send message";
            set({ error: message, isLoading: false });
          }
        },

        clearConversation: () =>
          set({
            conversationHistory: [],
            extractedSymptoms: [],
            suggestedDiseases: [],
          }),

        setSelectedModel: (model) => set({ selectedModel: model }),

        /* -------- Expert System Actions -------- */
        addSymptom: (symptom) =>
          set((state) => ({
            selectedSymptoms: [
              ...state.selectedSymptoms.filter((s) => s.name !== symptom.name),
              symptom,
            ],
          })),

        removeSymptom: (symptomName) =>
          set((state) => ({
            selectedSymptoms: state.selectedSymptoms.filter(
              (s) => s.name !== symptomName
            ),
          })),

        updateSymptom: (symptomName, updates) =>
          set((state) => ({
            selectedSymptoms: state.selectedSymptoms.map((s) =>
              s.name === symptomName ? { ...s, ...updates } : s
            ),
          })),

        clearSymptoms: () => set({ selectedSymptoms: [] }),

        setPatientInfo: (info) =>
          set((state) => ({
            patientInfo: { ...state.patientInfo, ...info },
          })),

        addLabResult: (result) =>
          set((state) => ({
            labResults: [
              ...state.labResults.filter((r) => r.test !== result.test),
              result,
            ],
          })),

        removeLabResult: (test) =>
          set((state) => ({
            labResults: state.labResults.filter((r) => r.test !== test),
          })),

        addDehydrationSign: (sign) =>
          set((state) => ({
            dehydrationSigns: [
              ...state.dehydrationSigns.filter((s) => s.sign !== sign.sign),
              sign,
            ],
          })),

        removeDehydrationSign: (signType) =>
          set((state) => ({
            dehydrationSigns: state.dehydrationSigns.filter(
              (s) => s.sign !== signType
            ),
          })),

        runDiagnosis: async () => {
          const { selectedSymptoms, patientInfo, labResults, dehydrationSigns } = get();

          if (selectedSymptoms.length === 0) {
            set({ error: "Please select at least one symptom" });
            return;
          }

          set({ isLoading: true, error: null });

          try {
            const response = await MesaService.diagnose({
              symptoms: selectedSymptoms,
              patient: Object.keys(patientInfo).length > 0 ? patientInfo : undefined,
              lab_results: labResults.length > 0 ? labResults : undefined,
              dehydration_signs: dehydrationSigns.length > 0 ? dehydrationSigns : undefined,
            });

            set({ diagnosisResult: response, isLoading: false });
          } catch (error) {
            const message = error instanceof Error ? error.message : "Failed to run diagnosis";
            set({ error: message, isLoading: false });
          }
        },

        clearDiagnosis: () =>
          set({
            diagnosisResult: null,
            selectedSymptoms: [],
            labResults: [],
            dehydrationSigns: [],
          }),

        /* -------- Voice Actions -------- */
        activateVoiceMode: () => set({ isVoiceActive: true, mode: "voice" }),
        
        deactivateVoiceMode: () =>
          set({ isVoiceActive: false, isVoicePlaying: false, mode: "chat" }),
        
        setVoicePlaying: (playing) => set({ isVoicePlaying: playing }),

        /* -------- Error Handling -------- */
        setError: (error) => set({ error }),
        clearError: () => set({ error: null }),

        /* -------- Reset -------- */
        resetAll: () => set({ ...initialState, isInitialized: get().isInitialized }),
      }),
      {
        name: "mesa-store",
        partialize: (state) => ({
          mode: state.mode,
          selectedModel: state.selectedModel,
          patientInfo: state.patientInfo,
        }),
      }
    ),
    { name: "MESA" }
  )
);

/* ----------------------------- SELECTORS ----------------------------- */

export const selectIsReady = (state: MesaState) => state.isInitialized && !state.isLoading;
export const selectHasSymptoms = (state: MesaState) => state.selectedSymptoms.length > 0;
export const selectHasConversation = (state: MesaState) => state.conversationHistory.length > 0;
export const selectHasDiagnosis = (state: MesaState) => state.diagnosisResult !== null;
