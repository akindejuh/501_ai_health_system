/**
 * MESA (Medical Expert System Assistant) Service
 * Production-grade API integration for the Medical Expert System
 */

import { apiClient } from "../ApiClient";
import { MesaRoutes } from "../BackendRoutes";
import type {
  ApiInfo,
  PingResponse,
  SymptomInfo,
  DiseaseInfo,
  DiagnosisRequest,
  DiagnosisResponse,
  ChatRequest,
  ChatResponse,
  ModelsResponse,
  ModelValidationRequest,
  ModelValidationResponse,
  ChatMessage,
  PatientInfo,
} from "../types/mesa.types";

/* ----------------------------- MESA SERVICE ----------------------------- */

class MesaService {
  /* -------- GENERAL ENDPOINTS -------- */

  /**
   * Get API information and status
   */
  static async getApiInfo(): Promise<ApiInfo> {
    const res = await apiClient.get<ApiInfo>(MesaRoutes.root, {
      requiresAuth: false,
    });
    return res.data;
  }

  /**
   * Health check endpoint
   */
  static async ping(): Promise<PingResponse> {
    const res = await apiClient.get<PingResponse>(MesaRoutes.ping, {
      requiresAuth: false,
    });
    return res.data;
  }

  /* -------- EXPERT SYSTEM ENDPOINTS -------- */

  /**
   * Run the expert system diagnosis on provided symptoms
   */
  static async diagnose(request: DiagnosisRequest): Promise<DiagnosisResponse> {
    const res = await apiClient.post<DiagnosisResponse>(
      MesaRoutes.diagnose,
      request,
      { requiresAuth: false }
    );
    return res.data;
  }

  /**
   * Get list of all valid symptoms the expert system accepts
   */
  static async getSymptoms(): Promise<SymptomInfo[]> {
    const res = await apiClient.get<SymptomInfo[]>(MesaRoutes.symptoms, {
      requiresAuth: false,
    });
    return res.data;
  }

  /**
   * Get list of all diseases the expert system can diagnose
   */
  static async getDiseases(): Promise<DiseaseInfo[]> {
    const res = await apiClient.get<DiseaseInfo[]>(MesaRoutes.diseases, {
      requiresAuth: false,
    });
    return res.data;
  }

  /**
   * Get detailed information about a specific disease
   */
  static async getDisease(name: string): Promise<DiseaseInfo> {
    const res = await apiClient.get<DiseaseInfo>(MesaRoutes.disease(name), {
      requiresAuth: false,
    });
    return res.data;
  }

  /* -------- AI CHAT ENDPOINTS -------- */

  /**
   * Send a message to the AI medical assistant
   */
  static async sendChatMessage(
    message: string,
    conversationHistory: ChatMessage[] = [],
    options?: {
      model?: string;
      includeExpertContext?: boolean;
      patientContext?: PatientInfo;
    }
  ): Promise<ChatResponse> {
    const request: ChatRequest = {
      message,
      conversation_history: conversationHistory,
      model: options?.model,
      include_expert_context: options?.includeExpertContext ?? true,
      patient_context: options?.patientContext,
    };

    const res = await apiClient.post<ChatResponse>(
      MesaRoutes.chatMessage,
      request,
      { requiresAuth: false }
    );
    return res.data;
  }

  /**
   * Get list of available LLM models
   */
  static async getModels(): Promise<ModelsResponse> {
    const res = await apiClient.get<ModelsResponse>(MesaRoutes.chatModels, {
      requiresAuth: false,
    });
    return res.data;
  }

  /**
   * Validate if a model ID is available
   */
  static async validateModel(model: string): Promise<ModelValidationResponse> {
    const request: ModelValidationRequest = { model };
    const res = await apiClient.post<ModelValidationResponse>(
      MesaRoutes.validateModel,
      request,
      { requiresAuth: false }
    );
    return res.data;
  }
}

export default MesaService;
export { MesaService };
