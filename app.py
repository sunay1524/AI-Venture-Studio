import streamlit as st
import json
import os
from datetime import date
from venture_studio import run_agent

# --------------------------------------------------
# RATE LIMITING
# --------------------------------------------------

DAILY_LIMIT = 10  # max free analyses per day
USAGE_FILE = os.path.join(os.path.dirname(__file__), "usage.json")

def _load_usage() -> dict:
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_usage(data: dict):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def get_daily_count() -> int:
    data = _load_usage()
    today = str(date.today())
    return data.get(today, 0)

def increment_daily_count():
    data = _load_usage()
    today = str(date.today())
    data[today] = data.get(today, 0) + 1
    _save_usage(data)

def is_rate_limited() -> bool:
    return get_daily_count() >= DAILY_LIMIT

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Venture Studio",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "startup_idea" not in st.session_state:
    st.session_state["startup_idea"] = ""

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    max-width:1400px;
}

.stButton>button{
    width:100%;
    height:3.2rem;
    font-size:16px;
    font-weight:bold;
    border-radius:12px;
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    color: white !important;
    border: none !important;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.stButton>button:hover{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.5);
    background: linear-gradient(135deg, #4338CA 0%, #6D28D9 100%) !important;
}

div[data-testid="stMetricValue"] {
    font-size: 24px;
    font-weight: bold;
    color: #6366F1;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🚀 AI Venture Studio")
    st.caption("Multi-Agent Startup Consultant")
    st.markdown("---")

    # ---- BYOK Section ----
    st.subheader("🔑 Your API Keys (Optional)")
    st.caption(
        "Enter your own keys to bypass the daily limit. "
        "Keys are **never stored** — used only for your session."
    )

    user_gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get a free key at https://aistudio.google.com/app/apikey"
    )
    user_tavily_key = st.text_input(
        "Tavily API Key",
        type="password",
        placeholder="tvly-...",
        help="Get a free key at https://app.tavily.com/"
    )

    using_own_keys = bool(user_gemini_key and user_tavily_key)

    if using_own_keys:
        st.success("✅ Using your own keys — no rate limit!")
    else:
        remaining = max(0, DAILY_LIMIT - get_daily_count())
        if remaining > 0:
            st.info(f"🎁 **{remaining}/{DAILY_LIMIT}** free analyses left today.")
        else:
            st.error("⛔ Daily free limit reached. Add your own API keys above to continue.")

    st.markdown("---")

    st.subheader("💡 Sample Ideas")
    templates = {
        "🧠 AI Interview Coach": "Build an AI platform that helps students prepare for interviews by conducting mock interviews, analyzing their voice and body language, and providing real-time constructive feedback.",
        "🚜 Smart Farming IoT": "An IoT and AI platform for precision agriculture that monitors soil moisture, temperature, and crop health using sensors, recommending optimal watering and fertilizer schedules to farmers.",
        "⚖️ AI Legal Auditor": "A SaaS application that uses LLMs to automatically audit contracts, lease agreements, and terms of service, highlighting risky clauses and suggesting edits."
    }
    for name, desc in templates.items():
        if st.button(name, use_container_width=True):
            st.session_state["startup_idea"] = desc
            st.rerun()

    st.markdown("---")
    st.info("💡 **How it works:**\nThis system orchestrates 8 AI agents using LangGraph & Gemini to research, design, and assess the feasibility of your business idea.")

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚀 AI Venture Studio")

st.caption(
    "Multi-Agent Startup Consultant powered by LangGraph + Gemini"
)

# --------------------------------------------------
# INPUT
# --------------------------------------------------

idea = st.text_area(
    "💡 Describe your Startup Idea",
    value=st.session_state["startup_idea"],
    height=200,
    placeholder="Select a sample idea from the sidebar or enter your own..."
)

# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def display_model(model):
    """
    Beautifully display any Pydantic model.
    """
    for key, value in model.model_dump().items():
        title = key.replace("_", " ").title()
        
        with st.container(border=True):
            st.markdown(f"##### 🔹 {title}")
            if isinstance(value, bool):
                if value:
                    st.markdown("<span style='color:#10B981; font-weight:bold; font-size:18px;'>✅ Yes</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:#EF4444; font-weight:bold; font-size:18px;'>❌ No</span>", unsafe_allow_html=True)
            else:
                st.markdown(value)

def generate_markdown_report(idea, final_state):
    report = f"""# 🚀 AI Venture Studio Startup Report

## 💡 Startup Idea
{idea}

---

## 📈 Market Research
"""
    mr = final_state.get("market_research_output")
    if mr:
        report += f"### Market Size\n{mr.market_size}\n\n### Growth Potential\n{mr.growth_potential}\n\n### Competitive Landscape\n{mr.competitive_landscape}\n\n### Key Insights\n{mr.key_insights}\n\n"

    report += "---\n\n## 🏢 Competitor Analysis\n"
    ca = final_state.get("competitor_analysis_output")
    if ca:
        report += f"### Competitor Strengths\n{ca.competitor_strengths}\n\n### Competitor Weaknesses\n{ca.competitor_weaknesses}\n\n### Competitor Strategies\n{ca.competitor_strategies}\n\n### Key Insights\n{ca.key_insights}\n\n"

    report += "---\n\n## 👥 Customer Research\n"
    cr = final_state.get("customer_research_output")
    if cr:
        report += f"### Customer Personas\n{cr.customer_personas}\n\n### Pain Points\n{cr.pain_points}\n\n### Feature Requests\n{cr.feature_requests}\n\n### Buying Motivation\n{cr.buying_motivation}\n\n### Objections\n{cr.objections}\n\n### Summary\n{cr.summary}\n\n"

    report += "---\n\n## 💼 Business Model\n"
    bm = final_state.get("buisness_model_output")
    if bm:
        report += f"### Value Proposition\n{bm.value_proposition}\n\n### Revenue Model\n{bm.revenue_model}\n\n### Cost Structure\n{bm.cost_structure}\n\n### Key Partners\n{bm.key_partners}\n\n### Key Activities\n{bm.key_activities}\n\n### Key Resources\n{bm.key_resources}\n\n### Key Insights\n{bm.key_insights}\n\n"

    report += "---\n\n## 🏗 Technical Architecture\n"
    ta = final_state.get("technical_architecture_output")
    if ta:
        report += f"### Feasibility\n{'✅ Feasible' if ta.feasibility else '❌ Not Feasible'}\n\n### Architecture Diagram Description\n{ta.architecture_diagram}\n\n### Technology Stack\n{ta.technology_stack}\n\n### Key Insights\n{ta.key_insights}\n\n"

    report += "---\n\n## ⚠ Risk Analysis\n"
    ra = final_state.get("risk_analysis_output")
    if ra:
        report += f"### Risk Acceptance\n{'✅ Acceptable' if ra.risk_acceptance else '⚠ High'}\n\n### Risk Identification\n{ra.risk_identification}\n\n### Risk Assessment\n{ra.risk_assessment}\n\n### Risk Mitigation\n{ra.risk_mitigation}\n\n### Key Insights\n{ra.key_insights}\n\n"

    report += "---\n\n## 🎤 Pitch Deck\n"
    pd = final_state.get("pitch_deck_output")
    if pd:
        report += f"### Pitch Deck Outline\n{pd.pitch_deck}\n\n### Key Insights\n{pd.key_insights}\n\n"

    return report

# --------------------------------------------------
# BUTTON
# --------------------------------------------------

if st.button("🚀 Analyze Startup Idea", use_container_width=True):

    if idea.strip() == "":
        st.warning("Please enter a startup idea.")
        st.stop()

    # ---------- Rate limit check ----------
    if not using_own_keys and is_rate_limited():
        st.error(
            "⛔ **Daily free limit reached** for today.\n\n"
            "To continue, add your own **Gemini** and **Tavily** API keys in the sidebar.\n\n"
            "- 🔑 [Get Gemini key (free)](https://aistudio.google.com/app/apikey)\n"
            "- 🔑 [Get Tavily key (free)](https://app.tavily.com/)"
        )
        st.stop()

    # Increment counter only for users on the shared key
    if not using_own_keys:
        increment_daily_count()

    left, right = st.columns([1,3])

    # --------------------------------------------------

    with left:

        st.subheader("Workflow")

        workflow = st.empty()

        progress = st.progress(0)

    # --------------------------------------------------

    with right:

        status = st.empty()

    # --------------------------------------------------

    completed = []

    final_state = {}

    node_names = {

        "venture_manager":"🚀 Venture Manager",

        "market_research":"📈 Market Research",

        "competitor_analysis":"🏢 Competitor Analysis",

        "customer_research":"👥 Customer Research",

        "Business_model":"💼 Business Model",

        "technical_architecture":"🏗 Technical Review",

        "risk_analysis":"⚠ Risk Analysis",

        "pitch_deck":"🎤 Pitch Deck"

    }

    total_nodes = len(node_names)

    # --------------------------------------------------
    # STREAM EVENTS
    # --------------------------------------------------

    for event in run_agent(
        idea,
        gemini_api_key=user_gemini_key if using_own_keys else None,
        tavily_api_key=user_tavily_key if using_own_keys else None
    ):

        node = list(event.keys())[0]

        completed.append(node)

        final_state.update(event[node])

        progress.progress(

            min(len(completed)/total_nodes,1.0)
        )

        text = ""

        for key in node_names:

            if key in completed:

                text += f"✅ {node_names[key]}\n\n"

            else:

                text += f"⏳ {node_names[key]}\n\n"

        workflow.markdown(text)

        status.info(f"Running: **{node_names[node]}**")

    progress.progress(1.0)

    status.success("🎉 Analysis Completed!")

    st.divider()

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    col1,col2,col3 = st.columns(3)

    with col1:

        tech = final_state["technical_architecture_output"]

        if tech.feasibility:

            st.metric("Technical Feasibility","✅ Feasible")

        else:

            st.metric("Technical Feasibility","❌ Not Feasible")

    with col2:

        risk = final_state["risk_analysis_output"]

        if risk.risk_acceptance:

            st.metric("Risk","✅ Acceptable")

        else:

            st.metric("Risk","⚠ High")

    with col3:

        st.metric(

            "Agents Completed",
            f"{len(completed)}/{total_nodes}"
        )

    st.divider()

    # --------------------------------------------------
    # EXPORT REPORT
    # --------------------------------------------------

    markdown_report = generate_markdown_report(idea, final_state)
    st.download_button(
        label="📥 Download Full Report (Markdown)",
        data=markdown_report,
        file_name="startup_analysis_report.md",
        mime="text/markdown",
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # TABS
    # --------------------------------------------------

    tabs = st.tabs([

        "📈 Market",

        "🏢 Competitors",

        "👥 Customers",

        "💼 Business",

        "🏗 Technical",

        "⚠ Risk",

        "🎤 Pitch Deck"

    ])

    with tabs[0]:

        display_model(final_state["market_research_output"])

    with tabs[1]:

        display_model(final_state["competitor_analysis_output"])

    with tabs[2]:

        display_model(final_state["customer_research_output"])

    with tabs[3]:

        display_model(final_state["buisness_model_output"])

    with tabs[4]:

        display_model(final_state["technical_architecture_output"])

    with tabs[5]:

        display_model(final_state["risk_analysis_output"])

    with tabs[6]:

        display_model(final_state["pitch_deck_output"])