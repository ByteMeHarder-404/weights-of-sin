// API service for journal recommendations

const API_BASE_URL = 'http://127.0.0.1:5001';

export interface JournalRecommendationRequest {
  title: string;
  abstract: string;
}

export interface Author {
  name: string;
  institution: string;
  works_count: number;
  cited_by_count: number;
  openalex_url: string;
}

export interface JournalRecommendation {
  rank: number;
  name: string;
  url: string;
  publisher: string;
  semantic_score: number;
  peer_review_questions: string[];
  issn: string;
  impact_factor: number;
  acceptance_rate: number;
}

export interface RecommendationResponse {
  topAuthors: Author[];
  journalRecommendations: JournalRecommendation[];
}

export async function getJournalRecommendations(
  data: JournalRecommendationRequest
): Promise<RecommendationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/recommend`, {
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