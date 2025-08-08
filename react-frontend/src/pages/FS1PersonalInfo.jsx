import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ProgressTracker from '../components/ProgressTracker';
import useScrollToTop from '../hooks/useScrollToTop';

const majors = [
  "Software Engineering", "Computer Science", "Electrical Engineering",
  "Computer Engineering", "Biomedical Engineering", "Mechanical Engineering", "Civil Engineering"
];

const years = ["Please Select an Option", "Year 1", "Year 2", "Year 3", "Year 4"];

const majorSpecializations = {
  "Computer Science": [
    "Please Select an Option",
    "Computer Communications and Networks Option",
    "Computer Graphics and Gaming Option",
    "Software Systems Option",
    "Theory Option"
  ],
  "Software Engineering": [
    "Please Select an Option",
    "Embedded Systems Option",
    "Data Science Option",
    "Cybersecurity Option"
  ]
};

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
    major: "",
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

  const [showMajorSuggestions, setShowMajorSuggestions] = useState(false);

  const filteredMajors = majors.filter((m) =>
    form.major.toLowerCase().length === 0
      ? true
      : m.toLowerCase().includes(form.major.toLowerCase())
  );

  return (
    <>
      <div className="w-full max-w-2xl mx-auto px-6 pt-10 overflow-x-hidden">
        <section className="bg-white rounded-2xl p-8 shadow-soft mb-10">
          <ProgressTracker currentStep={1} />

          <div className="space-y-4 text-sm mt-6">
            {/* Full Name */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Full Name</label>
              <input
                className="w-full rounded p-2 bg-white text-black"
                value={form.name}
                onChange={(e) => handleChange("name", e.target.value)}
              />
            </div>

            {/* Student ID */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Student ID (optional)</label>
              <input
                className="w-full rounded p-2 bg-white text-black"
                value={form.student_id}
                onChange={(e) => handleChange("student_id", e.target.value)}
              />
            </div>

            {/* Program Level */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Program Level</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.degree_type}
                onChange={(e) => handleChange("degree_type", e.target.value)}
              >
                {["Please Select an Option", "Undergraduate", "Master", "PhD"].map(renderOption)}
              </select>
            </div>

            {/* Year */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Year of Study</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.year}
                onChange={(e) => handleChange("year", e.target.value)}
              >
                {years.map(renderOption)}
              </select>
            </div>

            {/* Faculty */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Faculty</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.faculty}
                onChange={(e) => handleChange("faculty", e.target.value)}
              >
                {[
                  "Please Select an Option",
                  "Engineering", "Science", "Social Sciences",
                  "Humanities", "Business", "Education", "Fine Arts"
                ].map(renderOption)}
              </select>
            </div>

            {/* Smart Major Input */}
            <div className="rounded-lg border border-dark bg-white p-3 relative">
              <label className="block mb-1">Major</label>
              <input
                type="text"
                placeholder="Start typing your major..."
                className="w-full rounded p-2 bg-white text-black"
                value={form.major}
                onChange={(e) => {
                  handleChange("major", e.target.value);
                  setShowMajorSuggestions(true);
                }}
                onFocus={() => setShowMajorSuggestions(true)}
                onBlur={() => setTimeout(() => setShowMajorSuggestions(false), 100)}
              />
              {showMajorSuggestions && filteredMajors.length > 0 && (
                <ul className="absolute z-10 bg-white border border-gray-300 rounded w-full max-h-48 overflow-auto mt-1 shadow-lg">
                  {filteredMajors.map((major) => (
                    <li
                      key={major}
                      onClick={() => {
                        handleChange("major", major);
                        setShowMajorSuggestions(false);
                      }}
                      className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                    >
                      {major}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Minor */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Minor (optional)</label>
              <input
                className="w-full rounded p-2 bg-white text-black"
                value={form.minor}
                onChange={(e) => handleChange("minor", e.target.value)}
              />
            </div>

            {/* Specialization */}
            {majorSpecializations[form.major] && (
              <div className="rounded-lg border border-dark bg-white p-3">
                <label className="block mb-1">Specialization (optional)</label>
                <select
                  className="w-full rounded p-2 bg-white text-black"
                  value={form.specialization}
                  onChange={(e) => handleChange("specialization", e.target.value)}
                >
                  {majorSpecializations[form.major].map(renderOption)}
                </select>
              </div>
            )}

            {/* Transfer Credit */}
            <div className="rounded-lg border border-dark bg-white p-3">
              <label className="block mb-1">Completed UVic courses or have transfer credits?</label>
              <select
                className="w-full rounded p-2 bg-white text-black"
                value={form.has_credits}
                onChange={(e) => handleChange("has_credits", e.target.value)}
              >
                {["Please Select an Option", "Yes", "No"].map(renderOption)}
              </select>
            </div>
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
    </>
  );
}
