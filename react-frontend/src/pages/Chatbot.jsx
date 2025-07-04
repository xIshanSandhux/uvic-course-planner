import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

export default function Chatbot() {
  const { state } = useLocation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [fullCourseList, setFullCourseList] = useState([]);
  const [notCompleted, setNotCompleted] = useState([]);
  const [courseData, setCourseData] = useState({
    completed: "",      // ← array, so .join() is safe
    courseList: "",
    notComp: []
  });

  useEffect(() => {
    const fetchCourseContext = async () => {
      const [compRes, listRes, notCompRes] = await Promise.all([
        axios.get("http://127.0.0.1:8000/courses_completed"),
        axios.get("http://127.0.0.1:8000/course_list"),
        axios.get("http://127.0.0.1:8000/courses_not_completed"),
      ]);
      setSelectedCourses(compRes.data);
      setFullCourseList(listRes.data);
      setNotCompleted(notCompRes.data);
    };
    fetchCourseContext();
  }, []);

  useEffect(() => {
    const fetchCourseContext = async () => {
      setCourseData({
        completed: selectedCourses,
        courseList: fullCourseList,
        notComp: notCompleted,
      });
    };
    fetchCourseContext();
  }, [selectedCourses, fullCourseList, notCompleted]);

  console.log("courseData: ", courseData);

  



  // useEffect(() => {
  //   if (state?.selectedCourses) setSelectedCourses(state.selectedCourses);
  //   if (state?.fullCourseList) setFullCourseList(state.fullCourseList);
  //   if (state?.notCompleted) setNotCompleted(state.notCompleted);

  //   console.log("✅ Loaded from route state:");
  //   console.log("✅ selectedCourses:", state.selectedCourses);
  //   console.log("✅ fullCourseList:", state.fullCourseList);
  // }, [state]);

  let yearInstructions = "There are no extra instructions.";
  if (state.year === "First Year") {
    yearInstructions = "Focus on suggesting introductory-level courses and electives with few prerequisites.";
  } else if (state.year === "Second Year") {
    yearInstructions = "Suggest a mix of core required courses and electives assuming first-year prerequisites are completed.";
  } else if (state.year === "Third Year") {
    yearInstructions = "Suggest upper-level electives and core courses, and help them explore specialization paths.";
  } else if (state.year === "Fourth Year") {
    yearInstructions = "Focus on capstone projects, final graduation requirements, and any outstanding electives.";
  }

  const systemPrompt = `
  You are a kind and helpful UVic course planning assistant expert.

  🎓 This assistant is strictly for current or prospective **UVic students**.
  Only suggest **official UVic courses** that are part of UVic’s curriculum.

  Here is the student's information:
  - Name: ${state.name}
  - Major: ${state.major || "an unspecified major"}
  - Minor: ${state.minor || "None"}
  - Specialization: ${state.specialization || "None"}
  - Academic Interests: ${state.interests || "general academic fields"}
  - Degree Type: ${state.degree_type}
  - Year Level: ${state.year || "unspecified"}
  - ${yearInstructions}
  - Completed Co-op: ${state.coop_completed || 0}, Planned Co-op: ${state.coop_planned || 0}
  - Completed Courses: ${courseData.completed || "None"}
  - Courses which are not completed by ${state.name} and offered in the current term: ${courseData.notComp?.join(", ") || "None"}
  - Program Course List: ${courseData.courseList || "Not provided"}

  📚 The student plans to take:
  - ${state.core_courses} core course(s)
  - ${state.elective_courses} elective course(s)

  👉 Your task:
  - Recommend a total of ${state.core_courses + state.elective_courses} **UVic courses**
  - Choose core courses from the student’s major and program course list
  - Choose electives from outside the core list that align with their interests or provide breadth
  - Avoid recommending already completed courses
  - Make sure prerequisites are met
  - Adjust difficulty based on year level (e.g., don’t suggest 400-level courses to first-years)

  ✍️ Response Format for returning the courses:
  1. [Course Code] - [Course Title] (Core or Elective)

  Example:
  1. CSC 225 - Algorithms and Data Structures I (Core)
  2. CSC 226 - Algorithms and Data Structures II (Core)
  3. PHIL 161 - Introduction to Logic (Elective)

  💡 Use a friendly and clear tone. Keep the recommendations concise.
  Do **not** suggest non-UVic courses. Do **not** make up course codes.
  If you're unsure, politely ask the student for clarification before continuing.
  `;

  // console.log("Debug Info:");
  // console.log("state.core_courses:", state?.core_courses);
  // console.log("state.selectedCourses:", state.selectedCourses);
  // console.log("state.fullCourseList:", state.fullCourseList);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');

    const messagesForCohere = [
      { role: 'system', content: systemPrompt },
      ...updatedMessages.map(m => ({
        role: m.role,
        content: m.content
      }))
    ];

    try {
      const res = await fetch('http://localhost:8000/google/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messagesForCohere }),
      });

      const data = await res.json();
      const contentArr = data?.content;

      let replyText = '';
      if (Array.isArray(contentArr) && contentArr.length > 0) {
        replyText = contentArr[0].text?.trim() || '';
      } else {
        console.error('⚠️ Unexpected format for contentArr:', contentArr);
        replyText = "Sorry, I didn't understand that.";
      }

      setMessages([
        ...updatedMessages,
        { role: 'assistant', content: replyText }
      ]);
    } catch (e) {
      console.error('Cohere backend error:', e);
      alert('❌ Error talking to backend: ' + e.message);
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          role: 'assistant',
          content: `Hi ${state.name}, I’ll help you with your UVic course planning. Ask me anything about course selection!`
        }
      ]);
    }
  }, []);

  return (
    <div className="flex min-h-screen w-screen bg-gradient-to-b from-blue-600 to-blue-900 text-white justify-center items-center px-4 py-6">
      <div className="bg-white bg-opacity-10 backdrop-blur-md rounded-2xl p-6 w-full max-w-3xl shadow-lg flex flex-col h-full max-h-[90vh]">
        <h2 className="text-3xl font-bold mb-4 text-center">UVic Course Planning Assistant 💬</h2>

        <div className="flex-1 overflow-y-auto space-y-4 p-2">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] p-3 rounded-lg text-sm break-words whitespace-pre-wrap ${
                msg.role === 'user'
                  ? 'bg-white bg-opacity-20 text-white rounded-br-none'
                  : 'bg-white bg-opacity-10 text-white rounded-bl-none'
              }`}>
                {msg.content}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        <div className="flex gap-2 mt-4">
          <input
            className="flex-1 p-2 rounded bg-white bg-opacity-80 text-black"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask something..."
          />
          <button
            className="px-6 py-2 bg-yellow-400 text-blue-950 font-semibold rounded-full hover:bg-yellow-300 transition"
            onClick={sendMessage}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
