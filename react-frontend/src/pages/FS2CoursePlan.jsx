import { useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';
import ProgressTracker from '../components/ProgressTracker';
import useScrollToTop from '../hooks/useScrollToTop';

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
  useScrollToTop();

  const navigate = useNavigate();
  const { state } = useLocation(); // receives form data from FS1
  const [form, setForm] = useState(state);

  const total_courses = form.core_courses + form.elective_courses;

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = async () => {
    if (form.major === "Select a Major")
      return alert("Please select a major");
    if (form.has_credits === "Please Select an Option")
      return alert("Please select if you have completed credits at UVic or have transfer credits");
    if (total_courses > 8)
      return alert("Total number of courses cannot exceed 8");

    try {
      const res = await axios.post("http://127.0.0.1:8000/extract_courses", {
        major: form.major,
      });

      if (!res.data.success) {
        return alert(res.data.error);
      }

      const courses = res.data.data;

      const res2 = await axios.post("http://127.0.0.1:8000/course_list", { courses });
      if (!res2.data.success) {
        return alert(res2.data.error);
      }

      if (form.has_credits === "Yes") {
        navigate("/courses", {
          state: { ...form, courses },
        });
      } else {
        navigate("/chat", {
          state: { ...form, selectedCourses: [], fullCourseList: courses },
        });
      }
    } catch (err) {
      alert("Something went wrong: " + err.message);
      console.error("❌ Submission error:", err);
    }
  };

  return (
    <>
      <div className="w-full max-w-2xl mx-auto px-6 pt-10 overflow-x-hidden">
        <section className="bg-white rounded-2xl p-8 shadow-soft mb-10 text-black">
          <ProgressTracker currentStep={2} />

          <div className="space-y-4 text-sm mt-6">
            {/* Number of core courses */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Number of core courses to take next term</label>
              <input
                type="number"
                min="0"
                max="8"
                className="w-full rounded p-2 bg-white text-black"
                value={form.core_courses}
                onChange={(e) => handleChange('core_courses', +e.target.value)}
              />
            </div>

            {/* Number of elective courses */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Number of elective courses to take next term</label>
              <input
                type="number"
                min="0"
                max="8"
                className="w-full rounded p-2 bg-white text-black"
                value={form.elective_courses}
                onChange={(e) => handleChange('elective_courses', +e.target.value)}
              />
            </div>

            {/* Preferred Class Times */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Preferred Class Times</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.class_times}
                onChange={(e) => handleChange('class_times', e.target.value)}
              >
                {["Please Select an Option", "Morning", "Afternoon", "Evening", "No Preference"].map(renderOption)}
              </select>
            </div>

            {/* Maximum Credits */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Maximum Credits per Term</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.max_credits}
                onChange={(e) => handleChange('max_credits', e.target.value)}
              >
                {[
                  "Please Select an Option",
                  "6 (Light Load - 4 courses)",
                  "7.5 (Full Load - 5 courses)",
                  "9 (Max Normal Load - 6 courses)",
                  "9+ (Overload - Approval Needed)"
                ].map(renderOption)}
              </select>
            </div>

            {/* Preferred Learning Style */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Preferred Learning Style</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.learning_style}
                onChange={(e) => handleChange('learning_style', e.target.value)}
              >
                {["Please Select an Option", "Project-based", "Lecture-focused", "Hands-on", "Balanced / Mixed"].map(renderOption)}
              </select>
              <small className="text-sm text-gray-500">
                Helps us prioritize courses that match your preferred format.
              </small>
            </div>

            {/* Delivery Preference */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Delivery Preference</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.delivery_mode}
                onChange={(e) => handleChange('delivery_mode', e.target.value)}
              >
                {[
                  "Please Select an Option",
                  "In-Person (on campus)",
                  "Online (fully remote)",
                  "Blended / Hybrid",
                  "No Preference"
                ].map(renderOption)}
              </select>
            </div>
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
      </div>
    </>
  );
}
