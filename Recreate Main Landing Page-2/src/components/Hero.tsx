import { Link } from 'react-router-dom';

export default function Hero() {
  return (
    <section className="text-center py-16 px-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-6xl text-gray-800 mb-6 font-bold" style={{ fontFamily: 'Lora, serif' }}>
          Journal Compass
        </h1>
        <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto font-medium" style={{ fontFamily: 'Poppins, sans-serif' }}>
          Point your research toward the journals that fit best.
        </p>
        <Link to="/analyze" className="bg-[#8fac7e] hover:bg-[#7d9a6d] text-white px-8 py-4 rounded-full text-lg transition-colors font-semibold" style={{ fontFamily: 'Poppins, sans-serif' }}>
          Analyze Your Paper Now
        </Link>
      </div>
    </section>
  );
}