export default function FooterLinks() {
  return (
    <footer className="py-8 px-6 mt-16">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-center gap-8 text-gray-500 font-medium" style={{ fontFamily: 'Poppins, sans-serif' }}>
          <a href="#" className="hover:text-gray-700 transition-colors">
            About
          </a>
          <a href="https://svkm.mapmyaccess.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-700 transition-colors">
            Papers
          </a>
          <a href="#" className="hover:text-gray-700 transition-colors">
            Privacy Policy
          </a>
          <span>© Journal Compass</span>
        </div>
      </div>
    </footer>
  );
}