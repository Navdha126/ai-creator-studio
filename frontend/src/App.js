import { useState, useEffect, useRef } from "react";
import { Toaster, toast } from "react-hot-toast";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

const HOOK_VISUALS = {
  "Identity Hook": { gradient: "linear-gradient(135deg, #1a0533, #2d0a4e, #4a1a6b)", prompt: "person looking at camera confident portrait instagram reel dark purple aesthetic" },
  "Contrarian Hook": { gradient: "linear-gradient(135deg, #0d1a33, #1a2d4e, #0d3366)", prompt: "bold statement text aesthetic dark moody instagram reel blue purple" },
  "Authority Hook": { gradient: "linear-gradient(135deg, #1a1a0d, #2d2d0a, #4e4a1a)", prompt: "professional expert confident woman mystical golden aesthetic dark" },
  "Secret Hook": { gradient: "linear-gradient(135deg, #1a0d1a, #2d0a2d, #4e1a4e)", prompt: "mysterious dark aesthetic secret knowledge instagram reel deep purple" },
  "Action Hook": { gradient: "linear-gradient(135deg, #1a0d0d, #3d0a0a, #5c1a1a)", prompt: "energy motivation bold red dark aesthetic action instagram reel" },
  "Transformation Hook": { gradient: "linear-gradient(135deg, #0d1a0d, #0a2d1a, #1a4e2d)", prompt: "transformation before after glow aesthetic dark green gold" },
  "Number Hook": { gradient: "linear-gradient(135deg, #0d0d1a, #1a0a3d, #1a1a5c)", prompt: "numbered list aesthetic dark navy blue instagram content creator" },
  "Regret Hook": { gradient: "linear-gradient(135deg, #1a0a0d, #2d0a1a, #4e1a2d)", prompt: "emotional vulnerable storytelling aesthetic dark rose pink instagram" },
  "Curiosity Hook": { gradient: "linear-gradient(135deg, #0d1a1a, #0a2d2d, #1a4e4e)", prompt: "curious mysterious teal dark aesthetic instagram reel close up" },
  "Time Hook": { gradient: "linear-gradient(135deg, #1a1a0d, #2d2a0a, #4e3d1a)", prompt: "clock time countdown amber gold dark aesthetic instagram reel" },
  "Insider Hook": { gradient: "linear-gradient(135deg, #1a0533, #33051a, #4e1a33)", prompt: "exclusive insider knowledge luxury dark purple pink aesthetic" },
  "Contrarian Result Hook": { gradient: "linear-gradient(135deg, #0d1a0d, #1a3d1a, #2d5c2d)", prompt: "results transformation success dark emerald green aesthetic instagram" },
};

function InstagramPhoneMock() {
  const [trends, setTrends] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const [imageUrl, setImageUrl] = useState("");
  const [imageLoaded, setImageLoaded] = useState(false);
  const progressRef = useRef(null);

  useEffect(() => {
    axios.get(`${API}/trends`).then(res => setTrends(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (!trends?.hooks.length) return;
    clearInterval(progressRef.current);
    progressRef.current = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          setCurrentIndex(i => (i + 1) % trends.hooks.length);
          setImageLoaded(false);
          return 0;
        }
        return p + 2;
      });
    }, 100);
    return () => clearInterval(progressRef.current);
  }, [trends]);

  useEffect(() => {
    if (!trends?.hooks.length) return;
    const hook = trends.hooks[currentIndex];
    const visual = HOOK_VISUALS[hook.category] || HOOK_VISUALS["Identity Hook"];
    const encoded = encodeURIComponent(visual.prompt + " vertical 9:16");
    const seed = Math.floor(Math.random() * 9999);
    setImageUrl(`https://image.pollinations.ai/prompt/${encoded}?width=400&height=700&nologo=true&seed=${seed}`);
  }, [currentIndex, trends]);

  const current = trends?.hooks[currentIndex];
  const visual = current ? (HOOK_VISUALS[current.category] || HOOK_VISUALS["Identity Hook"]) : HOOK_VISUALS["Identity Hook"];

  return (
    <div className="phone-mock">
      <div className="phone-frame">
        <div className="phone-notch" />
        <div className="phone-screen">
          <div className="reel-bg" style={{ background: visual.gradient }} />
          {imageUrl && (
            <img
              src={imageUrl}
              alt="reel background"
              className={`reel-image ${imageLoaded ? "loaded" : ""}`}
              onLoad={() => setImageLoaded(true)}
              onError={() => setImageLoaded(false)}
            />
          )}
          <div className="reel-overlay" />

          <div className="reel-ig-header">
            <div className="reel-avatar">AI</div>
            <div>
              <div className="reel-username">ai.creator.studio</div>
            </div>
            <div className="reel-follow">Follow</div>
          </div>

          {current && (
            <div className="reel-hook-text">
              "{current.hook}"
            </div>
          )}

          <div className="reel-actions">
            <div className="reel-action-btn">
              <div className="reel-action-icon">❤️</div>
              <div className="reel-action-count">24.5K</div>
            </div>
            <div className="reel-action-btn">
              <div className="reel-action-icon">💬</div>
              <div className="reel-action-count">843</div>
            </div>
            <div className="reel-action-btn">
              <div className="reel-action-icon">➤</div>
              <div className="reel-action-count">1.2K</div>
            </div>
            <div className="reel-action-btn">
              <div className="reel-action-icon">🔖</div>
              <div className="reel-action-count">3.4K</div>
            </div>
          </div>

          {current && (
            <div className="reel-bottom">
              <div className="reel-category-badge">{current.category}</div>
              <div className="reel-caption">
                💡 {current.why_it_works?.slice(0, 60)}...
              </div>
            </div>
          )}

          <div className="reel-progress" style={{ width: `${progress}%` }} />
        </div>
      </div>
    </div>
  );
}

