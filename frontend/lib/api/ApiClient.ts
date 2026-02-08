/**
 * MESA API Client
 * Simplified HTTP client for the Medical Expert System
 */

// Types
export interface ApiError {
  message: string;
  status: number;
  code?: string;
  details?: unknown;
}

export interface ApiRequestConfig extends RequestInit {
  requiresAuth?: boolean;
  params?: Record<string, string | number | boolean | undefined>;
  timeout?: number;
}

export interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  headers: Headers;
}

// Configuration
const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  TIMEOUT: 30000,
} as const;

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_CONFIG.BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * GET request
   */
  async get<T = unknown>(
    endpoint: string,
    config?: ApiRequestConfig
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...config, method: "GET" });
  }

  /**
   * POST request
   */
  async post<T = unknown>(
    endpoint: string,
    data?: unknown,
    config?: ApiRequestConfig
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...config,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PUT request
   */
  async put<T = unknown>(
    endpoint: string,
    data?: unknown,
    config?: ApiRequestConfig
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...config,
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * DELETE request
   */
  async delete<T = unknown>(
    endpoint: string,
    config?: ApiRequestConfig
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...config, method: "DELETE" });
  }

  /**
   * Main request method
   */
  private async request<T>(
    endpoint: string,
    config: ApiRequestConfig = {}
  ): Promise<ApiResponse<T>> {
    const { timeout = API_CONFIG.TIMEOUT, params, ...fetchConfig } = config;

    // Build URL
    const url = this.buildURLWithParams(endpoint, params);

    // Prepare headers
    const headers = new Headers(fetchConfig.headers);
    if (!headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId =
      timeout > 0 ? setTimeout(() => controller.abort(), timeout) : undefined;

    try {
      const response = await fetch(url, {
        ...fetchConfig,
        headers,
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorData = await this.parseResponse<unknown>(response);
        const error: ApiError = {
          message: this.extractErrorMessage(errorData) || response.statusText,
          status: response.status,
          details: errorData,
        };
        throw error;
      }

      const data = await this.parseResponse<T>(response);
      return { data, status: response.status, headers: response.headers };
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        throw {
          message: "Request timeout",
          status: 408,
          code: "TIMEOUT",
        } as ApiError;
      }
      throw error;
    } finally {
      if (timeoutId) clearTimeout(timeoutId);
    }
  }

  /**
   * Build URL with query params
   */
  private buildURLWithParams(
    endpoint: string,
    params?: Record<string, string | number | boolean | undefined>
  ): string {
    const cleanEndpoint = endpoint.startsWith("/")
      ? endpoint.slice(1)
      : endpoint;
    const cleanBaseURL = this.baseURL.endsWith("/")
      ? this.baseURL.slice(0, -1)
      : this.baseURL;
    const base = `${cleanBaseURL}/${cleanEndpoint}`;

    if (!params) return base;

    const queryParts: string[] = [];
    for (const [key, val] of Object.entries(params)) {
      if (val !== undefined && val !== null) {
        queryParts.push(
          `${encodeURIComponent(key)}=${encodeURIComponent(String(val))}`
        );
      }
    }

    return queryParts.length > 0 ? `${base}?${queryParts.join("&")}` : base;
  }

  /**
   * Parse response data
   */
  private async parseResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get("content-type");

    if (response.status === 204 || !contentType) {
      return null as T;
    }

    if (contentType?.includes("application/json")) {
      return response.json();
    }

    return response.text() as unknown as T;
  }

  /**
   * Extract error message from response
   */
  private extractErrorMessage(data: unknown): string | null {
    if (!data || typeof data !== "object") return null;

    const obj = data as Record<string, unknown>;

    if (typeof obj.detail === "string") return obj.detail;
    if (typeof obj.message === "string") return obj.message;
    if (typeof obj.error === "string") return obj.error;
    if (Array.isArray(obj.detail)) {
      return obj.detail
        .map((d) => (typeof d === "string" ? d : JSON.stringify(d)))
        .join(", ");
    }

    return null;
  }

  /**
   * Set base URL
   */
  setBaseURL(url: string): void {
    this.baseURL = url;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
export default ApiClient;
