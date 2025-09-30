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

export interface RecommendationRequest {
  title: string;
  abstract: string;
}

export interface RecommendationResponse {
  topAuthors: Author[];
  journalRecommendations: JournalRecommendation[];
}