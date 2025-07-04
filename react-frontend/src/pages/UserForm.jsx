import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const majors = [
  "Select a Major", "Software Engineering"
];

const years = ["Please Select an Option", "Year 1", "Year 2", "Year 3", "Year 4"];

export default function UserForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    major: "Select a Major",
    elective_courses: 0,
    core_courses: 0,
    degree_type: "Please Select an Option",
    student_status: "Please Select an Option",
    year: "Please Select an Option",
    coop_completed: 0,
  });

  const total_courses = form.core_courses + form.elective_courses;

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = async () => {
    if (form.major === "Select a Major") return alert("Please select a major");
    if (total_courses > 6) return alert("Total number of courses cannot exceed 6");

    console.log("📤 Submitting form data:", form); // log the form state

    try {
      const res = await axios.post("http://127.0.0.1:8000/extract_courses", { major: form.major });
      const courses = res.data;

      // console.log("✅ Extracted course list:", courses);
      // console.log("🚀 Course list response:", course_list_res.status);
      // console.log("✅ Course list response:", course_list_res);
      // console.log("✅ Sent course list to backend.");

      const target = form.student_status === "Yes" ? "/courses" : "/chat";

      const nextState = {
        ...form,
        courses
      };
      console.log(" Navigating to", target, "with state:", nextState);

      navigate(target, { state: nextState });

    } catch (err) {
      alert("Something went wrong: " + err.message);
      console.error("❌ Submission error:", err);
    }
  };

  return (
    <div className="flex min-h-screen w-screen bg-gradient-to-b from-blue-600 to-blue-900 text-white">
      <main className="flex-grow flex justify-center items-center px-6">
        <section className="bg-white bg-opacity-10 backdrop-blur-md rounded-2xl p-10 w-full max-w-2xl shadow-lg">
          <h2 className="text-4xl font-bold mb-6 text-center">Your Academic Details</h2>

          <div className="space-y-4 text-left text-sm">
            <div>
              <label className="block mb-1">Name</label>
              <input className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.name}
                onChange={e => handleChange('name', e.target.value)}
              />
            </div>

            <div>
              <label className="block mb-1">Select your major</label>
              <select className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.major}
                onChange={e => handleChange('major', e.target.value)}
              >
                {majors.map(m => <option key={m}>{m}</option>)}
              </select>
            </div>

            {/* <div>
              <label className="block mb-1">Enter your minor</label>
              <input className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.minor}
                onChange={e => handleChange('minor', e.target.value)}
              />
            </div> */}

            {/* <div>
              <label className="block mb-1">Specialization (optional)</label>
              <input className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.specialization}
                onChange={e => handleChange('specialization', e.target.value)}
              />
            </div> */}

            <div>
              <label className="block mb-1">How many courses do you want to take?</label>
              <input type="number" min="0" max="8" className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.core_courses}
                onChange={e => handleChange('core_courses', +e.target.value)}
              />
            </div>

            <div>
              <label className="block mb-1">How many elective courses do you want to take?</label>
              <input type="number" min="0" max="8" className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.elective_courses}
                onChange={e => handleChange('elective_courses', +e.target.value)}
              />
            </div>

            <div>
              <label className="block mb-1">Select your degree type</label>
              <select className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.degree_type}
                onChange={e => handleChange('degree_type', e.target.value)}
              >
                {["Please Select an Option", "Undergraduate", "Master", "PHD"].map(d => <option key={d}>{d}</option>)}
              </select>
            </div>

            <div>
              <label className="block mb-1">Have you completed any courses at UVic or have transfer credits for courses?</label>
              <select className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.student_status}
                onChange={e => handleChange('student_status', e.target.value)}
              >
                {["Please Select an Option", "Yes", "No"].map(d => <option key={d}>{d}</option>)}
              </select>
            </div>

            <div>
              <label className="block mb-1">What year are you in?</label>
              <select className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                value={form.year}
                onChange={e => handleChange('year', e.target.value)}
              >
                {years.map(y => <option key={y}>{y}</option>)}
              </select>
            </div>

            {/* {(form.year === "Year 2" || form.year === "Year 3" || form.year === "Year 4") && (
              <>
                <div>
                  <label className="block mb-1">Does your program support co-op?</label>
                  <select className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                    value={form.supports_coop}
                    onChange={e => handleChange('supports_coop', e.target.value)}
                  >
                    {["Please Select an Option", "Yes", "No"].map(op => <option key={op}>{op}</option>)}
                  </select>
                </div>

                {form.supports_coop === "Yes" && (
                  <>
                    <div>
                      <label className="block mb-1">How many co-op terms have you already completed?</label>
                      <input type="number" min="0" max="4"
                        className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                        value={form.coop_completed}
                        onChange={e => handleChange('coop_completed', +e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block mb-1">How many total co-op terms would you like to finish by graduation?</label>
                      <input type="number" min="0" max="4"
                        className="w-full rounded p-2 bg-white bg-opacity-80 text-black"
                        value={form.coop_planned}
                        onChange={e => handleChange('coop_planned', +e.target.value)}
                      />
                    </div>
                  </>
                )}
              </>
            )} */}
          </div>

          <button
            className="mt-6 w-full px-6 py-3 bg-yellow-400 text-blue-950 font-semibold rounded-full hover:bg-yellow-300 transition"
            onClick={handleNext}
          >
            Next
          </button>
        </section>
      </main>
    </div>
  );
}
