/**
 * MESA (Medical Expert System Assistant) Types
 * Complete type definitions for the Medical Expert System API
 */

/* ----------------------------- SYMPTOM TYPES ----------------------------- */

export type SymptomSeverity = 'mild' | 'moderate' | 'severe';
export type FeverPattern = 'cyclical' | 'stepladder' | 'continuous' | 'irregular';
export type DiarrheaDescription = 'rice_water' | 'watery' | 'bloody' | 'mucoid';

export interface Symptom {
  name: string;
  present?: boolean;
  severity?: SymptomSeverity;
  duration_days?: number;
  pattern?: FeverPattern;
  description?: string;
}

export interface SymptomInfo {
  name: string;
  display_name: string;
  description: string;
  options: {
    pattern?: FeverPattern[];
    severity?: SymptomSeverity[];
    description?: string[];
  } | null;
}

/* ----------------------------- PATIENT TYPES ----------------------------- */

export interface PatientInfo {
  age?: number;
  is_child?: boolean;
  is_pregnant?: boolean;
  travel_endemic_area?: boolean;
  endemic_resident?: boolean;
  unsafe_water?: boolean;
  street_food?: boolean;
  household_contact?: boolean;
}

/* ----------------------------- LAB RESULTS ----------------------------- */

export type LabTestType = 
  | 'blood_smear' 
  | 'rdt_malaria' 
  | 'stool_culture' 
  | 'rdt_cholera' 
  | 'blood_culture' 
  | 'widal' 
  | 'typhidot';

export type LabResultValue = 'positive' | 'negative' | 'pending';

export interface LabResult {
  test: LabTestType;
  result: LabResultValue;
  details?: string;
}

/* ----------------------------- DEHYDRATION ASSESSMENT ----------------------------- */

export type DehydrationSignType = 'mental_state' | 'eyes' | 'skin_pinch' | 'thirst';

export type MentalStateFinding = 'alert' | 'restless' | 'irritable' | 'lethargic' | 'unconscious';
export type EyesFinding = 'normal' | 'sunken';
export type SkinPinchFinding = 'normal' | 'slow' | 'very_slow' | '>2_seconds';
export type ThirstFinding = 'drinks_normally' | 'drinks_eagerly' | 'unable_to_drink';

export interface DehydrationSign {
  sign: DehydrationSignType;
  finding: string;
}

/* ----------------------------- DIAGNOSIS REQUEST/RESPONSE ----------------------------- */

export interface DiagnosisRequest {
  symptoms: Symptom[];
  patient?: PatientInfo;
  lab_results?: LabResult[];
  dehydration_signs?: DehydrationSign[];
}

export type DiagnosisConfidence = 'confirmed' | 'confident' | 'suspect' | 'uncertain';
export type DehydrationLevel = 'none' | 'some' | 'severe';
export type TreatmentPlan = 'A' | 'B' | 'C';

export interface Diagnosis {
  disease: string;
  confidence: DiagnosisConfidence;
  reason: string;
  severity: string | null;
  recommendation: string | null;
}

export interface DiagnosisResponse {
  diagnoses: Diagnosis[];
  recommendations: string[];
  dehydration_level: DehydrationLevel;
  treatment_plan: TreatmentPlan;
  disclaimer: string;
}

/* ----------------------------- DISEASE INFO ----------------------------- */

export interface DiseaseInfo {
  name: string;
  description: string;
  key_symptoms: string[];
  pathognomonic_signs: string[];
}

/* ----------------------------- CHAT TYPES ----------------------------- */

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_history: ChatMessage[];
  model?: string;
  include_expert_context?: boolean;
  patient_context?: PatientInfo;
}

export interface ChatResponse {
  response: string;
  model_used: string;
  conversation_history: ChatMessage[];
  extracted_symptoms: string[];
  suggested_diseases: string[];
}

/* ----------------------------- MODEL TYPES ----------------------------- */

export interface ModelInfo {
  id: string;
  name: string;
  description: string;
  context_window: number;
}

export interface ModelsResponse {
  models: ModelInfo[];
  default_model: string;
  current_model: string | null;
}

export interface ModelValidationRequest {
  model: string;
}

export interface ModelValidationResponse {
  model: string;
  valid: boolean;
  available_models: string[] | null;
}

/* ----------------------------- API INFO ----------------------------- */

export interface ApiInfo {
  name: string;
  version: string;
  status: 'operational' | 'degraded' | 'down';
  docs: string;
  endpoints: {
    expert: string;
    chat: string;
  };
}

export interface PingResponse {
  message: string;
}

/* ----------------------------- UI STATE TYPES ----------------------------- */

export type MesaMode = 'chat' | 'expert' | 'voice';

export interface MesaState {
  mode: MesaMode;
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
}

/* ----------------------------- VALID SYMPTOM NAMES ----------------------------- */

export const VALID_SYMPTOMS = [
  'fever',
  'chills',
  'sweating',
  'diarrhea',
  'vomiting',
  'dehydration',
  'headache',
  'abdominal_pain',
  'severe_abdominal_pain',
  'constipation',
  'bitter_taste',
  'rose_spots',
  'relative_bradycardia',
  'altered_consciousness',
  'convulsions',
  'body_aches',
  'dark_urine',
  'anemia',
  'melena',
  'bloody_stool',
] as const;

export type ValidSymptomName = typeof VALID_SYMPTOMS[number];
