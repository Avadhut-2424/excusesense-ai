import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(page_title="ExcuseSense v2.0", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

API_URL = "http://localhost:8000"

# Fetch Stats
try:
    stats_res = requests.get(f"{API_URL}/stats").json()
    acc_val = stats_res.get("model_accuracy", 1.0) * 100
    ACC_PCT = int(acc_val) if acc_val.is_integer() else round(acc_val, 1)
except Exception:
    ACC_PCT = 100
    stats_res = {"total": 0, "genuine": 0, "suspicious": 0, "emotional": 0}

# Advanced CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

:root {{
    --bg: #080c14;
    --card: #0e1420;
    --border: #1e2d40;
    --teal: #2dd4bf;
    --blue: #0ea5e9;
    --green: #22c55e;
    --amber: #f59e0b;
    --purple: #a855f7;
    --text: #f8fafc;
    --muted: #94a3b8;
}}

/* Global fonts: avoid overriding Streamlit icon ligatures */
.stApp, .stApp *:not(.material-symbols-rounded):not([class*="material-symbol"]) {{
    font-family: 'Inter', sans-serif !important;
}}
.material-symbols-rounded,
[class*="material-symbol"] {{
    font-family: "Material Symbols Rounded" !important;
    font-style: normal !important;
    font-weight: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    direction: ltr !important;
}}
.stApp {{
    background-color: var(--bg) !important;
    background-image: radial-gradient(circle at center, rgba(45,212,191,0.03) 0%, transparent 100%), 
                      radial-gradient(rgba(255,255,255,0.02) 1px, transparent 1px) !important;
    background-size: 100% 100%, 20px 20px !important;
}}

/* Hide default streamlit elements (but keep header so sidebar toggle works) */
footer {{ display: none !important; }}
.stAppDeployButton {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}

/* Sidebar layout */
section[data-testid="stSidebar"] {{
    background-color: #05080f !important;
    border-right: 1px solid var(--border) !important;
    width: 260px !important;
}}

/* Card global */
.stCard {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,200,255,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.stCard:hover {{ transform: translateY(-2px); box-shadow: 0 4px 24px rgba(45,212,191,0.08); }}

/* Inputs */
.stTextArea textarea {{
    background: #0a1120 !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
}}
.stTextArea textarea:focus {{
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 2px rgba(45,212,191,0.2) !important;
}}

/* Analyze Button */
.btn-analyze button {{
    background: linear-gradient(135deg, var(--blue), var(--teal)) !important;
    color: #000 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px !important;
    transition: all 0.2s ease !important;
    position: relative;
    overflow: hidden;
}}
.btn-analyze button:active {{ transform: scale(0.97) !important; }}
.btn-analyze button::after {{
    content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 3s infinite;
}}
@keyframes shimmer {{ 0% {{left: -100%}} 100% {{left: 200%}} }}

/* Sidebar Button Overrides via Adjacency Hack */
.element-container:has(.btn-marker-genuine) + .element-container button {{ 
    background: linear-gradient(145deg, #0d3d2e, #072219) !important; 
    color: #2dd4bf !important; 
    border: 1px solid #115e45 !important; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    border-radius: 8px !important; transition: all 0.2s ease !important;
}}
.element-container:has(.btn-marker-genuine) + .element-container button:hover {{ 
    background: linear-gradient(145deg, #115e45, #0d3d2e) !important; 
    border-color: #2dd4bf !important; 
    transform: translateY(-2px) !important; 
    box-shadow: 0 6px 16px rgba(45,212,191,0.2) !important;
}}

.element-container:has(.btn-marker-suspicious) + .element-container button {{ 
    background: linear-gradient(145deg, #3d2a0d, #241807) !important; 
    color: #f59e0b !important; 
    border: 1px solid #78350f !important; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    border-radius: 8px !important; transition: all 0.2s ease !important;
}}
.element-container:has(.btn-marker-suspicious) + .element-container button:hover {{ 
    background: linear-gradient(145deg, #78350f, #3d2a0d) !important; 
    border-color: #f59e0b !important; 
    transform: translateY(-2px) !important; 
    box-shadow: 0 6px 16px rgba(245,158,11,0.2) !important;
}}

.element-container:has(.btn-marker-emotional) + .element-container button {{ 
    background: linear-gradient(145deg, #2d1054, #19092e) !important; 
    color: #a78bfa !important; 
    border: 1px solid #4c1d95 !important; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    border-radius: 8px !important; transition: all 0.2s ease !important;
}}
.element-container:has(.btn-marker-emotional) + .element-container button:hover {{ 
    background: linear-gradient(145deg, #4c1d95, #2d1054) !important; 
    border-color: #a78bfa !important; 
    transform: translateY(-2px) !important; 
    box-shadow: 0 6px 16px rgba(167,139,250,0.2) !important;
}}

[data-testid="stSidebar"] button p {{
    font-weight: 500 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
}}

/* Animations */
@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.animate-result {{ animation: slideUp 0.4s ease forwards; }}

/* Tabs styling */
div[data-testid="stTabs"] button {{
    color: var(--muted) !important;
    font-weight: 500 !important;
}}
div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--teal) !important;
    border-bottom-color: var(--teal) !important;
}}

/* Metric Cards */
div[data-testid="metric-container"] {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 0 20px rgba(0,200,255,0.03);
}}

/* Colorful horizontal accent bars */
.hbar-main {{
    height: 4px;
    border-radius: 999px;
    background: linear-gradient(90deg, #166534 0%, #22c55e 55%, #4ade80 100%);
    box-shadow: 0 0 20px rgba(34,197,94,0.18);
    margin: -10px 0 16px 0;
}}
.hbar-soft {{
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(120,53,15,0.95) 0%, rgba(234,179,8,0.78) 55%, rgba(253,224,71,0.56) 100%);
    margin: 6px 0 12px 0;
}}
.hbar-amber {{
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(127,29,29,0.96) 0%, rgba(239,68,68,0.75) 55%, rgba(252,165,165,0.52) 100%);
    margin: 6px 0 12px 0;
}}

/* Subtle horizontal background stripe behind Analyze section */
.hbar-bg {{
    height: 44px;
    border-radius: 10px;
    background: linear-gradient(
        90deg,
        rgba(22,101,52,0.14) 0%,
        rgba(34,197,94,0.12) 55%,
        rgba(74,222,128,0.10) 100%
    );
    border: 1px solid rgba(34,197,94,0.2);
    margin: 6px 0 14px 0;
}}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0 20px 0; border-bottom:1px solid #1e2d40; margin-bottom:20px;">
    <div style="display:flex; align-items:center; gap:12px;">
        <svg width="40" height="40" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="gradA" x1="24" y1="4" x2="24" y2="24" gradientUnits="userSpaceOnUse"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#0ea5e9"/></linearGradient>
                <linearGradient id="gradB" x1="4" y1="16" x2="24" y2="44" gradientUnits="userSpaceOnUse"><stop stop-color="#0ea5e9"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
                <linearGradient id="gradC" x1="44" y1="16" x2="24" y2="44" gradientUnits="userSpaceOnUse"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#10b981"/></linearGradient>
            </defs>
            <path d="M24 4L4 16L24 28L44 16L24 4Z" fill="url(#gradA)"/><path d="M4 16V36L24 48V28L4 16Z" fill="url(#gradB)"/><path d="M44 16V36L24 48V28L44 16Z" fill="url(#gradC)"/>
            <path d="M24 12L25.5 19.5L33 21L25.5 22.5L24 30L22.5 22.5L15 21L22.5 19.5L24 12Z" fill="#ffffff" opacity="0.95"/>
        </svg>
        <div>
            <div style="font-size:22px; font-weight:600; color:#fff; display:flex; align-items:center; gap:6px;">
                ExcuseSense <span style="width:6px; height:6px; background:#2dd4bf; border-radius:50%; box-shadow:0 0 8px #2dd4bf;"></span>
            </div>
            <div style="font-size:12px; color:#94a3b8;">Leave Intelligence Platform</div>
        </div>
    </div>
    <div style="display:flex; gap:8px; align-items:center;"></div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="hbar-main"></div>', unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <svg width="32" height="32" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="gradA" x1="24" y1="4" x2="24" y2="24" gradientUnits="userSpaceOnUse"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#0ea5e9"/></linearGradient>
                <linearGradient id="gradB" x1="4" y1="16" x2="24" y2="44" gradientUnits="userSpaceOnUse"><stop stop-color="#0ea5e9"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
                <linearGradient id="gradC" x1="44" y1="16" x2="24" y2="44" gradientUnits="userSpaceOnUse"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#10b981"/></linearGradient>
            </defs>
            <path d="M24 4L4 16L24 28L44 16L24 4Z" fill="url(#gradA)"/><path d="M4 16V36L24 48V28L4 16Z" fill="url(#gradB)"/><path d="M44 16V36L24 48V28L44 16Z" fill="url(#gradC)"/>
            <path d="M24 12L25.5 19.5L33 21L25.5 22.5L24 30L22.5 22.5L15 21L22.5 19.5L24 12Z" fill="#ffffff" opacity="0.95"/>
        </svg>
        <span style="font-size:20px; font-weight:600; color:#fff;">ExcuseSense</span>
        <span style="font-size:10px; background:#1e2d40; padding:2px 6px; border-radius:4px; color:#94a3b8;">v2.0</span>
    </div>
    <hr style="border-color:#1e2d40; margin-bottom:20px;">
    <div class="stCard" style="padding:16px; margin-bottom:24px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:16px; color:#fff; font-size:14px; font-weight:500;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg> Logistic Regression
        </div>
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
            <div style="position:relative; width:48px; height:48px;">
                <svg viewBox="0 0 36 36" style="width:100%; height:100%; transform: rotate(-90deg);">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#1e2d40" stroke-width="3"/>
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#2dd4bf" stroke-width="3" stroke-dasharray="{ACC_PCT}, 100" style="animation: fillRing 1.5s ease-out forwards; stroke-linecap: round;"/>
                </svg>
                <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#fff;">{ACC_PCT}%</div>
            </div>
            <div>
                <div style="font-size:12px; color:#94a3b8; font-weight:600; text-transform:uppercase;">Model Accuracy</div>
                <div style="font-size:11px; color:#2dd4bf; margin-top:2px;">Optimal Performance</div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; padding-top:12px; border-top:1px solid #1e2d40;">
            <span style="font-size:11px; color:#94a3b8;">Features: TF-IDF</span>
            <span style="font-size:11px; color:#94a3b8;">Classes: 3</span>
        </div>
    </div>
    <div style="font-size:12px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Sample Inputs</div>
    """, unsafe_allow_html=True)

    if "user_text" not in st.session_state:
        st.session_state.user_text = ""

    st.markdown('<div class="btn-marker-genuine" style="display:none;"></div>', unsafe_allow_html=True)
    if st.button("Genuine", key="s1", use_container_width=True):
        st.session_state.user_text = "I am suffering from a high fever and the doctor advised 3 days of rest."

    st.markdown('<div class="btn-marker-suspicious" style="display:none;"></div>', unsafe_allow_html=True)
    if st.button("Suspicious", key="s2", use_container_width=True):
        st.session_state.user_text = "I cannot come today because my car keys were stolen by a gang of monkeys."

    st.markdown('<div class="btn-marker-emotional" style="display:none;"></div>', unsafe_allow_html=True)
    if st.button("Emotional", key="s3", use_container_width=True):
        st.session_state.user_text = "I feel completely burnt out and need a mental health day to breathe and recover."

    st.markdown("""
    <div style="margin-top:14px; padding-top:12px; border-top:1px solid #1e2d40; display:flex; align-items:center; gap:8px; font-size:12px; color:#94a3b8;">
        <div style="width:8px; height:8px; background:#22c55e; border-radius:50%; box-shadow:0 0 10px #22c55e;"></div>
        Model Status: Online
    </div>
    """, unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────
t_analyze, t_history, t_dash = st.tabs(["🎯 Analyze", "🕒 History", "📊 Dashboard"])

with t_analyze:
    st.markdown('<div class="hbar-bg"></div>', unsafe_allow_html=True)
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.markdown("""
        <div style="margin-bottom:12px; display:flex; align-items:center; gap:8px;">
            <span style="font-size:16px; font-weight:600; color:#fff;">Leave Application Analysis</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="hbar-soft"></div>', unsafe_allow_html=True)

        user_input = st.text_area(
            label="Application Text",
            value=st.session_state.user_text,
            height=280,
            placeholder="Enter leave application text here...",
            label_visibility="collapsed"
        )
        st.markdown(f"<div style='font-size:12px; color:#94a3b8; margin-bottom:16px;'>{len(user_input)} characters</div>", unsafe_allow_html=True)

        st.markdown('<div class="btn-analyze">', unsafe_allow_html=True)
        analyze_btn = st.button("⚡ Analyze Application", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_output:
        if analyze_btn:
            if not user_input.strip():
                st.warning("Please enter text to analyze.")
            else:
                try:
                    res = requests.post(f"{API_URL}/analyze", json={"text": user_input})
                    if res.status_code == 200:
                        data = res.json()
                        pred = data["prediction"]
                        conf = data["confidence"]
                        kw = data["keywords"]
                        probs = data["probabilities"]

                        cfg = {
                            "Genuine": {"color": "#22c55e", "bg": "rgba(34,197,94,0.1)", "glow": "rgba(34,197,94,0.2)"},
                            "Suspicious": {"color": "#f59e0b", "bg": "rgba(245,158,11,0.1)", "glow": "rgba(245,158,11,0.2)"},
                            "Emotional": {"color": "#a855f7", "bg": "rgba(168,85,247,0.1)", "glow": "rgba(168,85,247,0.2)"}
                        }.get(pred, {"color": "#fff", "bg": "#000", "glow": "#000"})

                        st.markdown(f"""
                        <div style="margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                            <span style="font-size:16px; font-weight:600; color:#fff;">Analysis Result</span>
                        </div>
                        <div class="stCard animate-result" style="padding:24px; border-top:3px solid {cfg['color']};">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
                                <div style="display:flex; align-items:center; gap:16px;">
                                    <div style="background:{cfg['bg']}; color:{cfg['color']}; padding:10px 24px; border-radius:8px; font-size:24px; font-weight:700; border:1px solid {cfg['color']}; box-shadow:0 0 20px {cfg['glow']};">
                                        {pred.upper()}
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:36px; font-weight:700; color:#fff;">{conf*100:.1f}%</div>
                                    <div style="font-size:12px; color:#94a3b8; text-transform:uppercase;">Confidence Score</div>
                                </div>
                            </div>
                            <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:24px;">
                                <div style="display:flex; justify-content:space-between; align-items:center; background:#0a1120; border:1px solid #1e2d40; border-radius:8px; padding:12px 16px;">
                                    <div style="font-size:13px; color:#94a3b8; font-weight:500;">Genuine</div>
                                    <div style="font-size:16px; color:#22c55e; font-weight:600;">{probs.get('Genuine',0)*100:.1f}%</div>
                                </div>
                                <div style="display:flex; justify-content:space-between; align-items:center; background:#0a1120; border:1px solid #1e2d40; border-radius:8px; padding:12px 16px;">
                                    <div style="font-size:13px; color:#94a3b8; font-weight:500;">Suspicious</div>
                                    <div style="font-size:16px; color:#f59e0b; font-weight:600;">{probs.get('Suspicious',0)*100:.1f}%</div>
                                </div>
                                <div style="display:flex; justify-content:space-between; align-items:center; background:#0a1120; border:1px solid #1e2d40; border-radius:8px; padding:12px 16px;">
                                    <div style="font-size:13px; color:#94a3b8; font-weight:500;">Emotional</div>
                                    <div style="font-size:16px; color:#a855f7; font-weight:600;">{probs.get('Emotional',0)*100:.1f}%</div>
                                </div>
                            </div>
                            <div>
                                <div style="font-size:12px; color:#94a3b8; margin-bottom:8px; font-weight:600; text-transform:uppercase;">Extracted Keywords</div>
                                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                                    {"".join([f"<span style='background:{cfg['bg']}; color:{cfg['color']}; padding:6px 14px; border-radius:20px; font-size:13px; font-weight:500; border:1px solid {cfg['glow']}'>{w}</span>" for w in kw]) if kw else "<span style='color:#94a3b8; font-size:13px;'>No strong features found</span>"}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Radar Chart
                        st.markdown("<div class='animate-result' style='margin-top:20px;'>", unsafe_allow_html=True)
                        categories = ['Genuine', 'Suspicious', 'Emotional']
                        fig = go.Figure(data=go.Scatterpolar(
                          r=[probs.get(c,0) for c in categories],
                          theta=categories,
                          fill='toself',
                          fillcolor=cfg['bg'].replace('0.1', '0.4'),
                          line_color=cfg['color']
                        ))
                        fig.update_layout(
                          polar=dict(
                            radialaxis=dict(visible=True, range=[0, 1], color="#94a3b8", gridcolor="#1e2d40", showline=False),
                            angularaxis=dict(color="#f8fafc", gridcolor="#1e2d40", linecolor="#1e2d40")
                          ),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=40, r=40, t=20, b=20),
                          height=280
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error from API")
                except Exception as e:
                    st.error("Failed to connect to backend.")
        else:
            st.markdown("""
            <div style="margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                <span style="font-size:16px; font-weight:600; color:#fff;">Analysis Result</span>
            </div>
            <div class="hbar-amber"></div>
            <div style="height:280px; display:flex; align-items:center; justify-content:center; flex-direction:column; color:#94a3b8; padding:40px 20px; text-align:center; border:1px dashed #1e2d40; border-radius:12px; background:rgba(10,17,32,0.5);">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1e2d40" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                <div style="margin-top:16px; font-weight:500; font-size:14px; color:#f8fafc;">Awaiting Application</div>
                <div style="font-size:12px; margin-top:6px;">Submit an application on the left to view the AI analysis.</div>
            </div>
            """, unsafe_allow_html=True)

with t_history:
    st.markdown("<h3 style='color:#fff; font-size:18px; margin-bottom:16px;'>Past Analyses</h3>", unsafe_allow_html=True)
    
with t_history:
    import json
    import streamlit.components.v1 as components

    st.markdown("<h3 style='color:#fff; font-size:18px; margin-bottom:16px;'>Past Analyses</h3>", unsafe_allow_html=True)

    try:
        history = requests.get(f"{API_URL}/history").json()
        
        # Serialize history safely
        history_json = json.dumps(history)
        
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
            body {{
                margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; color: #f8fafc;
            }}
            /* Controls */
            .controls {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
            .search-box {{ position: relative; width: 200px; }}
            .search-box input {{
                width: 100%; box-sizing: border-box; background: #0a1120; border: 1px solid #1e2d40; border-radius: 8px;
                padding: 8px 12px 8px 32px; color: #f8fafc; font-size: 13px; outline: none; transition: all 0.2s;
            }}
            .search-box input:focus {{ border-color: #2dd4bf; box-shadow: 0 0 0 2px rgba(45,212,191,0.2); }}
            .search-icon {{ position: absolute; left: 10px; top: 9px; color: #64748b; }}
            .filters {{ display: flex; gap: 8px; }}
            .filter-pill {{
                background: #0a1120; border: 1px solid #1e2d40; color: #94a3b8; padding: 6px 12px;
                border-radius: 16px; font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.2s;
            }}
            .filter-pill.active {{ background: #2dd4bf; border-color: #2dd4bf; color: #000; font-weight: 600; }}
            .export-btn {{
                background: transparent; border: 1px solid #334155; color: #f8fafc; padding: 6px 12px;
                border-radius: 8px; font-size: 12px; font-weight: 500; cursor: pointer; transition: background 0.2s;
            }}
            .export-btn:hover {{ background: rgba(255,255,255,0.05); }}
            
            /* Table */
            table {{ width: 100%; border-collapse: separate; border-spacing: 0 6px; }}
            th {{
                background: #0a1120; position: sticky; top: 0; font-size: 11px; font-weight: 600; color: #64748b;
                text-transform: uppercase; letter-spacing: 0.08em; padding: 12px 16px; text-align: left; z-index: 10;
            }}
            .row {{ background: #0e1420; border-radius: 8px; transition: all 0.2s; outline: 1px solid #1a2640; }}
            .row:hover {{ background: #121e32; outline-color: #2dd4bf; }}
            td {{ padding: 14px 16px; font-size: 13px; color: #f8fafc; border-top: 1px solid transparent; border-bottom: 1px solid transparent; }}
            .row td:first-child {{ border-left: 3px solid transparent; border-radius: 8px 0 0 8px; }}
            .row:hover td:first-child {{ border-left: 3px solid #2dd4bf; }}
            .row td:last-child {{ border-right: 1px solid transparent; border-radius: 0 8px 8px 0; }}
            
            /* Verdict Pills */
            .pill {{
                display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 12px;
                font-size: 11px; font-weight: 600; text-transform: capitalize;
            }}
            .dot {{ width: 6px; height: 6px; border-radius: 50%; }}
            
            /* Confidence */
            .conf-wrap {{ display: flex; align-items: center; gap: 8px; }}
            .prog-bg {{ width: 80px; height: 6px; background: #1e2d40; border-radius: 3px; }}
            .prog-fill {{ height: 100%; border-radius: 3px; }}
            .conf-val {{ font-weight: 600; width: 35px; text-align: right; }}
            
            /* Actions */
            .actions {{ opacity: 0; transition: opacity 0.2s; display: flex; gap: 8px; justify-content: center; }}
            .row:hover .actions {{ opacity: 1; }}
            .act-btn {{ background: transparent; border: none; cursor: pointer; color: #64748b; padding: 4px; border-radius: 4px; }}
            .act-btn:hover {{ color: #f8fafc; background: rgba(255,255,255,0.1); }}
            
            /* Tooltip */
            .tooltip-container {{ position: relative; cursor: pointer; }}
            .tooltip-text {{
                visibility: hidden; background-color: #1e2d40; color: #fff; text-align: left; border-radius: 6px; border: 1px solid #334155;
                padding: 12px; position: absolute; z-index: 100; bottom: 120%; left: 0;
                opacity: 0; transition: opacity 0.2s; font-size: 12px; width: max-content; max-width: 300px;
                white-space: normal; line-height: 1.5; box-shadow: 0 10px 25px rgba(0,0,0,0.5); pointer-events: none;
            }}
            .tooltip-container:hover .tooltip-text {{ visibility: visible; opacity: 1; }}
            
            /* Empty & Paginator */
            .empty-state {{ display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px; text-align: center; }}
            .paginator {{ display: flex; justify-content: center; gap: 8px; margin-top: 20px; font-size: 13px; color: #94a3b8; align-items: center; }}
            .page-btn {{ cursor: pointer; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 6px; transition: background 0.2s; }}
            .page-btn:hover {{ background: rgba(255,255,255,0.05); color: #fff; }}
            .page-btn.active {{ background: #2dd4bf; color: #000; font-weight: 600; }}
            .nav-btn {{ cursor: pointer; transition: color 0.2s; }}
            .nav-btn:hover {{ color: #fff; }}
            
            .muted {{ color: #94a3b8; }}
        </style>
        </head>
        <body>
            <div class="controls">
                <div class="search-box">
                    <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                    <input type="text" placeholder="Search applications...">
                </div>
                <div class="filters">
                    <div class="filter-pill active">All</div>
                    <div class="filter-pill">Genuine</div>
                    <div class="filter-pill">Suspicious</div>
                    <div class="filter-pill">Emotional</div>
                </div>
                <button class="export-btn">↓ Export CSV</button>
            </div>
            
            <div style="font-size:12px; color:#94a3b8; margin-bottom:12px;">Showing <span id="count">0</span> results</div>
            
            <div id="table-container"></div>
            
            <script>
                const rawData = {history_json};
                const container = document.getElementById("table-container");
                const countEl = document.getElementById("count");
                
                function formatDate(isoStr) {{
                    try {{
                        const d = new Date(isoStr);
                        if(isNaN(d)) return `<span class="muted">${{isoStr.split('T')[0]}}</span>`;
                        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                        const day = String(d.getDate()).padStart(2, '0');
                        const hrs = String(d.getHours()).padStart(2, '0');
                        const mins = String(d.getMinutes()).padStart(2, '0');
                        return `<span class="muted">${{months[d.getMonth()]}} ${{day}} ·</span> ${{hrs}}:${{mins}}`;
                    }} catch(e) {{ return `<span class="muted">${{isoStr}}</span>`; }}
                }}
                
                function getCfg(pred) {{
                    if(pred === 'Genuine') return {{ bg: '#0d3d2e', c: '#2dd4bf' }};
                    if(pred === 'Suspicious') return {{ bg: '#3d2a0d', c: '#f59e0b' }};
                    if(pred === 'Emotional') return {{ bg: '#2d1054', c: '#a78bfa' }};
                    return {{ bg: '#333', c: '#fff' }};
                }}
                
                function renderTable(data) {{
                    countEl.innerText = data.length;
                    if(data.length === 0) {{
                        container.innerHTML = `
                        <div class="empty-state">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1e2d40" stroke-width="1.5" style="margin-bottom:16px;">
                                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                                <circle cx="12" cy="14" r="3"></circle>
                                <path d="M14.5 16.5L17 19"></path>
                            </svg>
                            <div style="font-weight:600; color:#f8fafc; font-size:15px; margin-bottom:4px;">No analyses found</div>
                            <div class="muted" style="font-size:13px;">Try a different filter or analyze your first application</div>
                        </div>`;
                        return;
                    }}
                    
                    let html = `<table><tr>
                        <th style="width:40px;">#</th>
                        <th style="width:120px;">Time</th>
                        <th>Leave Application</th>
                        <th style="width:130px;">Verdict</th>
                        <th style="width:140px;">Confidence</th>
                        <th style="width:80px; text-align:center;">Actions</th>
                    </tr>`;
                    
                    data.forEach((item, idx) => {{
                        const timeStr = formatDate(item.created_at);
                        const txt = item.text;
                        const trunc = txt.length > 55 ? txt.substring(0, 55) + "..." : txt;
                        const safeTxt = txt.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        const cfg = getCfg(item.prediction);
                        const conf = (item.confidence * 100).toFixed(1);
                        
                        html += `
                        <tr class="row">
                            <td class="muted">${{idx + 1}}</td>
                            <td>${{timeStr}}</td>
                            <td>
                                <div class="tooltip-container">
                                    ${{trunc.replace(/</g, "&lt;").replace(/>/g, "&gt;")}}
                                    <div class="tooltip-text">${{safeTxt}}</div>
                                </div>
                            </td>
                            <td>
                                <div class="pill" style="background:${{cfg.bg}}; color:${{cfg.c}};">
                                    <div class="dot" style="background:${{cfg.c}};"></div>
                                    ${{item.prediction}}
                                </div>
                            </td>
                            <td>
                                <div class="conf-wrap">
                                    <div class="prog-bg"><div class="prog-fill" style="width:${{conf}}%; background:${{cfg.c}};"></div></div>
                                    <div class="conf-val">${{conf}}%</div>
                                </div>
                            </td>
                            <td>
                                <div class="actions">
                                    <button class="act-btn" title="View"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button>
                                    <button class="act-btn" title="Delete"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
                                </div>
                            </td>
                        </tr>`;
                    }});
                    
                    html += `</table>
                    <div class="paginator">
                        <span class="nav-btn">← Prev</span>
                        <div class="page-btn active">1</div>
                        <div class="page-btn">2</div>
                        <div class="page-btn">3</div>
                        <span class="nav-btn">Next →</span>
                    </div>`;
                    
                    container.innerHTML = html;
                }}
                
                // Init render
                renderTable(rawData);
            </script>
        </body>
        </html>
        """
        
        components.html(html_code, height=650, scrolling=True)
        
    except Exception as e:
        st.error(f"Could not fetch history: {e}")

with t_dash:
    tot = stats_res.get("total", 0)
    g = stats_res.get("genuine", 0)
    s = stats_res.get("suspicious", 0)
    e = stats_res.get("emotional", 0)
    
    st.markdown("""
    <style>
    .dash-card {
        background: #0a1120;
        border: 1px solid #1e2d40;
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .dash-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    def stat_card(title, value, color, icon_svg, trend):
        return f"""
        <div class="dash-card" style="border-top:3px solid {color};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                <div style="width:32px; height:32px; border-radius:8px; background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center;">
                    {icon_svg}
                </div>
                <div style="font-size:11px; font-weight:600; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px;">{title}</div>
            </div>
            <div style="font-size:32px; font-weight:600; color:#f8fafc; margin-bottom:8px;">{value}</div>
            <div style="font-size:11px; color:{color};"><span style="font-weight:600;">{trend}</span></div>
        </div>
        """

    svg_tot = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
    svg_gen = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
    svg_sus = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
    svg_emo = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'

    c1.markdown(stat_card("Total Scans", tot, "#38bdf8", svg_tot, "↑ 12% this week"), unsafe_allow_html=True)
    c2.markdown(stat_card("Genuine", f"{round((g/tot)*100,1)}%" if tot else "0%", "#2dd4bf", svg_gen, "↑ 5% this week"), unsafe_allow_html=True)
    c3.markdown(stat_card("Suspicious", f"{round((s/tot)*100,1)}%" if tot else "0%", "#f59e0b", svg_sus, "↓ 2% this week"), unsafe_allow_html=True)
    c4.markdown(stat_card("Emotional", f"{round((e/tot)*100,1)}%" if tot else "0%", "#a78bfa", svg_emo, "↑ 8% this week"), unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:30px; margin-bottom:16px;">
        <div style="font-size:16px; font-weight:600; color:#fff;">Distribution by Category</div>
        <div style="background:#0a1120; border:1px solid #1e2d40; border-radius:16px; padding:4px 12px; font-size:12px; color:#94a3b8; cursor:pointer;">All Time ▾</div>
    </div>
    """, unsafe_allow_html=True)

    c_bar, c_donut = st.columns([1.5, 1], gap="large")

    with c_bar:
        if tot > 0:
            fig_bar = go.Figure(data=[go.Bar(
                x=['Genuine', 'Suspicious', 'Emotional'], 
                y=[g, s, e],
                marker=dict(color=['#2dd4bf', '#f59e0b', '#a78bfa'], cornerradius=8),
                hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
            )])
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(14,20,32,1)',
                font=dict(color="#f8fafc", family="Inter"),
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(gridcolor="#1e2d40", zeroline=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data available")

    with c_donut:
        if tot > 0:
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Genuine', 'Suspicious', 'Emotional'], 
                values=[g, s, e],
                hole=0.6,
                marker=dict(colors=['#2dd4bf', '#f59e0b', '#a78bfa']),
                textinfo='percent'
            )])
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#f8fafc", family="Inter"),
                margin=dict(l=0, r=0, t=20, b=20),
                height=300,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data available")

    # RECENT ACTIVITY
    st.markdown("<div style='margin-top:30px; font-size:16px; font-weight:600; color:#fff; margin-bottom:16px;'>Recent Activity</div>", unsafe_allow_html=True)
    try:
        history = requests.get(f"{API_URL}/history").json()
        if history:
            for item in history[:3]:
                cfg = {
                    "Genuine": {"color": "#2dd4bf", "bg": "rgba(45,212,191,0.1)"},
                    "Suspicious": {"color": "#f59e0b", "bg": "rgba(245,158,11,0.1)"},
                    "Emotional": {"color": "#a78bfa", "bg": "rgba(167,139,250,0.1)"}
                }.get(item['prediction'], {"color":"#fff", "bg":"#000"})
                
                txt = item['text'][:80] + "..." if len(item['text']) > 80 else item['text']
                
                st.markdown(f"""
                <div class="dash-card" style="padding:16px; margin-bottom:12px; display:flex; align-items:center; justify-content:space-between; border-radius:8px;">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <div style="background:{cfg['bg']}; color:{cfg['color']}; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600; text-transform:uppercase; min-width:85px; text-align:center;">
                            {item['prediction']}
                        </div>
                        <div style="font-size:13px; color:#f8fafc;">"{txt}"</div>
                    </div>
                    <div style="font-size:12px; color:#64748b; white-space:nowrap;">Just now</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#94a3b8; font-size:13px;'>No recent activity.</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div style='color:#ef4444; font-size:13px;'>Could not fetch history.</div>", unsafe_allow_html=True)