function Modal({ title, subtitle, onClose, children }) {
  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <button className="modal-close" onClick={onClose}>✕</button>
        <h2>{title}</h2>
        <p className="modal-subtitle">{subtitle}</p>
        {children}
      </div>
    </div>
  );
}

function ProfileModal({ onClose }) {
  const [profile, setProfile] = useState({ user_id: "", niche: "", tone: "", audience: "" });
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    if (!profile.user_id) return toast.error("Enter a User ID");
    try {
      setLoading(true);
      await axios.post(`${API}/save-profile`, profile);
      toast.success("Profile saved!");
    } catch {
      toast.error("Failed to save");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal title="Creator Profile" subtitle="Save your preferences — used across all features automatically" onClose={onClose}>
      <input placeholder="User ID (e.g. your name)" value={profile.user_id} onChange={e => setProfile({ ...profile, user_id: e.target.value })} />
      <input placeholder="Niche (e.g. tarot, fitness, fashion)" value={profile.niche} onChange={e => setProfile({ ...profile, niche: e.target.value })} />
      <input placeholder="Tone (e.g. mystical, energetic, professional)" value={profile.tone} onChange={e => setProfile({ ...profile, tone: e.target.value })} />
      <input placeholder="Target Audience (e.g. women 18-30)" value={profile.audience} onChange={e => setProfile({ ...profile, audience: e.target.value })} />
      <button className="btn-primary" onClick={handleSave} disabled={loading}>
        {loading ? "Saving..." : "Save Profile"}
      </button>
    </Modal>
  );
}

