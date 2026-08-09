import { useState } from 'react';
import './index.css';

// Simple mock candidates for the Start Screen based on candidates.json structure
const MOCK_CANDIDATES = [
  {
    id: "CAND-001",
    name: "Sarah Johnson",
    jobRole: "Senior Data Engineer",
    missions: [
      { day: 7, title: "Embeddings Explained", passed: true, attempts: 1 },
      { day: 10, title: "Retrieval", passed: true, attempts: 2 },
      { day: 12, title: "Prompt Engineering", passed: true, attempts: 4 },
      { day: 22, title: "Multi-Agent Orchestration", passed: true, attempts: 1 },
      { day: 23, title: "MCP", passed: true, attempts: 1 }
    ],
    signals: {}
  }
];

const API_BASE = "http://localhost:8000/api";

function App() {
  const [screen, setScreen] = useState<'LANDING' | 'START' | 'CHAT' | 'FEEDBACK'>('LANDING');
  
  // State
  const [sessionId] = useState(() => "session-" + Math.random().toString(36).substr(2, 9));
  const [candidate] = useState(MOCK_CANDIDATES[0]);
  const [chatHistory, setChatHistory] = useState<{role: 'interviewer' | 'candidate', text: string}[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);

  const startInterview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/interview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: sessionId,
          candidate: candidate
        })
      });
      const data = await res.json();
      setChatHistory([{ role: 'interviewer', text: data.reply }]);
      setScreen('CHAT');
    } catch (err) {
      console.error(err);
      alert("Failed to connect to backend. Is FastAPI running?");
    }
    setIsLoading(false);
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    
    const userMessage = inputValue;
    setInputValue("");
    setChatHistory(prev => [...prev, { role: 'candidate', text: userMessage }]);
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE}/interview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: sessionId,
          message: userMessage
        })
      });
      const data = await res.json();
      
      setChatHistory(prev => [...prev, { role: 'interviewer', text: data.reply }]);
      
      if (data.done && data.feedback) {
        setFeedback(data.feedback);
        setScreen('FEEDBACK');
      }
    } catch (err) {
      console.error(err);
      alert("Error sending message");
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4 md:p-8 font-sans text-gray-800">
      
      {/* LANDING SCREEN */}
      {screen === 'LANDING' && (
        <div className="max-w-4xl w-full flex flex-col items-center text-center space-y-10 animate-fade-in py-10">
          <div className="space-y-4">
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              Adaptive AI Interviewer
            </h1>
            <p className="text-lg md:text-2xl text-gray-600 font-light max-w-2xl mx-auto">
              A dynamic, intelligent evaluation engine built for the <span className="font-semibold text-purple-600">ABTalks 60 Day Challenge</span>.
            </p>
          </div>

          <div className="bg-white p-8 md:p-10 rounded-3xl shadow-xl shadow-blue-900/5 max-w-3xl w-full text-left space-y-6 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-800 border-b pb-2">Project Purpose</h2>
            <p className="text-gray-600 leading-relaxed text-lg">
              Most interview bots just read from a static list of questions. The <strong>Adaptive AI Interviewer</strong> does something completely different. 
            </p>
            <p className="text-gray-600 leading-relaxed text-lg">
              Designed as the capstone evaluation tool for the <strong>ABTalks 60 Day Challenge</strong>, it reads a learner's actual progress, builds a customized interview plan, and dynamically adjusts its follow-up questions based on how well they answer—exactly like a real human interviewer.
            </p>
            <div className="bg-indigo-50 p-6 rounded-2xl border border-indigo-100">
              <h3 className="font-semibold text-indigo-900 mb-2">Key Features</h3>
              <ul className="list-disc pl-5 text-indigo-800 space-y-1">
                <li>Grounds questions in the 60-day AI engineering curriculum</li>
                <li>Adapts difficulty (goes deeper or simplifies) based on your answers</li>
                <li>Generates evidence-based feedback highlighting strengths and gaps</li>
              </ul>
            </div>
          </div>

          <button 
            onClick={() => setScreen('START')}
            className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full font-bold text-lg md:text-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 overflow-hidden"
          >
            <span className="relative z-10">Experience the Interview</span>
            <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 transition-opacity"></div>
          </button>
        </div>
      )}

      {/* WRAPPER FOR APP SCREENS */}
      {screen !== 'LANDING' && (
        <div className="w-full max-w-3xl bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col border border-gray-100 transition-all" style={{ minHeight: '650px', maxHeight: '90vh' }}>
          
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-5 text-center font-bold text-xl md:text-2xl shadow-sm flex items-center justify-between">
            <span>Adaptive AI Interviewer</span>
            <button onClick={() => setScreen('LANDING')} className="text-sm font-normal text-blue-100 hover:text-white underline">Back to Home</button>
          </div>

          {/* START SCREEN */}
          {screen === 'START' && (
            <div className="flex-1 flex flex-col items-center justify-center p-6 md:p-10 space-y-8 animate-fade-in">
              <h2 className="text-2xl md:text-3xl font-bold text-gray-800 text-center">Ready for your Evaluation?</h2>
              
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-8 rounded-2xl w-full max-w-md text-left border border-gray-200 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-blue-100 rounded-full blur-2xl -mr-10 -mt-10 opacity-60"></div>
                
                <h3 className="text-sm uppercase tracking-wider font-semibold text-gray-500 mb-4">Candidate Profile</h3>
                <p className="font-bold text-2xl text-blue-900 mb-1">{candidate.name}</p>
                <p className="text-blue-600 font-medium">{candidate.jobRole}</p>
                
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <p className="text-sm text-gray-600 flex items-center">
                    <span className="w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                    Completed {candidate.missions.length} core curriculum days
                  </p>
                </div>
              </div>

              <button 
                onClick={startInterview}
                disabled={isLoading}
                className="w-full max-w-md px-8 py-4 bg-blue-600 text-white rounded-xl font-bold text-lg shadow-md hover:bg-blue-700 hover:shadow-lg transition-all disabled:opacity-50 flex justify-center items-center"
              >
                {isLoading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Initializing Engine...
                  </span>
                ) : 'Begin Interview Session'}
              </button>
            </div>
          )}

          {/* CHAT SCREEN */}
          {screen === 'CHAT' && (
            <div className="flex-1 flex flex-col h-full animate-fade-in">
              <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 max-h-[60vh] bg-gray-50/50">
                {chatHistory.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'candidate' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] md:max-w-[75%] shadow-sm p-4 md:p-5 text-[15px] md:text-base leading-relaxed ${
                      msg.role === 'candidate' 
                        ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-2xl rounded-tr-sm' 
                        : 'bg-white text-gray-800 rounded-2xl rounded-tl-sm border border-gray-100'
                    }`}>
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white border border-gray-100 text-gray-400 rounded-2xl rounded-tl-sm p-4 flex items-center space-x-2 shadow-sm">
                      <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                )}
              </div>
              <div className="p-4 md:p-5 bg-white border-t border-gray-100 flex flex-col md:flex-row space-y-3 md:space-y-0 md:space-x-3">
                <input 
                  type="text"
                  value={inputValue}
                  onChange={e => setInputValue(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && sendMessage()}
                  placeholder="Type your detailed response..."
                  className="flex-1 border border-gray-200 bg-gray-50 rounded-xl px-5 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-gray-800"
                  disabled={isLoading}
                />
                <button 
                  onClick={sendMessage}
                  disabled={isLoading || !inputValue.trim()}
                  className="bg-blue-600 text-white px-8 py-4 rounded-xl font-bold hover:bg-blue-700 disabled:opacity-50 transition-all shadow-sm hover:shadow active:scale-95 whitespace-nowrap"
                >
                  Send Answer
                </button>
              </div>
            </div>
          )}

          {/* FEEDBACK SCREEN */}
          {screen === 'FEEDBACK' && feedback && (
            <div className="flex-1 overflow-y-auto p-6 md:p-10 space-y-8 animate-fade-in">
              <div className="text-center pb-4 border-b border-gray-100">
                <h2 className="text-3xl font-extrabold text-gray-800">Evaluation Complete</h2>
                <p className="text-gray-500 mt-2 text-lg">Here is your evidence-based performance review</p>
              </div>
              
              <div className="bg-blue-50/50 p-6 md:p-8 rounded-2xl border border-blue-100 shadow-sm">
                <h3 className="font-bold text-blue-900 mb-3 text-lg flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  Overall Summary
                </h3>
                <p className="text-gray-700 leading-relaxed">{feedback.summary}</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-emerald-50/50 p-6 rounded-2xl border border-emerald-100 shadow-sm">
                  <h3 className="font-bold text-emerald-800 mb-4 text-lg flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Demonstrated Strengths
                  </h3>
                  <ul className="space-y-3">
                    {feedback.strengths.map((s: string, i: number) => (
                      <li key={i} className="flex items-start">
                        <span className="text-emerald-500 mr-2 mt-1">•</span>
                        <span className="text-emerald-900">{s}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="bg-rose-50/50 p-6 rounded-2xl border border-rose-100 shadow-sm">
                  <h3 className="font-bold text-rose-800 mb-4 text-lg flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    Knowledge Gaps
                  </h3>
                  <ul className="space-y-3">
                    {feedback.gaps.map((g: string, i: number) => (
                      <li key={i} className="flex items-start">
                        <span className="text-rose-500 mr-2 mt-1">•</span>
                        <span className="text-rose-900">{g}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="bg-amber-50/50 p-6 md:p-8 rounded-2xl border border-amber-100 shadow-sm">
                <h3 className="font-bold text-amber-800 mb-4 text-lg flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  Actionable Next Steps
                </h3>
                <ul className="space-y-3">
                  {feedback.next.map((n: string, i: number) => (
                    <li key={i} className="flex items-start">
                      <span className="w-6 h-6 rounded-full bg-amber-200 text-amber-800 flex items-center justify-center text-xs font-bold mr-3 mt-0.5 flex-shrink-0">{i+1}</span>
                      <span className="text-amber-900 font-medium pt-0.5">{n}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="pt-6 flex justify-center">
                 <button 
                  onClick={() => window.location.reload()}
                  className="px-8 py-3 bg-gray-900 text-white rounded-full font-semibold hover:bg-gray-800 transition"
                 >
                   Start New Interview
                 </button>
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default App;
