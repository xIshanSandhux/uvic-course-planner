import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';

export default function CourseSelect() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [search, setSearch] = useState("");
  const courses = state?.courses || [];

  const filteredCourses = search
    ? courses.filter(course => course.toLowerCase().includes(search.toLowerCase()))
    : courses;

  const toggleCourse = (course) => {
    setSelectedCourses(prev =>
      prev.includes(course)
        ? prev.filter(c => c !== course)
        : [...prev, course]
    );
  };

  const handleSubmit = async () => {
    try {
      // 1. POST selected (completed) courses
      await axios.post("http://127.0.0.1:8000/courses_completed", {
        courses: selectedCourses,
      });

      // 2. POST full course list (based on extracted major)
      await axios.post("http://127.0.0.1:8000/course_list", {
        courses: courses,
      });

      // 3. Navigate to chatbot with all relevant state
      console.log("Navigating to /chat with state:", {
        ...state,
        selectedCourses,
        fullCourseList: courses
      });
      navigate("/chat", {
        state: {
          ...state, // name, major, minor, etc. from UserForm
          selectedCourses, // specifically completed ones
          fullCourseList: courses, // can optionally use in Chatbot.jsx prompt too
        }
      });
    } catch (err) {
      alert("❌ Failed to submit courses: " + err.message);
      console.error("Course submit error:", err);
    }
  };

  console.log("selectedCourses being sent:", selectedCourses);
  console.log("courses being sent as fullCourseList:", courses);

  return (
    <div className="flex min-h-screen w-screen bg-gradient-to-b from-blue-600 to-blue-900 text-white">
      <main className="flex-grow flex justify-center items-center px-6">
        <section className="bg-white bg-opacity-10 backdrop-blur-md rounded-2xl p-10 w-full max-w-3xl shadow-lg">
          <h2 className="text-4xl font-bold mb-6 text-center">Select Your Courses</h2>

          <div className="mb-6">
            <label className="block mb-2 text-sm font-medium">Search Courses</label>
            <input
              type="text"
              placeholder="Search by course code or title"
              className="w-full p-2 rounded bg-white bg-opacity-80 text-black"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="space-y-2 max-h-64 overflow-y-auto pr-2 mb-6">
            {filteredCourses.map(course => (
              <label
                key={course}
                className="flex items-center text-sm bg-white bg-opacity-20 p-2 rounded hover:bg-opacity-30 transition"
              >
                <input
                  type="checkbox"
                  checked={selectedCourses.includes(course)}
                  onChange={() => toggleCourse(course)}
                  className="mr-3 accent-yellow-400"
                />
                <span className="text-white">{course}</span>
              </label>
            ))}
          </div>

          <div className="mb-6">
            <h3 className="text-xl font-semibold mb-2">Your Selected Courses</h3>
            {selectedCourses.length > 0 ? (
              <ul className="list-disc list-inside text-yellow-300 text-sm">
                {selectedCourses.map(course => (
                  <li key={course}>{course}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-200">No courses selected yet.</p>
            )}
          </div>

          <div className="flex gap-4 justify-center mt-4">
            <button
              className="px-6 py-2 bg-gray-400 text-white rounded-full hover:bg-gray-300 transition"
              onClick={() => navigate(-1)}
            >
              Back
            </button>
            <button
              className="px-6 py-2 bg-yellow-400 text-blue-950 font-semibold rounded-full hover:bg-yellow-300 transition"
              onClick={handleSubmit}
            >
              Start Planning
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
