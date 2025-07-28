import { useState } from 'react';

export default function PersonalInfo({ form, handleChange, renderOption, majors, years }) {
  const [majorQuery, setMajorQuery] = useState('');
  const [showMajorSuggestions, setShowMajorSuggestions] = useState(false);

  const filteredMajors =
    majorQuery.trim() === ''
      ? majors
      : majors.filter((major) =>
          major.toLowerCase().includes(majorQuery.toLowerCase())
        );

  const handleMajorSelect = (value) => {
    handleChange('major', value);
    setMajorQuery(value);
    setShowMajorSuggestions(false);
  };
  
  return (
    <div className="w-full overflow-x-hidden">
      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Full Name</label>
        <input
          className="w-full rounded p-2 bg-white text-black"
          value={form.name}
          onChange={e => handleChange('name', e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Student ID (optional)</label>
        <input
          className="w-full rounded p-2 bg-white text-black"
          value={form.student_id}
          onChange={e => handleChange('student_id', e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Program Level</label>
        <select
          className="w-full rounded p-2 bg-white text-black"
          value={form.degree_type}
          onChange={e => handleChange('degree_type', e.target.value)}
        >
          {["Please Select an Option", "Undergraduate", "Master", "PhD"].map(renderOption)}
        </select>
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Year of Study</label>
        <select
          className="w-full rounded p-2 bg-white text-black"
          value={form.year}
          onChange={e => handleChange('year', e.target.value)}
        >
          {years.map(renderOption)}
        </select>
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Faculty</label>
        <select
          className="w-full rounded p-2 bg-white text-black"
          value={form.faculty}
          onChange={e => handleChange('faculty', e.target.value)}
        >
          {[
            "Please Select an Option",
            "Engineering", "Science", "Social Sciences",
            "Humanities", "Business", "Education", "Fine Arts"
          ].map(renderOption)}
        </select>
      </div>

      <div className="rounded-lg border border-dark bg-white p-3 relative">
        <label className="block mb-1">Major</label>
        <input
          className="w-full rounded p-2 bg-white text-black"
          placeholder="Start typing your major..."
          value={majorQuery}
          onChange={(e) => {
            setMajorQuery(e.target.value);
            setShowMajorSuggestions(true);
            handleChange('major', e.target.value); // optional sync
          }}
          onFocus={() => setShowMajorSuggestions(true)}
          onBlur={() => setTimeout(() => setShowMajorSuggestions(false), 100)} // allow click
        />
        {showMajorSuggestions && filteredMajors.length > 0 && (
          <ul className="absolute z-10 bg-white border border-gray-300 rounded w-full max-h-48 overflow-auto mt-1 shadow-lg">
            {filteredMajors.map((major) => (
              <li
                key={major}
                onClick={() => handleMajorSelect(major)}
                className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              >
                {major}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Double Major / Combined Program (optional)</label>
        <input
          className="w-full rounded p-2 bg-white text-black"
          value={form.double_major}
          onChange={e => handleChange('double_major', e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Minor (optional)</label>
        <input
          className="w-full rounded p-2 bg-white text-black"
          value={form.minor}
          onChange={e => handleChange('minor', e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Specialization (optional)</label>
        <input
          className="w-full rounded p-2 bg-white text-black"
          value={form.specialization}
          onChange={e => handleChange('specialization', e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">UVic or Transfer Credits</label>
        <select
          className="w-full rounded p-2 bg-white text-black"
          value={form.student_status}
          onChange={e => handleChange('student_status', e.target.value)}
        >
          {["Please Select an Option", "Yes", "No"].map(renderOption)}
        </select>
      </div>
    </div>
  );
}
