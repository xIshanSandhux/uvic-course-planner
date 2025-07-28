import { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import jsPDF from 'jspdf';
import SidebarLayout from '../components/SidebarLayout';

export default function Chatbot() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [intialMessage, setIntialMessage] = useState('');
  const scrollContainerRef = useRef(null);

  useEffect(() => {
    const fetchIntialMessage = async () => {
      const courseList = await axios.get('http://localhost:8000/course_list');
      const courseListString = courseList.data.data.join(', ');
      const coursesCompleted = await axios.get('http://localhost:8000/courses_completed');
      const coursesCompletedString = coursesCompleted.data.data;
      const preReqCheck = await axios.get('http://localhost:8000/pre_req_check');
      const preReqCheckString = preReqCheck.data.data.join(', ');

      const systemPrompt = `
        The user wants to do 4 courses this term, based on the course list, courses already completed, 
        and courses they’re eligible for (based on prerequisites).
        Full list: ${courseListString}
        Completed: ${coursesCompletedString}
        Eligible: ${preReqCheckString}
      `;

      const messagesForCohere = [{ role: 'system', content: systemPrompt }];
      const res = await fetch('http://localhost:8000/cohere/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messagesForCohere }),
      });

      const data = await res.json();
      setIntialMessage(data.content[0].text.trim());
    };
    fetchIntialMessage();
  }, []);

  useEffect(() => {
    if (intialMessage && messages.length === 0) {
      setMessages([{ role: 'assistant', content: intialMessage }]);
    }
  }, [intialMessage]);

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);

    const systemPrompt = `You are a kind and helpful UVic course planning assistant expert.`;

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

  return (
    <SidebarLayout>
      <main className="h-screen w-full flex justify-center items-center bg-offwhite">
        <div className="w-full max-w-2xl h-[90vh] bg-white rounded-xl shadow-lg flex flex-col overflow-hidden">
          {/* Header */}
          <div className="py-4 border-b text-center text-lg font-semibold text-purple">
            UVic Course Planning Assistant 💬
          </div>

          {/* Chat Scroll Container */}
          <div
            ref={scrollContainerRef}
            className="flex-1 overflow-y-auto px-4 pt-6 space-y-4 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent"
          >
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`px-4 py-2 rounded-lg max-w-[80%] text-sm whitespace-pre-wrap ${
                    msg.role === 'user'
                      ? 'bg-accent text-white rounded-br-none'
                      : 'bg-gray-100 text-black shadow-sm rounded-bl-none'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="text-sm italic text-gray-400">Assistant is typing…</div>
            )}
          </div>

          {/* Chat Input */}
          <div className="border-t p-4 bg-white">
            <div className="flex items-center gap-2">
              <input
                className="flex-1 px-3 py-2 rounded-md border border-gray-300 bg-gray-50 text-black focus:outline-none"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Ask about your courses..."
              />
              <button
                onClick={sendMessage}
                className="px-5 py-2 bg-accent text-white rounded-md hover:bg-cyan transition"
              >
                Send
              </button>
            </div>

            <div className="flex justify-between items-center pt-2 text-sm">
              <button
                onClick={() => navigate(-1)}
                className="bg-black text-white px-4 py-1 rounded-md hover:opacity-80"
              >
                ← Back
              </button>
              <div className="flex gap-2">
                <button
                  onClick={exportPDF}
                  className="bg-black text-white px-4 py-1 rounded-md hover:opacity-80"
                >
                  📄 Export
                </button>
                <button
                  onClick={savePlan}
                  className="bg-black text-white px-4 py-1 rounded-md hover:opacity-80"
                >
                  💾 Save
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </SidebarLayout>
  );
}
