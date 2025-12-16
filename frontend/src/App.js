import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setReply("");

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    setReply(data.reply);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center text-white">
      <div className="w-full max-w-xl bg-slate-900/80 backdrop-blur rounded-2xl shadow-2xl p-6">
        <h1 className="text-3xl font-bold text-center mb-2">🌦️ WeatherMind</h1>
        <p className="text-center text-gray-400 mb-6">
          AI-powered weather assistant
        </p>

        <div className="flex gap-2">
          <input
            className="flex-1 rounded-xl px-4 py-3 bg-slate-800 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask about weather (Hindi / English / Hinglish)"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-3 rounded-xl font-semibold"
          >
            Ask
          </button>
        </div>

        <div className="mt-6 min-h-[100px]">
          {loading && (
            <p className="text-blue-400 animate-pulse">
              🤖 Thinking & checking weather...
            </p>
          )}
          {reply && (
            <div className="bg-slate-800 rounded-xl p-4 mt-2">
              <p className="text-green-400 font-semibold mb-1">WeatherBot:</p>
              <p>{reply}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
