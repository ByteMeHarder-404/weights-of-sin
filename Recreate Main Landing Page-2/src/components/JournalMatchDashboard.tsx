import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Checkbox } from './ui/checkbox';
import { Badge } from './ui/badge';
import { Card } from './ui/card';
import { Slider } from './ui/slider';
import { BookOpen, HelpCircle, User, Bookmark } from 'lucide-react';
import { type ApiRequest, type ApiResponse, type JournalRecommendation } from '../types/api';

const API_URL = 'http://127.0.0.1:5001';

async function getJournalRecommendations(data: ApiRequest): Promise<ApiResponse> {
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

  return response.json();
}
import { getJournalRecommendations, type JournalRecommendation } from '../lib/api';

// Background colors for journal cards
const BACKGROUND_COLORS = [
  'bg-[#F3F0D3]',  // Yellow
  'bg-[#D4D9E2]',  // Blue-gray
  'bg-[#E5E2D9]',  // Beige
  'bg-[#F2E2ED]',  // Pink
];
import { getJournalRecommendations, type JournalRecommendation } from '../lib/api';

export function JournalMatchDashboard() {
  const [impactFactor, setImpactFactor] = useState([2]);
  const [title, setTitle] = useState('');
  const [abstract, setAbstract] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<JournalRecommendation[]>([]);

  const handleSubmit = async () => {
    if (!title || !abstract) {
      setError('Please provide both title and abstract');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await getJournalRecommendations({ title, abstract });
      setRecommendations(response.journalRecommendations);
    } catch (err) {
      setError('Failed to fetch recommendations. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };
  const [title, setTitle] = useState('');
  const [abstract, setAbstract] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<JournalRecommendation[]>([]);

  const handleSubmit = async () => {
    if (!title || !abstract) {
      setError('Please provide both title and abstract');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await getJournalRecommendations({ title, abstract });
      setRecommendations(response.journalRecommendations);
    } catch (err) {
      setError('Failed to fetch recommendations. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#FCFCFA] p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-[#333333]" />
            <h1 className="text-2xl font-semibold text-[#333333]">Journal Compass</h1>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" className="text-[#6c757d]">Help</Button>
            <div className="w-10 h-10 bg-gray-200 border-2 border-gray-300 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-[#6c757d]" />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="space-y-8">
          {/* Find the Perfect Home Section */}
          <div className="text-center space-y-4 mb-8">
            <h2 className="text-3xl font-bold text-[#333333]">Find Your Journal Match with AI</h2>
            <p className="text-lg text-[#6c757d]">Enter your paper details below to get personalized journal recommendations.</p>
          </div>

          {/* Input Container */}
          <div className="bg-[#F0F0F0] rounded-2xl p-8 mb-8">
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-[#6c757d] mb-2">Paper Title</label>
                <Input 
                  placeholder="Enter your paper title here"
                  className="bg-white border-gray-300"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[#6c757d] mb-2">Abstract</label>
                <Textarea 
                  placeholder="Paste your paper abstract here"
                  className="bg-white border-gray-300 min-h-32"
                  value={abstract}
                  onChange={(e) => setAbstract(e.target.value)}
                />
              </div>
              <div className="flex justify-center">
                <Button 
                  className="bg-[#8A9A85] hover:bg-[#7a8a75] text-white px-8 py-3" 
                  onClick={handleSubmit}
                  disabled={loading}
                >
                  {loading ? 'Evaluating...' : 'Evaluate Paper'}
                </Button>
                {error && (
                  <p className="text-red-500 text-sm mt-2 text-center">{error}</p>
                )}
              </div>
            </div>
          </div>

          {/* Three Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left Sidebar - Analysis & Filters */}
            <div className="lg:col-span-3 space-y-6 bg-white p-6 rounded-lg border border-gray-200">
              <h3 className="text-xl font-bold text-[#333333]">Analysis & Filters</h3>
              
              {/* Keywords Section */}
              <div className="space-y-3">
                <h4 className="font-semibold text-[#6c757d]">Keywords</h4>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary" className="bg-[#E9ECEF] text-[#333333] hover:bg-[#E9ECEF]">Machine Learning</Badge>
                  <Badge variant="secondary" className="bg-[#E9ECEF] text-[#333333] hover:bg-[#E9ECEF]">AI Ethics</Badge>
                  <Badge variant="secondary" className="bg-[#E9ECEF] text-[#333333] hover:bg-[#E9ECEF]">NLP</Badge>
                </div>
              </div>

              {/* Discipline Section */}
              <div className="space-y-3">
                <h4 className="font-semibold text-[#6c757d]">Discipline</h4>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Checkbox id="cs" defaultChecked />
                    <label htmlFor="cs" className="text-[#6c757d]">Computer Science</label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="is" />
                    <label htmlFor="is" className="text-[#6c757d]">Information Science</label>
                  </div>
                </div>
              </div>

              {/* Impact Factor Section */}
              <div className="space-y-3">
                <h4 className="font-semibold text-[#6c757d]">Impact Factor</h4>
                <div className="space-y-2">
                  <Slider
                    value={impactFactor}
                    onValueChange={setImpactFactor}
                    max={10}
                    min={0}
                    step={0.1}
                    className="w-full [&_[role=slider]]:bg-[#8A9A85] [&_[data-orientation=horizontal]]:bg-gray-200"
                  />
                  <div className="flex justify-between text-sm text-[#6c757d]">
                    <span>Low</span>
                    <span>High</span>
                  </div>
                </div>
              </div>

              {/* More Filters Section */}
              <div className="space-y-3">
                <h4 className="font-semibold text-[#6c757d]">More Filters</h4>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Checkbox id="oa" defaultChecked />
                    <label htmlFor="oa" className="text-[#6c757d]">Open Access</label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="q1" />
                    <label htmlFor="q1" className="text-[#6c757d]">Q1 Quartile</label>
                  </div>
                </div>
              </div>
            </div>

            {/* Middle Column - Journal Recommendations */}
            <div className="lg:col-span-6 space-y-6">
              <h3 className="text-xl font-bold text-[#333333]">Ranked Journal Recommendations</h3>
              
              <div className="space-y-4">
                {recommendations.length > 0 ? (
                  recommendations.map((journal, index) => (
                    <Card key={journal.issn} className={`p-6 ${getBgColor(index)} border-gray-200 relative`}>
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="w-8 h-8 bg-[#333333] text-white rounded-full flex items-center justify-center text-sm font-bold">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <h4 className="font-bold text-[#333333] mb-1">{journal.name}</h4>
                        <p className="text-sm text-[#6c757d] mb-2">{journal.publisher} • ISSN: {journal.issn}</p>
                        <div className="flex gap-4 text-sm text-[#6c757d] mb-2">
                          <span>Impact Factor: {journal.impact_factor.toFixed(3)}</span>
                          <span>Acceptance: {journal.acceptance_rate}%</span>
                        </div>
                        <a href={journal.url} target="_blank" rel="noopener noreferrer" className="text-[#5E705A] text-sm underline">Visit Journal</a>
                      </div>
                    </div>
                    <Bookmark className="w-5 h-5 text-gray-400 hover:text-[#6c757d] cursor-pointer" />
                  </div>
                </Card>

                {/* Journal Card 2 */}
                <Card className="p-6 bg-[#D4D9E2] border-gray-200 relative">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="w-8 h-8 bg-[#333333] text-white rounded-full flex items-center justify-center text-sm font-bold">
                        2
                      </div>
                      <div className="flex-1">
                        <h4 className="font-bold text-[#333333] mb-1">Journal of Machine Learning Research</h4>
                        <p className="text-sm text-[#6c757d] mb-2">JMLR • ISSN: 1533-7928</p>
                        <div className="flex gap-4 text-sm text-[#6c757d] mb-2">
                          <span>Impact Factor: 6.064</span>
                          <span>Acceptance: 22%</span>
                        </div>
                        <a href="#" className="text-[#5E705A] text-sm underline">Visit Journal</a>
                      </div>
                    </div>
                    <Bookmark className="w-5 h-5 text-gray-400 hover:text-[#6c757d] cursor-pointer" />
                  </div>
                </Card>

                {/* Journal Card 3 */}
                <Card className="p-6 bg-[#E5E2D9] border-gray-200 relative">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="w-8 h-8 bg-[#333333] text-white rounded-full flex items-center justify-center text-sm font-bold">
                        3
                      </div>
                      <div className="flex-1">
                        <h4 className="font-bold text-[#333333] mb-1">AI Magazine</h4>
                        <p className="text-sm text-[#6c757d] mb-2">AAAI • ISSN: 0738-4602</p>
                        <div className="flex gap-4 text-sm text-[#6c757d] mb-2">
                          <span>Impact Factor: 9.000</span>
                          <span>Acceptance: 35%</span>
                        </div>
                        <a href="#" className="text-[#5E705A] text-sm underline">Visit Journal</a>
                      </div>
                    </div>
                    <Bookmark className="w-5 h-5 text-gray-400 hover:text-[#6c757d] cursor-pointer" />
                  </div>
                </Card>

                {/* Journal Card 4 */}
                <Card className="p-6 bg-[#F2E2ED] border-gray-200 relative">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="w-8 h-8 bg-[#333333] text-white rounded-full flex items-center justify-center text-sm font-bold">
                        4
                      </div>
                      <div className="flex-1">
                        <h4 className="font-bold text-[#333333] mb-1">Ethics and Information Technology</h4>
                        <p className="text-sm text-[#6c757d] mb-2">Springer • ISSN: 1388-1957</p>
                        <div className="flex gap-4 text-sm text-[#6c757d] mb-2">
                          <span>Impact Factor: 3.955</span>
                          <span>Acceptance: 42%</span>
                        </div>
                        <a href="#" className="text-[#5E705A] text-sm underline">Visit Journal</a>
                      </div>
                    </div>
                    <Bookmark className="w-5 h-5 text-gray-400 hover:text-[#6c757d] cursor-pointer" />
                  </div>
                </Card>
              </div>
            </div>

            {/* Right Column - Paper-to-Journal Alignment */}
            <div className="lg:col-span-3 space-y-6">
              <h3 className="text-xl font-bold text-[#333333]">Paper-to-Journal Alignment</h3>
              
              {/* Radar Chart Placeholder */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <div className="relative w-full h-64 flex items-center justify-center">
                  {/* Simple radar chart visualization */}
                  <div className="relative w-48 h-48">
                    <svg viewBox="0 0 200 200" className="w-full h-full">
                      {/* Grid lines */}
                      <g stroke="#6c757d" strokeWidth="1" fill="none">
                        <circle cx="100" cy="100" r="80" />
                        <circle cx="100" cy="100" r="60" />
                        <circle cx="100" cy="100" r="40" />
                        <circle cx="100" cy="100" r="20" />
                        {/* Axis lines */}
                        <line x1="100" y1="20" x2="100" y2="180" />
                        <line x1="20" y1="100" x2="180" y2="100" />
                        <line x1="44" y1="44" x2="156" y2="156" />
                        <line x1="156" y1="44" x2="44" y2="156" />
                      </g>
                      {/* Data polygon */}
                      <polygon 
                        points="100,40 140,70 130,130 70,120 60,70" 
                        fill="#8A9A85" 
                        fillOpacity="0.3" 
                        stroke="#8A9A85" 
                        strokeWidth="2"
                      />
                      {/* Data points */}
                      <g fill="#8A9A85">
                        <circle cx="100" cy="40" r="3" />
                        <circle cx="140" cy="70" r="3" />
                        <circle cx="130" cy="130" r="3" />
                        <circle cx="70" cy="120" r="3" />
                        <circle cx="60" cy="70" r="3" />
                      </g>
                    </svg>
                    
                    {/* Labels */}
                    <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-2 text-xs text-[#6c757d]">
                      Topical Relevance
                    </div>
                    <div className="absolute top-1/4 right-0 transform translate-x-2 -translate-y-1/2 text-xs text-[#6c757d]">
                      Scope Match
                    </div>
                    <div className="absolute bottom-1/4 right-0 transform translate-x-2 translate-y-1/2 text-xs text-[#6c757d]">
                      Impact Alignment
                    </div>
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-4 text-xs text-[#6c757d]">
                      Audience Match
                    </div>
                    <div className="absolute top-1/4 left-0 transform -translate-x-8 -translate-y-1/2 text-xs text-[#6c757d]">
                      Methodology Fit
                    </div>
                  </div>
                </div>
                <p className="text-sm text-[#6c757d] text-center mt-4">
                  Hover over a journal to see its alignment score.
                </p>
              </div>
            </div>
          </div>

          {/* Load More Button */}
          <div className="flex justify-center mt-8 pb-8">
            <Button variant="outline" className="px-8 py-3 bg-white border-gray-300 text-[#333333] hover:bg-gray-50">
              Load More
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}