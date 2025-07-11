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
  const [preReq, setPreReq] = useState([]);
  const [courseData, setCourseData] = useState({
    completed: "",      // ← array, so .join() is safe
    courseList: "",
    notComp: [],
    preReqs: []
  });

  useEffect(() => {
    const fetchCourseContext = async () => {
      const [compRes, listRes, notCompRes, preReqRes] = await Promise.all([
        axios.get("http://127.0.0.1:8000/courses_completed"),
        axios.get("http://127.0.0.1:8000/course_list"),
        axios.get("http://127.0.0.1:8000/courses_not_completed"),
        axios.get("http://127.0.0.1:8000/pre_req_check"),
      ]);
      setSelectedCourses(compRes.data);
      setFullCourseList(listRes.data);
      setNotCompleted(notCompRes.data);
      setPreReq(preReqRes.data);
    };
    fetchCourseContext();
  }, []);

  useEffect(() => {
    const fetchCourseContext = async () => {
      setCourseData({
        completed: selectedCourses,
        courseList: fullCourseList,
        notComp: notCompleted,
        preReqs: preReq
      });
    };
    fetchCourseContext();
  }, [selectedCourses, fullCourseList, notCompleted]);

  // console.log("courseData: ", courseData);

  



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
  You are a friendly and knowledgeable UVic course planning advisor. Think of yourself as a helpful academic advisor who's having a natural conversation with a student.
**Your Role**: You're here to help UVic students with course planning, but you're flexible and conversational. You don't need to always give the same structured response.

**Student Context**:
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
  - Currently ${state.name} has met the prerequisites for the following courses: ${courseData.preReqs?.join(", ") || "None"}
  - Program Course List: ${courseData.courseList || "Not provided"}

  The student plans to take:
  - ${state.core_courses} core course(s)
  - ${state.elective_courses} elective course(s)

    **Your Approach**:
  - Be conversational and natural - like talking to a friend
  - Don't always give the same format or same courses
  - Vary your responses based on what the student asks
  - Sometimes give detailed explanations, sometimes brief suggestions
  - Ask follow-up questions when appropriate
  - Share insights about course difficulty, workload, or interesting aspects
  - Mention alternatives or different approaches when relevant
  - the user is only alolowed to do the courses they have met the prerequisites for, only suggest those courses.
  - when suggesting do it in the following format: course name (course code) 
    eg: "CSC 370 (Database Systems)"

  **Response Style**:
  - Use a warm, friendly tone
  - Be encouraging and supportive
  - Share personal insights about courses when relevant
  - Ask clarifying questions if needed
  - Don't be rigid with formatting - adapt to the conversation flow

  Remember: You're having a conversation, not filling out a form. Be helpful, engaging, and varied in your responses.
  `;


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
      const res = await fetch('http://localhost:8000/cohere/chat', {
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
