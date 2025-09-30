import { Search, BarChart3, FileText, Globe } from "lucide-react";
import FeatureCard from "./FeatureCard";

export default function KeyFeatures() {
  const features = [
    {
      icon: <Search className="w-8 h-8" />,
      title: "Smart Matching",
      description: "Our AI recommends journals based on your paper's content.",
      backgroundColor: "bg-[#f5f3e7]", // cream/yellow
      textColor: "text-gray-700"
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: "Impact Metrics",
      description: "View crucial metrics like impact factor and acceptance rates.",
      backgroundColor: "bg-[#d4d8e1]", // blue-gray
      textColor: "text-gray-700"
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: "Submission Guidelines",
      description: "Quick access to publisher submission requirements.",
      backgroundColor: "bg-[#e8e0d5]", // tan/beige
      textColor: "text-gray-700"
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: "Interdisciplinary Insights",
      description: "Discover relevant journals across diverse academic fields.",
      backgroundColor: "bg-[#e8d8e8]", // pink/purple
      textColor: "text-gray-700"
    }
  ];

  return (
    <section className="py-16 px-6">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl text-gray-800 text-center mb-12 font-bold" style={{ fontFamily: 'Lora, serif' }}>
          Key Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <FeatureCard
              key={`feature-${index}`}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              backgroundColor={feature.backgroundColor}
              textColor={feature.textColor}
            />
          ))}
        </div>
      </div>
    </section>
  );
}