function ContentModal({ onClose }) {
  const [req, setReq] = useState({ user_id: "", content_type: "reel", vision: "" });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [savedProfile, setSavedProfile] = useState(null);
  const [imageData, setImageData] = useState(null);
  const [imageLoading, setImageLoading] = useState(false);
  const [customPrompt, setCustomPrompt] = useState("");
  const [showCustomise, setShowCustomise] = useState(false);

  const fetchProfile = async (userId) => {
    if (!userId) return setSavedProfile(null);
    try {
      const res = await axios.get(`${API}/get-profile/${userId}`);
      if (res.data.profile) setSavedProfile(res.data.profile);
      else setSavedProfile(null);
    } catch {
      setSavedProfile(null);
    }
  };

  const handleGenerate = async () => {
    if (!req.user_id) return toast.error("Enter your User ID");
    try {
      setLoading(true);
      setImageData(null);
      const res = await axios.post(`${API}/generate-caption`, req);
      setResult(res.data);
    } catch {
      toast.error("Failed to generate");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateImage = async (customVision = null) => {
    if (!req.user_id) return toast.error("Enter your User ID");
    try {
      setImageLoading(true);
      const vision = customVision || req.vision || `${savedProfile?.niche || "general"} Instagram post`;
      const res = await axios.post(`${API}/generate-post`, { user_id: req.user_id, vision });
      setImageData(res.data);
      setShowCustomise(false);
      setCustomPrompt("");
    } catch {
      toast.error("Failed to generate image");
    } finally {
      setImageLoading(false);
    }
  };

  return (
    <Modal title="Content Generator" subtitle="AI-powered post ideas, captions, hooks, and hashtags" onClose={onClose}>
      <input placeholder="User ID" value={req.user_id}
        onChange={e => { setReq({ ...req, user_id: e.target.value }); fetchProfile(e.target.value); }} />

      {savedProfile && (
        <div style={{ background: "#1e0d35", border: "1px solid #3a1a5a", borderRadius: "10px", padding: "10px 14px", marginBottom: "12px", fontSize: "0.82rem", color: "#9b7bb8" }}>
          ✦ Niche: <strong style={{ color: "#c084e8" }}>{savedProfile.niche}</strong> · Tone: <strong style={{ color: "#c084e8" }}>{savedProfile.tone}</strong> · Audience: <strong style={{ color: "#c084e8" }}>{savedProfile.audience}</strong>
        </div>
      )}

      <select value={req.content_type} onChange={e => setReq({ ...req, content_type: e.target.value })}>
        <option value="reel">Reel</option>
        <option value="carousel">Carousel</option>
        <option value="story">Story</option>
        <option value="post">Post</option>
      </select>

      <textarea placeholder="Your vision (optional): What do you want to post about?" value={req.vision}
        onChange={e => setReq({ ...req, vision: e.target.value })} rows={3} />

      <button className="btn-primary" onClick={handleGenerate} disabled={loading}>
        {loading ? "Generating..." : "Generate Content"}
      </button>

      {result && (
        <div>
          {result.trending_hook_used && (
            <div style={{ background: "#1e0d35", border: "1px solid #833AB4", borderRadius: "10px", padding: "12px 16px", marginTop: "16px", marginBottom: "4px" }}>
              <div style={{ fontSize: "0.7rem", color: "#C13584", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1px", marginBottom: "4px" }}>🔥 Trending Hook Used</div>
              <div style={{ fontSize: "0.82rem", color: "#c084e8", fontWeight: 500 }}>{result.trending_hook_used.category}</div>
              <div style={{ fontSize: "0.82rem", color: "#9b7bb8", fontStyle: "italic" }}>"{result.trending_hook_used.hook}"</div>
            </div>
          )}

          <div className="result-box">
            <h4>Generated Content</h4>
            <pre>{result.result}</pre>
          </div>

          <div style={{ marginTop: "20px", border: "1px solid #2a1a45", borderRadius: "14px", padding: "20px", background: "#0a0614" }}>
            <div style={{ fontSize: "0.85rem", fontWeight: 700, color: "#e0c8ff", marginBottom: "4px", fontFamily: "Inria Serif, serif" }}>🖼️ Post Image</div>
            <div style={{ fontSize: "0.78rem", color: "#4a3060", marginBottom: "14px" }}>Generate a brand-aligned image for this post</div>

            {!imageData && !imageLoading && (
              <button className="btn-primary" onClick={() => handleGenerateImage()}>Generate Post Image</button>
            )}

            {imageLoading && (
              <div style={{ textAlign: "center", padding: "20px", color: "#6b4f8a", fontSize: "0.85rem" }}>✨ Generating image...</div>
            )}

            {imageData && (
              <div>
                {imageData.image?.image_url && (
                  <div>
                    <img src={imageData.image.image_url} alt="Generated post"
                      style={{ width: "100%", borderRadius: "12px", marginBottom: "8px", border: "1px solid #2a1a45" }}
                      onError={e => { e.target.style.display = "none"; }} />
                    <button onClick={() => window.open(imageData.image.image_url, "_blank")}
                      style={{ display: "block", width: "100%", background: "transparent", border: "none", fontSize: "0.78rem", color: "#833AB4", marginBottom: "12px", textAlign: "center", cursor: "pointer" }}>
                      🔗 Open image in new tab
                    </button>
                  </div>
                )}
                <div style={{ fontSize: "0.78rem", color: "#4a3060", marginBottom: "12px", padding: "10px", background: "#1e0d35", borderRadius: "8px" }}>
                  <strong style={{ color: "#833AB4" }}>Prompt:</strong> {imageData.image?.prompt_used?.slice(0, 100)}...
                </div>
                <div style={{ display: "flex", gap: "8px" }}>
                  <button onClick={() => handleGenerateImage()} disabled={imageLoading}
                    style={{ flex: 1, padding: "10px", background: "transparent", border: "1px solid #C13584", borderRadius: "10px", color: "#C13584", cursor: "pointer", fontSize: "0.85rem", fontFamily: "Inter, sans-serif", fontWeight: 600 }}>
                    ↻ Regenerate
                  </button>
                  <button onClick={() => setShowCustomise(!showCustomise)}
                    style={{ flex: 1, padding: "10px", background: "transparent", border: "1px solid #833AB4", borderRadius: "10px", color: "#c084e8", cursor: "pointer", fontSize: "0.85rem", fontFamily: "Inter, sans-serif", fontWeight: 600 }}>
                    ✏️ Customise
                  </button>
                </div>
                {showCustomise && (
                  <div style={{ marginTop: "12px" }}>
                    <textarea placeholder="Describe changes..." value={customPrompt} onChange={e => setCustomPrompt(e.target.value)} rows={3}
                      style={{ width: "100%", padding: "12px", background: "#0a0614", border: "1px solid #2a1a45", borderRadius: "10px", color: "#e0c8ff", fontSize: "0.85rem", fontFamily: "Inter, sans-serif", outline: "none", marginBottom: "8px", resize: "vertical" }} />
                    <button className="btn-primary" onClick={() => handleGenerateImage(customPrompt)} disabled={imageLoading || !customPrompt}>
                      Generate Customised Image
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
}

function ColorsModal({ onClose }) {
  const [files, setFiles] = useState([]);
  const [niche, setNiche] = useState("");
  const [vision, setVision] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (files.length === 0) return toast.error("Upload at least one image");
    try {
      setLoading(true);
      const formData = new FormData();
      files.forEach(f => formData.append("files", f));
      formData.append("niche", niche || "general");
      if (vision) formData.append("vision", vision);
      const res = await axios.post(`${API}/analyze-colors`, formData);
      setResult(res.data);
    } catch {
      toast.error("Failed to analyze");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal title="Brand Color Intelligence" subtitle="Upload Instagram screenshots to detect your visual archetype" onClose={onClose}>
      <input placeholder="Your niche (e.g. tarot, fitness)" value={niche} onChange={e => setNiche(e.target.value)} />
      <textarea placeholder="Your vision (optional): I want to showcase..." value={vision} onChange={e => setVision(e.target.value)} rows={2} />
      <div className="upload-area" onClick={() => document.getElementById("colorFiles").click()}>
        <input id="colorFiles" type="file" multiple accept="image/*" style={{ display: "none" }}
          onChange={e => setFiles(Array.from(e.target.files))} />
        {files.length > 0 ? `✅ ${files.length} image(s) selected` : "📁 Click to upload images"}
      </div>
      <button className="btn-primary" onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Brand Colors"}
      </button>
      {result && (
        <div className="result-box">
          <h4>Color Palette</h4>
          <div className="palette">
            {result.unified_palette.map((c, i) => (
              <div key={i} className="swatch-container">
                <div className="swatch" style={{ backgroundColor: c.hex }} />
                <span>{c.hex}</span>
                {c.percentage && <span>{c.percentage}%</span>}
              </div>
            ))}
          </div>
          <div className="archetype-badge">
            <strong>{result.archetype.primary_archetype}</strong>
            <span> — {result.archetype.description}</span>
          </div>
          <div className="alignment" style={{ color: result.niche_alignment.aligned ? "#4ade80" : "#fb923c" }}>
            {result.niche_alignment.message}
          </div>
          <h4 style={{ marginTop: "16px" }}>Recommended for Your Niche</h4>
          <div className="palette">
            {result.niche_recommended_colors.colors.map((c, i) => (
              <div key={i} className="swatch-container">
                <div className="swatch" style={{ backgroundColor: c }} />
                <span>{result.niche_recommended_colors.names[i]}</span>
              </div>
            ))}
          </div>
          <h4 style={{ marginTop: "16px" }}>Brand Analysis</h4>
          <pre>{result.brand_analysis}</pre>
        </div>
      )}
    </Modal>
  );
}

function StrategyModal({ onClose }) {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question) return toast.error("Enter a question");
    try {
      setLoading(true);
      const res = await axios.post(`${API}/ask-knowledge-base`, { question });
      setResult(res.data.answer);
    } catch {
      toast.error("Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal title="Strategy Knowledge Base" subtitle="Ask questions — answers pulled from your marketing guides via RAG" onClose={onClose}>
      <input placeholder="e.g. How do I write a hook that stops the scroll?"
        value={question} onChange={e => setQuestion(e.target.value)}
        onKeyDown={e => e.key === "Enter" && handleAsk()} />
      <button className="btn-primary" onClick={handleAsk} disabled={loading}>
        {loading ? "Searching..." : "Ask Knowledge Base"}
      </button>
      {result && (
        <div className="result-box">
          <h4>Answer</h4>
          <pre>{result}</pre>
        </div>
      )}
    </Modal>
  );
}

function TrendsModal({ onClose }) {
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeSection, setActiveSection] = useState("hooks");

  const loadTrends = async () => {
    try {
      const res = await axios.get(`${API}/trends`);
      setTrends(res.data);
    } catch {
      toast.error("Failed to load");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await axios.post(`${API}/refresh-trends`);
      await loadTrends();
      toast.success("Trends refreshed!");
    } catch {
      toast.error("Failed to refresh");
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => { loadTrends(); }, []);

  return (
    <Modal title="Trending Hooks & Formats" subtitle="Auto-updated daily from top marketing sources" onClose={onClose}>
      <div style={{ display: "flex", gap: "8px", marginBottom: "20px", flexWrap: "wrap" }}>
        {["hooks", "formats", "articles"].map(s => (
          <button key={s} onClick={() => setActiveSection(s)}
            style={{ padding: "7px 14px", borderRadius: "8px", border: "1px solid", borderColor: activeSection === s ? "#C13584" : "#2a1a45", background: activeSection === s ? "#1e0d35" : "transparent", color: activeSection === s ? "#C13584" : "#6b4f8a", cursor: "pointer", fontSize: "0.82rem", fontFamily: "Inter, sans-serif" }}>
            {s === "hooks" ? "🪝 Hooks" : s === "formats" ? "🎬 Formats" : "📰 Articles"}
          </button>
        ))}
        <button onClick={handleRefresh} disabled={refreshing}
          style={{ marginLeft: "auto", padding: "7px 14px", borderRadius: "8px", border: "1px solid #2a1a45", background: "transparent", color: "#6b4f8a", cursor: "pointer", fontSize: "0.82rem", fontFamily: "Inter, sans-serif" }}>
          {refreshing ? "..." : "↻ Refresh"}
        </button>
      </div>
      {loading && <p style={{ color: "#4a3060" }}>Loading...</p>}
      {!loading && activeSection === "hooks" && trends?.hooks.map((hook, i) => (
        <div key={i} style={{ background: "#0a0614", border: "1px solid #2a1a45", borderRadius: "12px", padding: "16px", marginBottom: "10px" }}>
          <div style={{ fontSize: "0.7rem", color: "#C13584", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1px", marginBottom: "6px" }}>{hook.category}</div>
          <div style={{ fontSize: "0.9rem", color: "#e0c8ff", fontWeight: 600, marginBottom: "6px", lineHeight: 1.5 }}>"{hook.hook}"</div>
          <div style={{ fontSize: "0.8rem", color: "#6b4f8a", marginBottom: "4px" }}>💡 {hook.why_it_works}</div>
          <div style={{ fontSize: "0.8rem", color: "#833AB4", fontStyle: "italic" }}>📝 {hook.example}</div>
        </div>
      ))}
      {!loading && activeSection === "formats" && trends?.formats.map((f, i) => (
        <div key={i} style={{ background: "#0a0614", border: "1px solid #2a1a45", borderRadius: "12px", padding: "16px", marginBottom: "10px" }}>
          <div style={{ fontSize: "0.7rem", color: "#C13584", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1px", marginBottom: "6px" }}>{f.best_for}</div>
          <div style={{ fontSize: "0.92rem", color: "#e0c8ff", fontWeight: 600, marginBottom: "8px" }}>{f.format}</div>
          <div style={{ fontSize: "0.82rem", color: "#6b4f8a", marginBottom: "4px" }}>🎥 {f.film}</div>
          <div style={{ fontSize: "0.82rem", color: "#6b4f8a", marginBottom: "4px" }}>✍️ {f.text}</div>
          <div style={{ fontSize: "0.82rem", color: "#6b4f8a" }}>🎵 {f.sound}</div>
        </div>
      ))}
      {!loading && activeSection === "articles" && (
        trends?.articles.length === 0
          ? <p style={{ color: "#4a3060" }}>No articles yet. Click Refresh.</p>
          : trends?.articles.map((a, i) => (
            <div key={i} style={{ background: "#0a0614", border: "1px solid #2a1a45", borderRadius: "12px", padding: "16px", marginBottom: "10px" }}>
              <div style={{ fontSize: "0.7rem", color: "#6b4f8a", marginBottom: "4px" }}>{a.source}</div>
              <button onClick={() => window.open(a.link, "_blank")} style={{ background: "none", border: "none", color: "#c084e8", fontSize: "0.88rem", fontWeight: 500, cursor: "pointer", padding: 0, textAlign: "left" }}>
                {a.title}
              </button>
            </div>
          ))
      )}
    </Modal>
  );
}

function PostModal({ onClose }) {
  const [userId, setUserId] = useState("");
  const [vision, setVision] = useState("");
  const [savedProfile, setSavedProfile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [customPrompt, setCustomPrompt] = useState("");
  const [showCustomise, setShowCustomise] = useState(false);

  const fetchProfile = async (id) => {
    if (!id) return setSavedProfile(null);
    try {
      const res = await axios.get(`${API}/get-profile/${id}`);
      if (res.data.profile) setSavedProfile(res.data.profile);
      else setSavedProfile(null);
    } catch {
      setSavedProfile(null);
    }
  };

  const handleGenerate = async (customVision = null) => {
    if (!userId) return toast.error("Enter your User ID");
    try {
      setLoading(true);
      const res = await axios.post(`${API}/generate-post`, {
        user_id: userId,
        vision: customVision || vision || `${savedProfile?.niche || "general"} Instagram post`
      });
      setResult(res.data);
      setShowCustomise(false);
      setCustomPrompt("");
    } catch {
      toast.error("Failed to generate post");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal title="Post Generator" subtitle="Generate a complete branded Instagram post with AI image and caption" onClose={onClose}>
      <input placeholder="User ID" value={userId}
        onChange={e => { setUserId(e.target.value); fetchProfile(e.target.value); }} />
      {savedProfile && (
        <div style={{ background: "#1e0d35", border: "1px solid #3a1a5a", borderRadius: "10px", padding: "10px 14px", marginBottom: "12px", fontSize: "0.82rem", color: "#9b7bb8" }}>
          ✦ Niche: <strong style={{ color: "#c084e8" }}>{savedProfile.niche}</strong> · Tone: <strong style={{ color: "#c084e8" }}>{savedProfile.tone}</strong>
        </div>
      )}
      <textarea placeholder="What do you want to post about?" value={vision} onChange={e => setVision(e.target.value)} rows={3} />
      <button className="btn-primary" onClick={() => handleGenerate()} disabled={loading}>
        {loading ? "Creating your post..." : "Generate Post"}
      </button>
      {result && (
        <div style={{ marginTop: "20px" }}>
          {result.image?.image_url && (
            <div>
              <img src={result.image.image_url} alt="Generated post"
                style={{ width: "100%", borderRadius: "14px", marginBottom: "8px", border: "1px solid #2a1a45" }}
                onError={e => { e.target.style.display = "none"; }} />
              <button onClick={() => window.open(result.image.image_url, "_blank")}
                style={{ display: "block", width: "100%", background: "transparent", border: "none", fontSize: "0.78rem", color: "#833AB4", marginBottom: "12px", textAlign: "center", cursor: "pointer" }}>
                🔗 Open image in new tab
              </button>
            </div>
          )}
          <div style={{ background: "#1e0d35", border: "1px solid #3a1a5a", borderRadius: "10px", padding: "12px 16px", marginBottom: "12px" }}>
            <div style={{ fontSize: "0.7rem", color: "#C13584", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1px", marginBottom: "6px" }}>Generated Caption</div>
            <pre style={{ color: "#9b7bb8", fontSize: "0.85rem" }}>{result.caption}</pre>
          </div>
          <div style={{ background: "#0a0614", border: "1px solid #2a1a45", borderRadius: "10px", padding: "10px 14px", marginBottom: "16px", fontSize: "0.75rem", color: "#4a3060" }}>
            <strong style={{ color: "#833AB4" }}>Image prompt:</strong> {result.image?.prompt_used?.slice(0, 100)}...
          </div>
          <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
            <button onClick={() => handleGenerate()} disabled={loading}
              style={{ flex: 1, padding: "10px", background: "transparent", border: "1px solid #C13584", borderRadius: "10px", color: "#C13584", cursor: "pointer", fontSize: "0.85rem", fontFamily: "Inter, sans-serif", fontWeight: 600 }}>
              ↻ Regenerate
            </button>
            <button onClick={() => setShowCustomise(!showCustomise)}
              style={{ flex: 1, padding: "10px", background: "transparent", border: "1px solid #833AB4", borderRadius: "10px", color: "#c084e8", cursor: "pointer", fontSize: "0.85rem", fontFamily: "Inter, sans-serif", fontWeight: 600 }}>
              ✏️ Customise
            </button>
          </div>
          {showCustomise && (
            <div>
              <textarea placeholder="Describe changes..." value={customPrompt} onChange={e => setCustomPrompt(e.target.value)} rows={3}
                style={{ width: "100%", padding: "12px", background: "#0a0614", border: "1px solid #2a1a45", borderRadius: "10px", color: "#e0c8ff", fontSize: "0.85rem", fontFamily: "Inter, sans-serif", outline: "none", marginBottom: "8px", resize: "vertical" }} />
              <button className="btn-primary" onClick={() => handleGenerate(customPrompt)} disabled={loading || !customPrompt}>
                Generate Customised Post
              </button>
            </div>
          )}
        </div>
      )}
    </Modal>
  );
}

const TOOLS = [
  { id: "profile", icon: "👤", title: "Creator Profile", desc: "Save your niche, tone, and audience once" },
  { id: "content", icon: "✍️", title: "Content Generator", desc: "AI captions, hooks, and hashtags" },
  { id: "colors", icon: "🎨", title: "Color Intelligence", desc: "Detect your visual archetype" },
  { id: "strategy", icon: "📚", title: "Strategy Q&A", desc: "RAG-powered marketing answers" },
  { id: "trends", icon: "🔥", title: "Trends Feed", desc: "Daily hook updates" },
  { id: "post", icon: "🖼️", title: "Post Generator", desc: "AI image + caption + hashtags" },
];

const SHOWCASE = [
  {
    number: "01", icon: "👤", title: "The AI remembers you.",
    desc: "Save your profile once and every feature in the studio automatically personalizes to your niche, tone, and target audience. No need to repeat yourself — the AI remembers.",
    features: ["Persistent memory across sessions", "Niche and tone stored automatically", "Drives personalization in every feature"],
    id: "profile"
  },
  {
    number: "02", icon: "✍️", title: "Content that actually sounds like you.",
    desc: "Generate on-brand Instagram captions, hook lines, and hashtag sets in seconds. The AI uses your saved profile and pulls from trending hooks automatically.",
    features: ["Post idea with real specific examples", "3 captions with different angles", "10 relevant hashtags", "Trending hook integrated automatically"],
    id: "content"
  },
  {
    number: "03", icon: "🎨", title: "Your brand has a personality.",
    desc: "Upload your Instagram screenshots and the system extracts your dominant colors, detects your visual archetype from 8 possible types, and tells you whether your palette aligns with your niche.",
    features: ["K-Means color extraction from images", "8 visual archetypes detected", "20+ niche color databases", "Alignment scoring with your niche"],
    id: "colors"
  },
  {
    number: "04", icon: "📚", title: "Strategy from your own knowledge.",
    desc: "Upload marketing PDFs and guides. Ask any question and the system retrieves the most relevant knowledge using RAG — not just keyword search, actual semantic understanding.",
    features: ["PDF ingestion and chunking", "Semantic search with ChromaDB", "Sentence Transformer embeddings", "Context-aware LLM answers"],
    id: "strategy"
  },
  {
    number: "05", icon: "🔥", title: "Always know what's trending.",
    desc: "A background scheduler fetches fresh articles daily from Buffer, Sprout Social, and Social Media Examiner. The AI reads them and extracts trending hook templates automatically.",
    features: ["Auto-refreshes every 24 hours", "12 built-in hook frameworks", "6 content formats with filming instructions", "Real articles from top marketing sources"],
    id: "trends"
  },
  {
    number: "06", icon: "🖼️", title: "Generate a complete post.",
    desc: "Generate a complete Instagram post in one click. AI creates a brand-aligned image, paired with a matching caption and hashtags. Regenerate or customise with your own prompt.",
    features: ["Brand-aligned image generation", "Matching caption and hashtags", "Regenerate with one click", "Customise image with your own prompt"],
    id: "post"
  },
];

export default function App() {
  const [activeModal, setActiveModal] = useState(null);

  return (
    <div>
      <Toaster position="top-center" toastOptions={{
        style: { background: "#160d28", color: "#e0c8ff", border: "1px solid #3a1a5a" }
      }} />

      <nav className="navbar">
        <div className="navbar-logo">✦ AI Creator Studio</div>
        <ul className="navbar-links">
          <li><button onClick={() => document.getElementById("about").scrollIntoView({ behavior: "smooth" })}>About</button></li>
          <li><button onClick={() => document.getElementById("showcase").scrollIntoView({ behavior: "smooth" })}>Tools</button></li>
          <li><button onClick={() => document.getElementById("footer").scrollIntoView({ behavior: "smooth" })}>Contact</button></li>
        </ul>
      </nav>

      {/* Hero */}
      <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 60px" }}>
        <section className="hero">
          <div style={{ position: "relative", zIndex: 1 }}>
            <InstagramPhoneMock />
          </div>

          <div className="hero-right" style={{ position: "relative", zIndex: 1 }}>
            <div className="orb orb-purple" style={{ top: "-100px", right: "-100px" }} />
            <div className="hero-badge">✦ Built for Instagram Creators</div>
            <h1>
              <span className="ig-gradient">Your AI Brand</span>
              <br />Strategist
            </h1>
            <p>
              Generate on-brand content, detect your visual archetype,
              retrieve marketing strategy, and stay on top of trending hooks —
              all in one place.
            </p>
            <div className="tools-grid">
              {TOOLS.map(tool => (
                <div key={tool.id} className="tool-card" onClick={() => setActiveModal(tool.id)}>
                  <div className="tool-card-icon">{tool.icon}</div>
                  <h3>{tool.title}</h3>
                  <p>{tool.desc}</p>
                  <div className="tool-card-arrow">→</div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      {/* About */}
      <section className="about-section" id="about">
        <div className="orb orb-pink" style={{ top: "20%", left: "-100px" }} />
        <div className="orb orb-purple" style={{ bottom: "10%", right: "-100px" }} />
        <div className="about-inner">
          <h2>Engineered for creators,<br /><span className="ig-gradient">not marketers.</span></h2>
          <p className="subtitle">
            Most AI tools are built for marketing teams with big budgets.
            This one is built for creators who want to grow on Instagram
            with real strategy, not guesswork.
          </p>
          <div className="perks-grid">
            {[
              { icon: "🧠", title: "Remembers You", desc: "Save your profile once. Every tool automatically uses your niche, tone, and audience — no repetition." },
              { icon: "🎨", title: "Brand Intelligence", desc: "Not just color extraction. The system detects your visual archetype and tells you if it aligns with your niche." },
              { icon: "📚", title: "Real Knowledge", desc: "RAG-powered answers from your actual marketing documents — not hallucinated generics." },
              { icon: "🔥", title: "Always Current", desc: "Trending hooks and formats pulled daily from top marketing sources. Automatically. No manual updates." },
              { icon: "⚡", title: "Actually Fast", desc: "Powered by Groq's Llama 3.3 70B — one of the fastest LLM inference engines available." },
              { icon: "🔮", title: "20+ Niches", desc: "Color recommendations and archetype detection tuned for 20+ creator niches from tarot to tech." },
            ].map((perk, i) => (
              <div key={i} className="perk-card">
                <div className="perk-icon">{perk.icon}</div>
                <h3>{perk.title}</h3>
                <p>{perk.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tool Showcase */}
      <div id="showcase">
        {SHOWCASE.map((item, i) => (
          <section key={i} className="tool-showcase">
            <div className="orb orb-purple" style={{ top: "20%", left: i % 2 === 0 ? "-150px" : "auto", right: i % 2 !== 0 ? "-150px" : "auto" }} />
            <div className="showcase-inner" style={{ direction: i % 2 !== 0 ? "rtl" : "ltr" }}>
              <div className="showcase-text" style={{ direction: "ltr" }}>
                <div className="showcase-number">{item.number} — {item.title.split(" ")[0].toUpperCase()}</div>
                <h3>{item.title}</h3>
                <p>{item.desc}</p>
                <ul className="showcase-features">
                  {item.features.map((f, j) => <li key={j}>{f}</li>)}
                </ul>
                <button
                  onClick={() => setActiveModal(item.id)}
                  style={{ marginTop: "24px", padding: "12px 28px", background: "linear-gradient(45deg, #833AB4, #C13584)", border: "none", borderRadius: "12px", color: "white", fontSize: "0.9rem", fontWeight: 600, cursor: "pointer", fontFamily: "Inter, sans-serif" }}
                >
                  Try {item.title.split(" ").slice(-1)} →
                </button>
              </div>
              <div className="showcase-visual" style={{ direction: "ltr" }}>
                <span style={{ fontSize: "6rem", position: "relative", zIndex: 1 }}>{item.icon}</span>
              </div>
            </div>
          </section>
        ))}
      </div>

      {/* Footer */}
      <footer className="footer" id="footer">
        <h3>✦ AI Creator Studio</h3>
        <p>Built by Navdha </p>
        <div className="footer-links">
          <button onClick={() => window.open("https://github.com/Navdha126/ai-creator-studio", "_blank")}>GitHub</button>
          <button onClick={() => window.open("http://127.0.0.1:8000/docs", "_blank")}>API Docs</button>
        </div>
      </footer>

      {activeModal === "profile" && <ProfileModal onClose={() => setActiveModal(null)} />}
      {activeModal === "content" && <ContentModal onClose={() => setActiveModal(null)} />}
      {activeModal === "colors" && <ColorsModal onClose={() => setActiveModal(null)} />}
      {activeModal === "strategy" && <StrategyModal onClose={() => setActiveModal(null)} />}
      {activeModal === "trends" && <TrendsModal onClose={() => setActiveModal(null)} />}
      {activeModal === "post" && <PostModal onClose={() => setActiveModal(null)} />}
    </div>
  );
}