import { useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';
import ProgressTracker from '../components/ProgressTracker';
import CoursePlan from '../components/FS2-Course-Plan';
import useScrollToTop from '../hooks/useScrollToTop'; // Import hook

const renderOption = (value) => (
  <option
    key={value}
    value={value}
    disabled={value.includes("Please") || value.includes("Select")}
    className={value.includes("Please") || value.includes("Select") ? "italic text-gray-500" : ""}
  >
    {value}
  </option>
);

export default function FS2CoursePlan() {
  useScrollToTop(); // Scroll to top on mount

  const navigate = useNavigate();
  const { state } = useLocation(); // receives form data from FS1
  const [form, setForm] = useState(state);

  const total_courses = form.core_courses + form.elective_courses;

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = async () => {
    if (form.major === "Select a Major") return alert("Please select a major");
    if (total_courses > 8) return alert("Total number of courses cannot exceed 8");

    try {
      const res = await axios.post("http://127.0.0.1:8000/extract_courses", { major: form.major });
      const courses = res.data;

      await axios.post("http://127.0.0.1:8000/course_list", { courses });

      navigate("/courses", {
        state: {
          ...form,
          courses,
        }
      });
    } catch (err) {
      alert("Something went wrong: " + err.message);
      console.error("❌ Submission error:", err);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-screen bg-offwhite text-purple">
      <main className="flex-grow flex justify-center items-start px-6 py-6 pt-14 overflow-y-auto">
        <section className="bg-white rounded-2xl p-10 w-full max-w-2xl shadow-soft mb-10">
          <ProgressTracker currentStep={2} />

          <h2 className="text-4xl font-bold mb-9 text-center text-purple">
            Course Planning
          </h2>

          <div className="space-y-4 text-sm">
            <CoursePlan
              form={form}
              handleChange={handleChange}
              renderOption={renderOption}
            />
          </div>

          <div className="mt-6 flex justify-between gap-4">
            <button
              className="px-6 py-3 bg-gray-200 text-black font-semibold rounded-full hover:bg-gray-300 transition"
              onClick={() => navigate(-1)}
            >
              Back
            </button>

            <button
              className="ml-auto px-6 py-3 bg-accent text-white font-semibold rounded-full hover:text-black hover:bg-cyan transition shadow-soft"
              onClick={handleNext}
            >
              Next
            </button>
          </div>
        </section>
      </main>

      <footer className="bg-primary text-purple/60 py-4 text-center text-sm w-full">
        © {new Date().getFullYear()} UVic Course Planner
      </footer>
    </div>
  );
}
