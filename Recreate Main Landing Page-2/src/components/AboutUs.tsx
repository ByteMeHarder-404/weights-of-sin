import { MapPin, Code, Palette, Database, BrainCircuit, Lightbulb } from "lucide-react";
import TeamCard from "./TeamCard";

function AboutUs() {
  const teamMembers = [
    {
      name: "Atharva Deo",
      description: "Crafting intuitive and engaging user experiences on websites.",
      tags: [
        { icon: <MapPin className="w-4 h-4" />, text: "Mumbai" },
        { icon: <Code className="w-4 h-4" />, text: "Frontend Developer" },
        { icon: <Palette className="w-4 h-4" />, text: "React" }
      ]
    },
    {
      name: "Bhavik Seth",
      description: "Building fast, responsive, and beautiful web applications from DJSCE.",
      tags: [
        { icon: <MapPin className="w-4 h-4" />, text: "Mumbai" },
        { icon: <Database className="w-4 h-4" />, text: "Backend Developer" },
        { icon: <Code className="w-4 h-4" />, text: "Node" }
      ]
    },
    {
      name: "Dravvya Jain",
      description: "Uncovering insights and telling stories with data in India.",
      tags: [
        { icon: <MapPin className="w-4 h-4" />, text: "Mumbai" },
        { icon: <BrainCircuit className="w-4 h-4" />, text: "Data Science" },
        { icon: <Code className="w-4 h-4" />, text: "Python & R" }
      ]
    },
    {
      name: "Akshat Bhalani",
      description: "Understanding machine needs and advocating for human computer interaction in India.",
      tags: [
        { icon: <MapPin className="w-4 h-4" />, text: "Mumbai" },
        { icon: <BrainCircuit className="w-4 h-4" />, text: "ML Ops" },
        { icon: <Lightbulb className="w-4 h-4" />, text: "GenAI" }
      ]
    }
  ];

  return (
    <section className="py-16 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-5xl text-gray-800 mb-4 font-bold" style={{ fontFamily: 'Lora, serif' }}>
            About Our Team
          </h2>
          <p 
            className="text-lg text-gray-600 max-w-3xl mx-auto font-medium" 
            style={{ fontFamily: 'Poppins, sans-serif' }}
          >
            We are a collective of passionate creators, developers, and strategists dedicated to pushing the boundaries of digital interaction.
          </p>
        </div>

        {/* Team Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
          {teamMembers.map((member, index) => (
            <TeamCard key={`team-${index}`} {...member} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default AboutUs;