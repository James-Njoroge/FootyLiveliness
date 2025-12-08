/**
 * API client for Footy Liveliness backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'APIError';
    this.status = status;
  }
}

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new APIError(error.error || 'Request failed', response.status);
  }
  return response.json();
}

export const api = {
  /**
   * Check API health
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await handleResponse(response);
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  /**
   * Get model information
   */
  async getModelInfo() {
    try {
      const response = await fetch(`${API_BASE_URL}/model/info`);
      return await handleResponse(response);
    } catch (error) {
      console.error('Failed to get model info:', error);
      throw error;
    }
  },

  /**
   * Predict liveliness for a single match
   */
  async predictMatch(matchData) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(matchData),
      });
      return await handleResponse(response);
    } catch (error) {
      console.error('Prediction failed:', error);
      throw error;
    }
  },

  /**
   * Predict liveliness for multiple matches
   */
  async predictBatch(matches) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ matches }),
      });
      return await handleResponse(response);
    } catch (error) {
      console.error('Batch prediction failed:', error);
      throw error;
    }
  },
};

export { APIError };
