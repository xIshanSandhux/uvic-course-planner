import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ProgressTracker from '../components/ProgressTracker';
import useScrollToTop from '../hooks/useScrollToTop';
import SidebarLayout from '../components/SidebarLayout';

const majors = [
  "Select a Major", "Software Engineering", "Computer Science", "Electrical Engineering",
  "Computer Engineering", "Biomedical Engineering", "Mechanical Engineering", "Civil Engineering"
];

const years = ["Please Select an Option", "Year 1", "Year 2", "Year 3", "Year 4"];

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

export default function FS1PersonalInfo() {
  useScrollToTop();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    student_id: "",
    degree_type: "Please Select an Option",
    year: "Please Select an Option",
    faculty: "",
    major: "Select a Major",
    double_major: "",
    minor: "",
    specialization: "",
    has_credits: "Please Select an Option",
    core_courses: 0,
    elective_courses: 0,
    class_times: "Please Select an Option",
    max_credits: "Please Select an Option",
    learning_style: "Please Select an Option",
    delivery_mode: "Please Select an Option",
    supports_coop: "Please Select an Option",
    coop_completed: 0,
    coop_planned: 0,
  });

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  return (
    <SidebarLayout>
      <div className="w-full max-w-2xl mx-auto px-6 py-10 overflow-x-hidden">
        <section className="bg-white rounded-2xl p-8 shadow-soft mb-10">
          <ProgressTracker currentStep={1} />

          <div className="space-y-4 text-sm mt-6">
            {/* Input Fields */}
            {[
              {
                label: "Full Name",
                type: "input",
                field: "name"
              },
              {
                label: "Student ID",
                type: "input",
                field: "student_id"
              },
              {
                label: "Program Level",
                type: "select",
                field: "degree_type",
                options: ["Please Select an Option", "Undergraduate", "Master", "PhD"]
              },
              {
                label: "Year of Study",
                type: "select",
                field: "year",
                options: years
              },
              {
                label: "Faculty",
                type: "select",
                field: "faculty",
                options: [
                  "Please Select an Option",
                  "Engineering", "Science", "Social Sciences",
                  "Humanities", "Business", "Education", "Fine Arts"
                ]
              },
              {
                label: "Major",
                type: "select",
                field: "major",
                options: majors
              },
              {
                label: "Minor (optional)",
                type: "input",
                field: "minor"
              },
              {
                label: "Specialization (optional)",
                type: "input",
                field: "specialization"
              },
              {
                label: "Completed UVic courses or have transfer credits?",
                type: "select",
                field: "has_credits",
                options: ["Please Select an Option", "Yes", "No"]
              }
            ].map(({ label, type, field, options }) => (
              <div key={field} className="rounded-lg border border-dark bg-white p-3">
                <label className="block mb-1">{label}</label>
                {type === "input" ? (
                  <input
                    className="w-full rounded p-2 bg-white text-black"
                    value={form[field]}
                    onChange={e => handleChange(field, e.target.value)}
                  />
                ) : (
                  <select
                    className="w-full rounded p-2 bg-white text-black"
                    value={form[field]}
                    onChange={e => handleChange(field, e.target.value)}
                  >
                    {options.map(renderOption)}
                  </select>
                )}
              </div>
            ))}
          </div>

          {/* Navigation Buttons */}
          <div className="mt-6 flex justify-between">
            <button
              className="px-6 py-3 bg-gray-200 text-black font-semibold rounded-full hover:bg-gray-300 transition"
              onClick={() => navigate('/')}
            >
              Back
            </button>

            <button
              className="ml-auto px-6 py-3 bg-accent text-white font-semibold rounded-full hover:text-black hover:bg-cyan transition shadow-soft"
              onClick={() => navigate('/form/plan', { state: form })}
            >
              Next
            </button>
          </div>
        </section>
      </div>
    </SidebarLayout>
  );
}
