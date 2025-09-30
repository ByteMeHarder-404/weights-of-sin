import { ReactNode } from "react";

interface TeamCardProps {
  name: string;
  description: string;
  tags: {
    icon: ReactNode;
    text: string;
  }[];
}

export default function TeamCard({ name, description, tags }: TeamCardProps) {
  return (
    <div className="rounded-xl border border-gray-300 bg-white/50 backdrop-blur-sm p-8 h-auto min-h-[280px] flex flex-col transition-shadow duration-300 hover:shadow-xl cursor-pointer">
      <div className="flex-1">
        <h3 className="text-2xl text-gray-800 mb-4 font-bold leading-tight" style={{ fontFamily: 'Lora, serif' }}>
          {name}
        </h3>
        <p className="text-gray-600 mb-6 leading-relaxed font-medium" style={{ fontFamily: 'Poppins, sans-serif' }}>
          {description}
        </p>
      </div>
      <div className="flex flex-wrap gap-2 mt-auto">
        {tags.map((tag, index) => (
          <div 
            key={index}
            className="flex items-center gap-1.5 rounded-full px-3 py-2 text-sm border border-gray-200 bg-white/80 font-medium"
            style={{ fontFamily: 'Poppins, sans-serif' }}
          >
            <div className="text-gray-500">
              {tag.icon}
            </div>
            <span className="text-gray-700">{tag.text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}