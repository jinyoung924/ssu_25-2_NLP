import React, { useState, useEffect } from "react";
import axios from "axios";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    // ✅ 리더보드 더미 데이터 복구
    setLeaderboard([
      { publisher: "조선일보", avg_score: 0.913 },
      { publisher: "한겨레", avg_score: 0.878 },
      { publisher: "연합뉴스", avg_score: 0.842 },
      { publisher: "중앙일보", avg_score: 0.825 },
      { publisher: "KBS", avg_score: 0.812 },
      { publisher: "MBC", avg_score: 0.798 },
      { publisher: "SBS", avg_score: 0.787 },
      { publisher: "서울신문", avg_score: 0.774 },
      { publisher: "YTN", avg_score: 0.761 },
      { publisher: "한국일보", avg_score: 0.745 },
      { publisher: "동아일보", avg_score: 0.733 },
      { publisher: "경향신문", avg_score: 0.721 },
      { publisher: "매일경제", avg_score: 0.709 },
      { publisher: "전자신문", avg_score: 0.698 },
      { publisher: "파이낸셜뉴스", avg_score: 0.689 },
      { publisher: "뉴스1", avg_score: 0.673 },
      { publisher: "노컷뉴스", avg_score: 0.662 },
      { publisher: "프레시안", avg_score: 0.651 },
      { publisher: "ZDNet Korea", avg_score: 0.645 },
      { publisher: "아이뉴스24", avg_score: 0.638 },
    ]);
  }, []);

  const analyze = async () => {
    if (!url.trim()) return alert("뉴스 URL을 입력해주세요!");
    try {
      const response = await axios.post("http://localhost:8000/analyze", { url });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      alert("분석 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col items-center py-10 px-4 md:px-10">
      <h1 className="text-3xl font-bold text-blue-700 mb-8 flex items-center gap-2">
        🧠 언론탐정단
      </h1>

      {/* 통계 위젯 */}
      <div className="w-full max-w-6xl grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        {[
          { label: "총 분석 수", value: 126 },
          { label: "평균 유사도", value: 0.784 },
          { label: "최고 유사도", value: 0.982 },
        ].map((item, idx) => (
          <div
            key={idx}
            className="bg-white border-2 border-gray-300 rounded-lg shadow-sm p-4 text-center"
          >
            <p className="text-gray-500 text-sm">{item.label}</p>
            <p className="text-2xl font-bold text-blue-600">{item.value}</p>
          </div>
        ))}
      </div>

      <div className="flex flex-col md:flex-row gap-8 w-full max-w-7xl">
        {/* 입력 및 결과 */}
        <div className="flex-1">
          <div className="bg-white border-2 border-gray-300 rounded-2xl shadow-md p-6 mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">뉴스 기사 분석</h2>
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="뉴스 URL을 입력하세요"
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
              />
              <button
                onClick={analyze}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition"
              >
                분석
              </button>
            </div>
          </div>

          {/* 안내 카드 */}
          {!result && (
            <div className="bg-white border-2 border-gray-300 shadow rounded-xl p-6 mb-6">
              <h2 className="text-lg font-semibold text-gray-700 mb-2">👋 사용 안내</h2>
              <p className="text-gray-600 leading-relaxed">
                뉴스 기사 URL을 입력한 뒤{" "}
                <span className="font-semibold text-blue-600">[분석]</span> 버튼을 누르면<br />
                기사 제목과 본문 간의 유사도를 분석하고 요약을 제공합니다.
              </p>
            </div>
          )}

          {/* 분석 결과 */}
          {result && (
            <div className="bg-white border-2 border-gray-300 rounded-2xl shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">📄 분석 결과</h3>
              <div className="flex flex-col md:flex-row items-center gap-6">
                <div className="w-40 h-40">
                  <Doughnut
                    data={{
                      labels: ["유사도", "차이"],
                      datasets: [
                        {
                          data: [result.similarity_score, 1 - result.similarity_score],
                          backgroundColor: ["#3B82F6", "#E5E7EB"],
                          borderWidth: 1,
                        },
                      ],
                    }}
                    options={{
                      plugins: { legend: { display: false } },
                      cutout: "70%",
                    }}
                  />
                </div>
                <div className="flex-1">
                  <p className="text-gray-700 mb-2">
                    <b>제목:</b> {result.title}
                  </p>
                  <p className="text-gray-700 mb-2">
                    <b>유사도 점수:</b>{" "}
                    <span className="text-blue-600 font-bold">
                      {result.similarity_score.toFixed(4)}
                    </span>
                  </p>
                  <p className="text-gray-700 mb-2">
                    <b>판정:</b>{" "}
                    <span className="font-semibold">
                      {result.label}
                    </span>
                  </p>
                  <p className="text-gray-700 leading-relaxed">
                    <b>요약:</b> {result.summary}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* 리더보드 */}
        <div className="w-full md:w-1/3">
          <div className="bg-white border-2 border-gray-300 rounded-2xl shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">🏆 언론사 리더보드</h2>
            <ul className="divide-y divide-gray-200 max-h-96 overflow-y-scroll pr-4">
              {leaderboard.map((item, idx) => {
                const rankIcon =
                  idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : `${idx + 1}.`;
                const scoreColor =
                  item.avg_score >= 0.85
                    ? "text-blue-600"
                    : item.avg_score >= 0.75
                    ? "text-gray-600"
                    : "text-gray-400";
                return (
                  <li
                    key={idx}
                    className="py-3 flex justify-between items-center text-gray-700"
                  >
                    <span className="font-medium flex items-center gap-2">
                      {rankIcon} {item.publisher}
                    </span>
                    <span className={`${scoreColor} font-semibold`}>
                      {item.avg_score.toFixed(3)}
                    </span>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
