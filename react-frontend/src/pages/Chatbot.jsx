import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

const Chatbot = () => {
  const { state } = useLocation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  const systemPrompt = `You are a kind and helpful UVic course planning assistant expert. If you need additional information, you can ask them before providing the most accurate possible recommendation/help.
Major: ${state.major}
Minor: ${state.minor || "None"}
Specialization: ${state.specialization || "None"}
Interests: ${state.interests || "general academic fields"}
Completed courses: ${state.selectedCourses?.join(", ") || "None"}
Year: ${state.year}
Elective courses: ${state.elective_courses}, Core courses: ${state.core_courses}
Completed ${state.coop_completed || 0} co-op terms, planning ${state.coop_planned || 0}
`;

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "USER", content: input }];
    setMessages(newMessages);
    setInput("");

    const chat_history = [
      { role: "SYSTEM", message: systemPrompt },
      ...newMessages.map(m => ({
        role: m.role === "USER" ? "USER" : "CHATBOT",
        message: m.content,
      }))
    ];

    try {
      const res = await fetch("https://api.cohere.ai/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${import.meta.env.VITE_COHERE_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "command-r",
          message: input,
          chat_history
        })
      });

      const data = await res.json();
      const reply = data.text || "Sorry, I didn't get that.";
      setMessages([...newMessages, { role: "CHATBOT", content: reply }]);
    } catch (e) {
      alert("Error talking to AI: " + e.message);
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ role: "CHATBOT", content: "👋 Hi! I'm your UVic course planning assistant. Ask me anything about course selection!" }]);
    }
  }, []);

  return (
    <div className="flex flex-col max-w-3xl mx-auto p-4 h-screen">
      <div className="flex-1 overflow-y-auto space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`p-3 rounded-md ${msg.role === "USER" ? 'bg-blue-100 self-end' : 'bg-gray-100 self-start'}`}>
            <p>{msg.content}</p>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2 mt-4">
        <input
          className="flex-1 border p-2 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask something..."
        />
        <button
          className="px-4 py-2 bg-green-600 text-white rounded"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
