export default function ProgressTracker({ currentStep }) {
  const steps = [
    { label: "Personal Info", id: 1 },
    { label: "Course Plan", id: 2 },
    { label: "Prereqs Completed", id: 3 },
  ];

  return (
    <div className="flex justify-center items-center mb-10">
      {steps.map((step, idx) => {
        const isActive = currentStep === step.id;
        const isCompleted = currentStep > step.id;

        return (
          <div key={step.id} className="flex items-center">
            {/* Circle */}
            <div
              className={`w-10 h-10 flex items-center justify-center rounded-full border-4 text-sm font-semibold transition-all duration-500 
                ${isActive ? 'bg-[#FF8811] text-white border-[#FF8811]' :
                isCompleted ? 'bg-[#FF8811] text-white border-[#FF8811]' :
                'bg-[#FFF8F0] text-gray-400 border-[#FFF8F0]'}`}
            >
              {step.id}
            </div>

            {/* Line to next step */}
            {idx < steps.length - 1 && (
              <div
                className={`w-16 h-1 transition-all duration-500 
                  ${currentStep > step.id ? 'bg-[#FF8811]' : 'bg-[#FFF8F0]'}`}
              ></div>
            )}
          </div>
        );
      })}
    </div>
  );
}
