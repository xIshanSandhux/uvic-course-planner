export default function CoursePlan({ form, handleChange, renderOption }) {
  return (
    <>
      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Number of core courses to take next term</label>
        <input type="number" min="0" max="8" className="w-full rounded p-2 bg-white text-black"
          value={form.core_courses}
          onChange={e => handleChange('core_courses', +e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Number of elective courses to take next term</label>
        <input type="number" min="0" max="8" className="w-full rounded p-2 bg-white text-black"
          value={form.elective_courses}
          onChange={e => handleChange('elective_courses', +e.target.value)}
        />
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Preferred Class Times</label>
        <select className="w-full rounded p-2 bg-white text-black"
          value={form.class_times}
          onChange={e => handleChange('class_times', e.target.value)}
        >
          {["Please Select an Option", "Morning", "Afternoon", "Evening", "No Preference"].map(renderOption)}
        </select>
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Maximum Credits per Term</label>
        <select className="w-full rounded p-2 bg-white text-black"
          value={form.max_credits}
          onChange={e => handleChange('max_credits', e.target.value)}
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

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Preferred Learning Style</label>
        <select className="w-full rounded p-2 bg-white text-black"
          value={form.learning_style}
          onChange={e => handleChange('learning_style', e.target.value)}
        >
          {["Please Select an Option", "Project-based", "Lecture-focused", "Hands-on", "Balanced / Mixed"].map(renderOption)}
        </select>
        <small className="text-sm text-muted">Helps us prioritize courses that match your preferred format.</small>
      </div>

      <div className="rounded-lg border border-dark bg-white p-3">
        <label className="block mb-1">Delivery Preference</label>
        <select className="w-full rounded p-2 bg-white text-black"
          value={form.delivery_mode}
          onChange={e => handleChange('delivery_mode', e.target.value)}
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
    </>
  );
}
