import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { client } from '../utils/cohereClient';

export default function Chatbot() {
  const { state } = useLocation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  const systemPrompt = `You are a kind and helpful UVic course planning assistant expert.
Major: ${state.major}
Minor: ${state.minor || "None"}
Specialization: ${state.specialization || "None"}
Interests: ${state.interests || "general academic fields"}
Completed courses: ${state.selectedCourses?.join(", ") || "None"}
Year: ${state.year}
Elective courses: ${state.elective_courses}, Core courses: ${state.core_courses}
Completed ${state.coop_completed || 0} co-op term(s), planning ${state.coop_planned || 0}.`;

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
      const res = await client.chat({
        model: 'command-r',
        messages: messagesForCohere,
        temperature: 0.3,
      });

      // 1️⃣ Grab the array off the `message` object
      const contentArr = res.message?.content;

      // 2️⃣ Inspect the raw array
      console.log('🔥 Cohere contentArr:', contentArr);

      // 3️⃣ Safely pull out the first .text
      let replyText = '';
      if (Array.isArray(contentArr) && contentArr.length > 0) {
        replyText = contentArr[0].text?.trim() || '';
        console.log('🗨️  First reply:', replyText);
      } else {
        console.error('⚠️  Unexpected format for contentArr:', contentArr);
      }

      // 4️⃣ Update state with that reply
      setMessages([
        ...updatedMessages,
        { role: 'assistant', content: replyText }
      ]);
    } catch (e) {
      console.error('Cohere error:', e);
      alert('❌ Error talking to Cohere: ' + e.message);
    }
  };


  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        { role: 'CHATBOT', content: '👋 Hi! I’m your UVic course planning assistant. Ask me anything about course selection!' }
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
