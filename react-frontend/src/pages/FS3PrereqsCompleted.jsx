import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';
import ProgressTracker from '../components/ProgressTracker';
import useScrollToTop from '../hooks/useScrollToTop';
import SidebarLayout from '../components/SidebarLayout';

export default function FS3PrereqsCompleted() {
  useScrollToTop();

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
      // console.log(selectedCourses);
      // const postCoursesCompleted = await axios.post("http://127.0.0.1:8000/courses_completed", {
      //   courses: selectedCourses,
      // });

      // console.log(postCoursesCompleted.data);

      // if (!postCoursesCompleted.data.success) {
      //   return alert(postCoursesCompleted.data.error);
      // }

      // console.log(courses);
      // const postCourseList = await axios.post("http://127.0.0.1:8000/course_list", {
      //   courses: courses,
      // });
      // console.log(postCourseList.data);
      // if (!postCourseList.data.success) {
      //   return alert(res2.data.error);
      // }

      // const postCoursesNotCompleted = await axios.post("http://127.0.0.1:8000/courses_not_completed");
      // console.log(postCoursesNotCompleted.data);
      // if (!postCoursesNotCompleted.data.success) {
      //   return alert(postCoursesNotCompleted.data.error);
      // }

      // const postPreReqCheck = await axios.post("http://127.0.0.1:8000/pre_req_check");
      // console.log(postPreReqCheck.data);
      // if (!postPreReqCheck.data.success) {
      //   return alert(postPreReqCheck.data.error);
      // }


      navigate("/chat", {
        state: {
          ...state,
          selectedCourses,
          fullCourseList: courses,
        }
      });
    } catch (err) {
      alert("❌ Failed to submit courses: " + err.message);
      console.error("Course submit error:", err);
    }
  };

  return (
    <SidebarLayout>
      <main className="flex-grow flex justify-center items-start px-6 pt-14 overflow-y-auto">
        <section className="bg-white rounded-2xl p-10 w-full max-w-2xl shadow-soft mb-10">
          <ProgressTracker currentStep={3} />

          {/* Search Field */}
          <div className="mb-6">
            <label className="block mb-2 text-sm font-medium">Search Courses</label>
            <input
              type="text"
              placeholder="Search by course code or title"
              className="w-full p-2 rounded border text-black bg-white"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          {/* Course Selection */}
          <div className="space-y-2 max-h-64 overflow-y-auto pr-2 mb-6">
            {filteredCourses.map(course => (
              <label
                key={course}
                className="flex items-center text-sm bg-gray-100 p-2 rounded hover:bg-gray-200 transition"
              >
                <input
                  type="checkbox"
                  checked={selectedCourses.includes(course)}
                  onChange={() => toggleCourse(course)}
                  className="mr-3 accent-accent"
                />
                <span className="text-black">{course}</span>
              </label>
            ))}
          </div>

          {/* Selected Courses Summary */}
          <div className="pt-4 border-t border-gray-200 mb-6">
            <h3 className="text-xl font-semibold mb-2">Your Selected Courses</h3>
            {selectedCourses.length > 0 ? (
              <ul className="list-disc list-inside text-purple text-sm space-y-1">
                {selectedCourses.map(course => (
                  <li key={course}>{course}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No courses selected yet.</p>
            )}
          </div>

          {/* Buttons */}
          <div className="flex justify-between mt-6">
            <button
              className="px-6 py-3 bg-gray-200 text-black font-semibold rounded-full hover:bg-gray-300 transition"
              onClick={() => navigate(-1)}
            >
              Back
            </button>
            <button
              className="px-6 py-3 bg-accent text-white font-semibold rounded-full hover:text-black hover:bg-cyan transition shadow-soft"
              onClick={handleSubmit}
            >
              Begin Chat
            </button>
          </div>
        </section>
      </main>
    </SidebarLayout>
  );
}