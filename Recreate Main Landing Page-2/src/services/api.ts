import { type RecommendationRequest, type RecommendationResponse } from '../types/api';

const API_URL = 'http://127.0.0.1:5001';

export async function getJournalRecommendations(data: RecommendationRequest): Promise<RecommendationResponse> {
  try {
    const response = await fetch(`${API_URL}/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching journal recommendations:', error);
    throw error;
  }
}