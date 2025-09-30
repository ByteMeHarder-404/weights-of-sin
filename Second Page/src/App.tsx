import { JournalMatchDashboard } from './components/JournalMatchDashboard';

export default function App() {
  return (
    <div className="min-h-screen">
      {/* JournalMatch AI Dashboard */}
      <JournalMatchDashboard />
      
      {/* Footer Section */}
      <div className="bg-gray-50 flex items-center justify-center p-8">
        <div className="w-full max-w-6xl bg-[#F8F4EE] rounded-3xl shadow-lg p-12 relative">
          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
            {/* Left Content Area */}
            <div className="space-y-8">
              {/* Headline */}
              <h1 className="text-5xl font-bold text-gray-900 leading-tight">
                Navigate the World of Academic Publishing.
              </h1>
              
              {/* Body Text */}
              <p className="text-xl text-gray-700 leading-relaxed">
                Journal Compass analyzes your work to find the perfect home for your research, increasing your chances of acceptance.
              </p>
              
              {/* Separator Line */}
              <div className="w-full h-px bg-gray-600 my-8"></div>
              
              {/* Footer Links */}
              <div className="flex space-x-8">
                <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors">
                  Privacy Policy
                </a>
                <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors">
                  About Us
                </a>
                <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors">
                  Contact Us
                </a>
              </div>
            </div>
            
            {/* Right Content Area - Image Placeholder */}
            <div className="flex items-start justify-center">
              <div className="w-full max-w-md h-80 bg-white border-4 border-gray-800 rounded-3xl flex items-center justify-center shadow-sm">
                <span className="text-2xl text-gray-600">Journal Compass</span>
              </div>
            </div>
          </div>
          

        </div>
      </div>
    </div>
  );
}