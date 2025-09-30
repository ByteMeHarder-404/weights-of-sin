<<<<<<< HEAD
````markdown
# 📖 Journal Compass  
=======
# Journal Compass  
>>>>>>> fix-openalex

Journal Compass is a modern, two-page web application designed to help researchers find the **perfect journal** for their work.  
Built for the **Hackops 2.5 hackathon**, it combines a sleek UI with an integrated **JournalMatch AI** engine that analyzes a research paper’s title and abstract to recommend the most suitable journals.  

---

##  Features  

- 🎨 **Interactive Wave Background** — An engaging background that subtly reacts to user mouse movement.  
- 🧭 **Two-Page Application** — Clean client-side routing between the landing page and the `/analyze` page with React Router.  
- 📱 **Responsive Design** — A modern, minimal UI that looks great on desktops, tablets, and mobile devices.  
- 🧩 **Component-Based Architecture** — Built using a clean, reusable component structure inspired by [shadcn/ui](https://ui.shadcn.com/).  
- ⚡ **Modern Tech Stack** — Powered by **React, Vite, TypeScript, and Tailwind CSS** for speed and scalability.  
- 🤖 **JournalMatch AI** *(demo-ready)* — Upload your title + abstract and receive intelligent journal recommendations (powered by RAG & OpenAlex).  

---

<<<<<<< HEAD
## Tech Stack  
=======
##  Tech Stack  
>>>>>>> fix-openalex

- **Framework:** React (with TypeScript)  
- **Build Tool:** Vite  
- **Styling:** Tailwind CSS  
- **UI Components:** Custom, based on shadcn/ui  
- **Routing:** React Router DOM  
- **Icons:** [Lucide React](https://lucide.dev/)  
- **Animations:** Custom CSS & hooks + [@tsparticles/react](https://particles.js.org/)  
- **Backend/ML Integration (planned):** Node.js, Python, ChromaDB, OpenAlex API  

---

##  Getting Started  

Follow these steps to set up the project locally.  

### ✅ Prerequisites  
- [Node.js](https://nodejs.org/) **v18.x+**  
- npm **v9+**  

<<<<<<< HEAD
### ⚙️ Installation  

---

## Project Structure
=======
### ⚙️ Project Structure  

>>>>>>> fix-openalex
```bash
# Clone the repository
git clone https://your-repository-url.git
cd journal-compass

# Install dependencies
npm install

# Start the development server
npm run dev


<<<<<<< HEAD
=======
---
>>>>>>> fix-openalex
/
├── public/                 # Static assets
└── src/
    ├── components/         # Reusable React components
    │   ├── ui/             # Core UI elements (Button, Card, waves-background.tsx)
    │   ├── AboutUs.tsx
    │   ├── Header.tsx
    │   ├── Hero.tsx
    │   └── TeamCard.tsx
    ├── pages/              # Page-level components
    │   ├── LandingPage.tsx
    │   └── SecondPage.tsx  # /analyze page
    ├── App.tsx             # Router configuration
    ├── index.css           # Global styles & Tailwind directives
    └── main.tsx            # App entry point
├── package.json            # Dependencies & scripts
└── tailwind.config.js      # Tailwind configuration
