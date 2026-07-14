import streamlit as st
from venture_studio import run_agent

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Venture Studio",
    page_icon="🚀",
    layout="wide"
)

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
    font-size:18px;
    font-weight:bold;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

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
    height=220,
    placeholder="Example:\nBuild an AI platform that helps students prepare for interviews..."
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

        st.subheader(title)

        if isinstance(value, bool):

            if value:
                st.success("✅ Yes")

            else:
                st.error("❌ No")

        else:

            st.write(value)

        st.divider()

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

if st.button("🚀 Analyze Startup", use_container_width=True):

    if idea.strip() == "":
        st.warning("Please enter a startup idea.")
        st.stop()

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

    for event in run_agent(idea):

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