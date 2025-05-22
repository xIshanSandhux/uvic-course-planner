import { useNavigate } from 'react-router-dom';

const Landing = () => {
  const navigate = useNavigate();

  console.log(import.meta.env.VITE_COHERE_API_KEY)

  return (
    <div className="min-h-screen flex flex-col justify-center items-center text-center p-8">
      <h1 className="text-4xl font-bold mb-6">UVic Course Planner 🎓</h1>
      <p className="mb-4 text-lg max-w-xl">
        Welcome to the UVic Course Planner, an AI-powered assistant to help you:
        <ul className="list-disc text-left mt-2 ml-5">
          <li>Pick your courses smartly</li>
          <li>Avoid conflicts in schedule</li>
          <li>Get suggestions based on your interests</li>
          <li>Generate and export timetables easily</li>
        </ul>
      </p>
      <button
        className="mt-6 px-6 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
        onClick={() => navigate("/form")}
      >
        Start Planning
      </button>
    </div>
  );
};


export default Landing;
