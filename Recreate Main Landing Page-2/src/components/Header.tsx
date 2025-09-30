import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="w-full px-6 py-6">
      <nav className="bg-white rounded-xl shadow-lg px-8 py-4 max-w-5xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <span className="text-gray-700 font-bold text-xl" style={{ fontFamily: 'Lora, serif' }}>
            Journal Compass
          </span>
        </div>
        
        {/* Center Navigation */}
        <div className="flex items-center">
          <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors font-medium px-4" style={{ fontFamily: 'Poppins, sans-serif' }}>
            About Us
          </a>
          <span className="text-gray-300">|</span>
          <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors font-medium px-4" style={{ fontFamily: 'Poppins, sans-serif' }}>
            GitHub
          </a>
          <span className="text-gray-300">|</span>
          <a href="https://svkm.mapmyaccess.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-gray-800 transition-colors font-medium px-4" style={{ fontFamily: 'Poppins, sans-serif' }}>
            Papers
          </a>
          <span className="text-gray-300">|</span>
          <a href="#" className="text-gray-600 hover:text-gray-800 transition-colors font-medium px-4" style={{ fontFamily: 'Poppins, sans-serif' }}>
            Privacy Policy
          </a>
        </div>
        
        {/* Analyze Button */}
        <Link to="/analyze" className="bg-[#8fac7e] hover:bg-[#7d9a6d] text-white px-6 py-2 rounded-md transition-colors font-medium" style={{ fontFamily: 'Poppins, sans-serif' }}>
          Analyze
        </Link>
      </nav>
    </header>
  );
}