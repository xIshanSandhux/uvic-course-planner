import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';

const CourseSelect = () => {
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
      await axios.post("http://127.0.0.1:8000/courses_completed", { courses: selectedCourses });
      navigate("/chat", { state: { ...state, selectedCourses } });
    } catch (err) {
      alert("Failed to submit courses: " + err.message);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Select Courses</h2>
      <input
        type="text"
        placeholder="Search courses"
        className="w-full border p-2 mb-4"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="space-y-2">
        {filteredCourses.map(course => (
          <label key={course} className="block">
            <input
              type="checkbox"
              checked={selectedCourses.includes(course)}
              onChange={() => toggleCourse(course)}
              className="mr-2"
            />
            {course}
          </label>
        ))}
      </div>

      <h3 className="text-xl font-semibold mt-6">Your Selected Courses</h3>
      {selectedCourses.length > 0 ? (
        <ul className="list-disc pl-6">
          {selectedCourses.map(course => (
            <li key={course}>{course}</li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No courses selected yet.</p>
      )}

      <div className="flex gap-4 mt-6">
        <button className="px-6 py-2 bg-gray-500 text-white rounded" onClick={() => navigate(-1)}>
          Back
        </button>
        <button className="px-6 py-2 bg-blue-600 text-white rounded" onClick={handleSubmit}>
          Start Planning
        </button>
      </div>
    </div>
  );
};

export default CourseSelect;