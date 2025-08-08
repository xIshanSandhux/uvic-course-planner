import { useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';
import ProgressTracker from '../components/ProgressTracker';
import CoursePlan from '../components/FS2-Course-Plan';
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
          state: {
            ...form,
            courses,
          },
        });
      } else {
        navigate("/chat", {
          state: {
            ...form,
            selectedCourses: [],
            fullCourseList: courses,
          },
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
        <section className="bg-white rounded-2xl p-8 shadow-soft mb-10">
          <ProgressTracker currentStep={2} />

          <div className="space-y-4 text-sm mt-6">
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
      </div>
    </>
  );
}
