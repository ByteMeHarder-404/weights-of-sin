import Header from "../components/Header";
import Hero from "../components/Hero";
import KeyFeatures from "../components/KeyFeatures";
import AboutUs from "../components/AboutUs";
import FooterLinks from "../components/FooterLinks";
import { Waves } from "../components/ui/waves-background";

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden flex flex-col" style={{ backgroundColor: '#FFDAB9' }}>
      {/* Waves Background */}
      <Waves 
        className="absolute inset-0 z-0" 
        lineColor="rgba(143, 172, 126, 0.3)"
        waveSpeedX={0.015}
        waveSpeedY={0.01}
        waveAmpX={50}
        waveAmpY={25}
      />

      {/* Main Content (with a higher z-index) */}
      <div className="relative z-10 flex-1">
        <Header />
        <Hero />
        <KeyFeatures />
        <div className="mt-16 w-full">
          <AboutUs />
        </div>
      </div>
      <div className="relative z-10">
        <FooterLinks />
      </div>
    </div>
  );
}