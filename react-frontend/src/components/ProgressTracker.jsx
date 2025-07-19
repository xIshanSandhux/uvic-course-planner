export default function ProgressTracker({ currentStep }) {
  const steps = [
    { label: "Personal Info", id: 1 },
    { label: "Course Plan", id: 2 },
    { label: "Pre-requisites Completed", id: 3 },
  ];

  return (
    <div className="mb-10 relative px-4">
      {/* Circles + Labels */}
      <div className="flex justify-center relative z-10 gap-10 sm:gap-16">
        {steps.map((step, idx) => {
          const isActive = currentStep === step.id;
          const isCompleted = currentStep > step.id;

          return (
            <div key={step.id} className="flex flex-col items-center w-28 text-center">
              {/* Circle */}
              <div
                className={`w-10 h-10 flex items-center justify-center rounded-full border-4 text-sm font-semibold transition-all duration-500
                ${isActive ? 'bg-[#FF8811] text-white border-[#FF8811]' :
                  isCompleted ? 'bg-[#FF8811] text-white border-[#FF8811]' :
                    'bg-[#FFF8F0] text-gray-400 border-[#FFF8F0]'}`}
              >
                {step.id}
              </div>

              {/* Label */}
              <div className="mt-2 text-xs text-gray-700">
                {step.label}
              </div>
            </div>
          );
        })}
      </div>

      {/* Connecting Lines */}
      <div className="absolute top-[21px] left-1/2 transform -translate-x-1/2 w-[calc(100%-4rem)] max-w-[400px] flex justify-between z-0">
        {[0, 1].map((_, idx) => (
          <div
            key={idx}
            className={`h-1 flex-1 mx-2 transition-all duration-500
              ${currentStep > idx + 1 ? 'bg-[#FF8811]' : 'bg-[#FFF8F0]'}`}
          />
        ))}
      </div>
    </div>
  );
}
