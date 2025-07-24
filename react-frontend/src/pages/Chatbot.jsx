import { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import jsPDF from 'jspdf';
import useScrollToTop from '../hooks/useScrollToTop';
import SidebarLayout from '../components/SidebarLayout';

export default function Chatbot() {
  useScrollToTop();

  const { state } = useLocation();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const [courseData, setCourseData] = useState({ completed: '', courseList: '' });
  const [intialMessage, setIntialMessage] = useState('');

  useEffect(() => {
    const fetchCourseContext = async () => {
      const [compRes, listRes] = await Promise.all([
        axios.get('http://127.0.0.1:8000/courses_completed'),
        axios.get('http://127.0.0.1:8000/course_list'),
      ]);
      setCourseData({
        completed: compRes.data,
        courseList: listRes.data,
      });
    };
    fetchCourseContext();
  }, []);

    useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    const fetchIntialMessage = async () => {
      const courseList = await axios.get('http://localhost:8000/course_list');
      console.log("courseList", courseList.data);
      const courseListString = courseList.data.data.join(', ')
   
      console.log("courseListString", courseListString);

      const coursesCompleted = await axios.get('http://localhost:8000/courses_completed');
      console.log("coursesCompleted", coursesCompleted.data);
      const coursesCompletedString = coursesCompleted.data.data;

      const preReqCheck = await axios.get('http://localhost:8000/pre_req_check');
      const preReqCheckString = preReqCheck.data.data.join(', ');

      const systemPrompt = `
      The user wants to do 4 courses this term, based on the course list, courses already completed,courses left to complete which are offered in the term and the courses for which the user has completed the pre-reqs for. 
      SUGGEST 4 COURSES THAT THE USER SHOULD TAKE ONLY BASED ON THE COURSES FOR WHICH THE USER HAS COMPLETED THE PREREQS FOR.
      Full Course list: ${courseListString}
      Courses already completed by the user in the past: ${coursesCompletedString}
      COURSES FOR WHICH THE USER HAS COMPLETED THE PREREQS AND IS ALLOWED TO TAKE: ${preReqCheckString}
      `;
      const messagesForCohere = [{ role: 'system', content: systemPrompt }];
      const res = await fetch('http://localhost:8000/cohere/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messagesForCohere }),
      });

      const data = await res.json();
      setIntialMessage(data.content[0].text.trim());
    }
    fetchIntialMessage();
  }, []);

  useEffect(() => {
    if (intialMessage && messages.length === 0) {
      setMessages([
        {
          role: 'assistant',
          content: intialMessage,
        },
      ]);
    }
  }, [intialMessage]);

  console.log(intialMessage);

  const yearInstructions = {
    'First Year': 'Focus on suggesting introductory-level courses and electives with few prerequisites.',
    'Second Year': 'Suggest a mix of core required courses and electives assuming first-year prerequisites are completed.',
    'Third Year': 'Suggest upper-level electives and core courses, and help them explore specialization paths.',
    'Fourth Year': 'Focus on capstone projects, final graduation requirements, and any outstanding electives.',
  }[state.year] || 'There are no extra instructions.';

  const systemPrompt = `You are a kind and helpful UVic course planning assistant expert.`;

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);

    const messagesForCohere = [
      { role: 'system', content: systemPrompt },
      ...updatedMessages.map((m) => ({ role: m.role, content: m.content })),
    ];

    try {
      const res = await fetch('http://localhost:8000/cohere/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messagesForCohere }),
      });

      const data = await res.json();
      const replyText = data?.content?.[0]?.text?.trim() || "Sorry, I didn’t understand that.";

      setMessages([...updatedMessages, { role: 'assistant', content: replyText }]);
    } catch (e) {
      console.error('Cohere backend error:', e);
      alert('❌ Error talking to backend: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const exportPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(14);
    doc.text('UVic Course Plan Recommendations', 10, 10);
    let y = 20;
    messages.forEach((msg) => {
      if (msg.role === 'assistant') {
        const lines = doc.splitTextToSize(`Assistant: ${msg.content}`, 180);
        doc.text(lines, 10, y);
        y += lines.length * 10;
      }
    });
    doc.save('uvic_course_plan.pdf');
  };

  const savePlan = async () => {
    try {
      await axios.post('http://localhost:8000/save_plan', {
        user: state.name,
        messages,
      });
      alert('✅ Plan saved successfully!');
    } catch (e) {
      console.error(e);
      alert('❌ Failed to save plan.');
    }
  };

  const suggestions = [
    'Suggest requested core courses and elective courses',
    'What are the upcoming core courses to be done?',
    'Suggest easy electives.',
    'Give a sample 4-month schedule',
  ];

  return (
    <SidebarLayout>
      <main className="flex-grow flex justify-center items-start px-6 pt-14 pb-10">
        <section className="bg-white rounded-2xl p-10 w-full max-w-2xl shadow-soft mb-10 pt-10 flex flex-col h-[85vh]">
          <h2 className="text-3xl font-bold text-center mb-6">UVic Course Planning Assistant 💬</h2>

          <div className="flex-1 overflow-y-auto space-y-4 px-2">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[75%] p-3 rounded-lg text-sm whitespace-pre-wrap break-words ${
                  msg.role === 'user'
                    ? 'bg-accent text-white rounded-br-none'
                    : 'bg-purple/10 text-black rounded-bl-none'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="text-sm text-gray-500 italic">Assistant is typing...</div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="mt-4 flex gap-2">
            <input
              className="flex-1 p-2 rounded border bg-white text-black"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask something..."
            />
            <button
              className="px-6 py-2 bg-accent text-white font-semibold rounded-full hover:text-black hover:bg-cyan transition shadow-soft"
              onClick={sendMessage}
            >
              Send
            </button>
          </div>

          <div className="mt-4">
            <h3 className="text-sm font-semibold mb-2">Suggestions:</h3>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((text, i) => (
                <button
                  key={i}
                  onClick={() => setInput(text)}
                  className="px-3 py-1 text-xs rounded-full border border-purple text-purple hover:bg-purple/10 bg-white"
                >
                  {text}
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-between items-center flex-wrap gap-4 mt-6">
            <button
              className="px-6 py-3 bg-gray-200 text-black font-semibold rounded-full hover:bg-gray-300 transition"
              onClick={() => navigate(-1)}
            >
              Back
            </button>

            <div className="flex gap-4">
              <button
                onClick={exportPDF}
                className="px-4 py-2 bg-white text-purple text-sm rounded-full border border-purple hover:bg-purple/10"
              >
                📄 Export Chat
              </button>
              <button
                onClick={savePlan}
                className="px-4 py-2 bg-white text-purple text-sm rounded-full border border-purple hover:bg-purple/10"
              >
                💾 Save this Schdule
              </button>
            </div>
          </div>
        </section>
      </main>
    </SidebarLayout>
  );
}