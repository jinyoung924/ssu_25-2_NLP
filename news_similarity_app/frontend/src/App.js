import { useState } from "react";
import axios from "axios";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  const analyze = async () => {
    const res = await axios.post("/analyze", { url });
    setResult(res.data);
    const lb = await axios.get("/leaderboard");
    setLeaderboard(lb.data);
  };

  return (
    <div style={{ display: "flex", padding: 20 }}>
      <div style={{ flex: 3 }}>
        <h1>뉴스 기사 분석</h1>
        <input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="뉴스 URL 입력" style={{ width: "60%" }} />
        <button onClick={analyze}>분석</button>
        {result && (
          <div>
            <h2>제목: {result.title}</h2>
            <p><b>유사도:</b> {result.similarity_score}</p>
            <p><b>요약:</b> {result.summary}</p>
          </div>
        )}
      </div>
      <div style={{ flex: 1, marginLeft: 20 }}>
        <h2>언론사 리더보드</h2>
        <ul>
          {leaderboard.map((item, idx) => (
            <li key={idx}>{item.publisher} - {item.avg_score}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
