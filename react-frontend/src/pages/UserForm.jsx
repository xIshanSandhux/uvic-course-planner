import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const majors = [
  "Select a Major", "Software Engineering", "Computer Science", "Electrical Engineering",
  "Computer Engineering", "Biomedical Engineering", "Mechanical Engineering", "Civil Engineering"
];

const years = ["Please Select an Option", "Year 1", "Year 2", "Year 3", "Year 4"];

const UserForm = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    major: "Select a Major",
    minor: "",
    specialization: "",
    core_courses: 0,
    elective_courses: 0,
    degree_type: "Please Select an Option",
    student_status: "Please Select an Option",
    year: "Please Select an Option",
    supports_coop: "Please Select an Option",
    coop_completed: 0,
    coop_planned: 0,
  });

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

      if (form.student_status === "Yes") {
        navigate("/courses", { state: { ...form, courses } });
      } else {
        navigate("/chat", { state: { ...form, courses } });
      }
    } catch (err) {
      alert("Something went wrong: " + err.message);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6">User Details</h2>
      <div className="space-y-4">
        <input className="w-full border p-2" placeholder="Name" value={form.name} onChange={e => handleChange('name', e.target.value)} />
        <select className="w-full border p-2" value={form.major} onChange={e => handleChange('major', e.target.value)}>
          {majors.map(m => <option key={m}>{m}</option>)}
        </select>
        <input className="w-full border p-2" placeholder="Minor (optional)" value={form.minor} onChange={e => handleChange('minor', e.target.value)} />
        <input className="w-full border p-2" placeholder="Specialization (optional)" value={form.specialization} onChange={e => handleChange('specialization', e.target.value)} />

        <div className="flex gap-4">
          <input type="number" min="0" max="8" className="w-full border p-2" placeholder="# Core Courses" value={form.core_courses} onChange={e => handleChange('core_courses', +e.target.value)} />
          <input type="number" min="0" max="8" className="w-full border p-2" placeholder="# Electives" value={form.elective_courses} onChange={e => handleChange('elective_courses', +e.target.value)} />
        </div>

        <select className="w-full border p-2" value={form.degree_type} onChange={e => handleChange('degree_type', e.target.value)}>
          {["Please Select an Option", "Undergraduate", "Master", "PHD"].map(d => <option key={d}>{d}</option>)}
        </select>

        <select className="w-full border p-2" value={form.student_status} onChange={e => handleChange('student_status', e.target.value)}>
          {["Please Select an Option", "Yes", "No"].map(d => <option key={d}>{d}</option>)}
        </select>

        <select className="w-full border p-2" value={form.year} onChange={e => handleChange('year', e.target.value)}>
          {years.map(y => <option key={y}>{y}</option>)}
        </select>

        {(form.year === "Year 2" || form.year === "Year 3" || form.year === "Year 4") && (
          <>
            <select className="w-full border p-2" value={form.supports_coop} onChange={e => handleChange('supports_coop', e.target.value)}>
              {["Please Select an Option", "Yes", "No"].map(op => <option key={op}>{op}</option>)}
            </select>
            {form.supports_coop === "Yes" && (
              <div className="flex gap-4">
                <input type="number" min="0" max="4" className="w-full border p-2" placeholder="# Co-op Completed" value={form.coop_completed} onChange={e => handleChange('coop_completed', +e.target.value)} />
                <input type="number" min="0" max="4" className="w-full border p-2" placeholder="# Co-op Planned" value={form.coop_planned} onChange={e => handleChange('coop_planned', +e.target.value)} />
              </div>
            )}
          </>
        )}
      </div>

      <button
        className="mt-6 px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        onClick={handleNext}
      >
        Next
      </button>
    </div>
  );
};

export default UserForm;