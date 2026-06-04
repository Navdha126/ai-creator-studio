import { useState } from "react";
import { Toaster, toast } from "react-hot-toast";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function TrendsTab() {
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeSection, setActiveSection] = useState("hooks");

  const loadTrends = async () => {
    try {
      const res = await axios.get(`${API}/trends`);
      setTrends(res.data);
    } catch {
      toast.error("Failed to load trends");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await axios.post(`${API}/refresh-trends`);
      await loadTrends();
      toast.success("Trends refreshed with latest articles!");
    } catch {
      toast.error("Failed to refresh trends");
    } finally {
      setRefreshing(false);
    }
  };

  useState(() => { loadTrends(); }, []);

  if (loading) return <div className="card"><p style={{color:"#888"}}>Loading trends...</p></div>;
  if (!trends) return null;

  return (
    <div>
      <div className="card">
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:"16px"}}>
          <div>
            <h2>🔥 Trending Now</h2>
            <p className="subtitle">
              {trends.last_updated
                ? `Last updated: ${new Date(trends.last_updated).toLocaleString()}`
                : "Built-in hooks — refresh to fetch latest"}
            </p>
          </div>
          <button className="btn-refresh" onClick={handleRefresh} disabled={refreshing}>
            {refreshing ? "Refreshing..." : "↻ Refresh"}
          </button>
        </div>

        <div className="section-tabs">
          <button className={activeSection === "hooks" ? "active" : ""} onClick={() => setActiveSection("hooks")}>
            🪝 Hooks ({trends.hooks.length})
          </button>
          <button className={activeSection === "formats" ? "active" : ""} onClick={() => setActiveSection("formats")}>
            🎬 Formats ({trends.formats.length})
          </button>
          <button className={activeSection === "articles" ? "active" : ""} onClick={() => setActiveSection("articles")}>
            📰 Articles ({trends.articles.length})
          </button>
        </div>
      </div>

      {activeSection === "hooks" && (
        <div>
          {trends.hooks.map((hook, i) => (
            <div key={i} className="trend-card">
              <div className="trend-category">{hook.category}</div>
              <div className="trend-hook">"{hook.hook}"</div>
              <div className="trend-why">💡 {hook.why_it_works}</div>
              <div className="trend-example">📝 Example: {hook.example}</div>
            </div>
          ))}
        </div>
      )}

      {activeSection === "formats" && (
        <div>
          {trends.formats.map((format, i) => (
            <div key={i} className="trend-card">
              <div className="trend-category">{format.best_for}</div>
              <h3 style={{color:"#fff", marginBottom:"8px"}}>{format.format}</h3>
              <p style={{color:"#aaa", fontSize:"0.9rem", marginBottom:"12px"}}>{format.description}</p>
              <div className="format-detail"><span>🎥 Film:</span> {format.film}</div>
              <div className="format-detail"><span>✍️ Text:</span> {format.text}</div>
              <div className="format-detail"><span>🎵 Sound:</span> {format.sound}</div>
            </div>
          ))}
        </div>
      )}

      {activeSection === "articles" && (
        <div>
          {trends.articles.length === 0
            ? <div className="card"><p style={{color:"#888"}}>No articles yet. Click Refresh to fetch latest marketing articles.</p></div>
            : trends.articles.map((article, i) => (
              <div key={i} className="trend-card">
                <div className="trend-category">{article.source}</div>
                <h3 style={{color:"#fff", marginBottom:"8px", fontSize:"1rem"}}>{article.title}</h3>
                <a href={article.link} target="_blank" rel="noreferrer" style={{color:"#a855f7", fontSize:"0.85rem"}}>
                  Read article →
                </a>
              </div>
            ))
          }
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState("profile");
  const [profile, setProfile] = useState({ user_id: "", niche: "", tone: "", audience: "" });
  const [contentReq, setContentReq] = useState({ user_id: "", content_type: "reel" });
  const [colorFiles, setColorFiles] = useState([]);
  const [colorNiche, setColorNiche] = useState("");
  const [colorVision, setColorVision] = useState("");
  const [ragQuestion, setRagQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSaveProfile = async () => {
    try {
      setLoading(true);
      await axios.post(`${API}/save-profile`, profile);
      toast.success("Profile saved!");
    } catch {
      toast.error("Failed to save profile");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateCaption = async () => {
    try {
      setLoading(true);
      const res = await axios.post(`${API}/generate-caption`, contentReq);
      setResult({ type: "caption", data: res.data.result });
    } catch {
      toast.error("Failed to generate content");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeColors = async () => {
    if (colorFiles.length === 0) return toast.error("Upload at least one image");
    try {
      setLoading(true);
      const formData = new FormData();
      colorFiles.forEach(f => formData.append("files", f));
      formData.append("niche", colorNiche || "general");
      if (colorVision) formData.append("vision", colorVision);
      const res = await axios.post(`${API}/analyze-colors`, formData);
      setResult({ type: "colors", data: res.data });
    } catch {
      toast.error("Failed to analyze colors");
    } finally {
      setLoading(false);
    }
  };

  const handleRagQuestion = async () => {
    if (!ragQuestion) return toast.error("Enter a question");
    try {
      setLoading(true);
      const res = await axios.post(`${API}/ask-knowledge-base`, { question: ragQuestion });
      setResult({ type: "rag", data: res.data.answer });
    } catch {
      toast.error("Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <Toaster />
      <header>
        <h1>✦ AI Creator Studio</h1>
        <p>Your AI-powered Instagram brand strategist</p>
      </header>

      <nav>
        {["profile", "content", "colors", "strategy", "trends"].map(t => (
          <button key={t} className={tab === t ? "active" : ""} onClick={() => setTab(t)}>
            {t === "profile" && "👤 Profile"}
            {t === "content" && "✍️ Content"}
            {t === "colors" && "🎨 Colors"}
            {t === "strategy" && "📚 Strategy"}
            {t === "trends" && "🔥 Trends"}
          </button>
        ))}
      </nav>

      <main>
        {tab === "profile" && (
          <div className="card">
            <h2>Creator Profile</h2>
            <p className="subtitle">Save your preferences for personalized content</p>
            <input placeholder="User ID (your name)" value={profile.user_id} onChange={e => setProfile({ ...profile, user_id: e.target.value })} />
            <input placeholder="Niche (e.g. tarot, fitness, fashion)" value={profile.niche} onChange={e => setProfile({ ...profile, niche: e.target.value })} />
            <input placeholder="Tone (e.g. mystical, energetic, professional)" value={profile.tone} onChange={e => setProfile({ ...profile, tone: e.target.value })} />
            <input placeholder="Target Audience (e.g. women 18-30)" value={profile.audience} onChange={e => setProfile({ ...profile, audience: e.target.value })} />
            <button className="btn-primary" onClick={handleSaveProfile} disabled={loading}>
              {loading ? "Saving..." : "Save Profile"}
            </button>
          </div>
        )}

        {tab === "content" && (
          <div className="card">
            <h2>Generate Content</h2>
            <p className="subtitle">AI-powered captions, hooks, and hashtags</p>
            <input placeholder="User ID" value={contentReq.user_id} onChange={e => setContentReq({ ...contentReq, user_id: e.target.value })} />
            <select value={contentReq.content_type} onChange={e => setContentReq({ ...contentReq, content_type: e.target.value })}>
              <option value="reel">Reel</option>
              <option value="carousel">Carousel</option>
              <option value="story">Story</option>
              <option value="post">Post</option>
            </select>
            <button className="btn-primary" onClick={handleGenerateCaption} disabled={loading}>
              {loading ? "Generating..." : "Generate Content"}
            </button>
          </div>
        )}

        {tab === "colors" && (
          <div className="card">
            <h2>Brand Color Intelligence</h2>
            <p className="subtitle">Upload images to analyze your brand palette</p>
            <input placeholder="Your niche (e.g. tarot, fitness)" value={colorNiche} onChange={e => setColorNiche(e.target.value)} />
            <textarea placeholder="Your vision (optional): I want to showcase..." value={colorVision} onChange={e => setColorVision(e.target.value)} rows={3} />
            <div className="upload-area" onClick={() => document.getElementById("fileInput").click()}>
              <input id="fileInput" type="file" multiple accept="image/*" style={{ display: "none" }}
                onChange={e => setColorFiles(Array.from(e.target.files))} />
              {colorFiles.length > 0
                ? <p>✅ {colorFiles.length} image(s) selected</p>
                : <p>📁 Click to upload images (select multiple)</p>}
            </div>
            <button className="btn-primary" onClick={handleAnalyzeColors} disabled={loading}>
              {loading ? "Analyzing..." : "Analyze Brand Colors"}
            </button>
          </div>
        )}

        {tab === "strategy" && (
          <div className="card">
            <h2>Strategy Knowledge Base</h2>
            <p className="subtitle">Ask questions from your marketing knowledge base</p>
            <input placeholder="e.g. How do I write a good hook?" value={ragQuestion} onChange={e => setRagQuestion(e.target.value)} />
            <button className="btn-primary" onClick={handleRagQuestion} disabled={loading}>
              {loading ? "Searching..." : "Ask Knowledge Base"}
            </button>
          </div>
        )}
        {tab === "trends" && (
  <TrendsTab />
)}

      

        {result && (
          <div className="result-card">
            {result.type === "caption" && (
              <div>
                <h3>Generated Content</h3>
                <pre>{result.data}</pre>
              </div>
            )}

            {result.type === "rag" && (
              <div>
                <h3>Strategy Answer</h3>
                <pre>{result.data}</pre>
              </div>
            )}

            {result.type === "colors" && (
              <div>
                <h3>Brand Analysis</h3>
                <div className="palette">
                  {result.data.unified_palette.map((c, i) => (
                    <div key={i} className="swatch-container">
                      <div className="swatch" style={{ backgroundColor: c.hex }} />
                      <span>{c.hex}</span>
                      <span>{c.percentage ? `${c.percentage}%` : ""}</span>
                    </div>
                  ))}
                </div>
                <div className="archetype-badge">
                  <span>Visual Archetype: </span>
                  <strong>{result.data.archetype.primary_archetype}</strong>
                  <span> ({result.data.archetype.confidence}% confidence)</span>
                </div>
                <div className="alignment" style={{ color: result.data.niche_alignment.aligned ? "#4caf50" : "#ff9800" }}>
                  {result.data.niche_alignment.message}
                </div>
                <h4>Recommended Colors for Your Niche</h4>
                <div className="palette">
                  {result.data.niche_recommended_colors.colors.map((c, i) => (
                    <div key={i} className="swatch-container">
                      <div className="swatch" style={{ backgroundColor: c }} />
                      <span>{result.data.niche_recommended_colors.names[i]}</span>
                      <span>{c}</span>
                    </div>
                  ))}
                </div>
                <h4>Brand Analysis</h4>
                <pre>{result.data.brand_analysis}</pre>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
