import { ReactNode } from "react";

interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  backgroundColor: string;
  textColor?: string;
}

export default function FeatureCard({ 
  icon, 
  title, 
  description, 
  backgroundColor, 
  textColor = "text-gray-700" 
}: FeatureCardProps) {
  return (
    <div 
      className={`${backgroundColor} p-6 rounded-2xl h-56 flex flex-col transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 cursor-pointer`}
    >
      <div className="flex justify-start mb-4">
        <div className={`${textColor} opacity-80`}>
          {icon}
        </div>
      </div>
      <div className="flex-1 flex flex-col justify-between">
        <div>
          <h3 className={`${textColor} text-xl mb-3 font-bold leading-tight`} style={{ fontFamily: 'Lora, serif' }}>
            {title}
          </h3>
          <p className={`${textColor} opacity-75 text-sm leading-relaxed font-medium`} style={{ fontFamily: 'Poppins, sans-serif' }}>
            {description}
          </p>
        </div>
      </div>
    </div>
  );
}