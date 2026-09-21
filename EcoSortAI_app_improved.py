import streamlit as st

from agent import run_ecosort
from llm import analyze_image


st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# -----------------------------
# UI helpers
# -----------------------------
CATEGORY_META = {
    "Plastic": ("🟢", "Plastic"),
    "Paper / Cardboard": ("🔵", "Paper / Cardboard"),
    "Glass": ("🟣", "Glass"),
    "Metal": ("🟠", "Metal"),
    "Batteries": ("🔴", "Batteries"),
    "E-Waste": ("🟦", "E-Waste"),
    "Organic / Food Waste": ("🟤", "Organic / Food Waste"),
    "Sanitary / Hygiene Waste": ("🟡", "Sanitary / Hygiene Waste"),
    "Hazardous / Chemical Waste": ("⚠️", "Hazardous / Chemical Waste"),
    "Mixed / Unknown": ("⚪", "Mixed / Unknown"),
}

EXAMPLES = [
    "Empty plastic water bottle",
    "Used lithium battery from a power bank",
    "Banana peel",
]


@st.cache_data(show_spinner=False)
def _category_meta(category: str):
    return CATEGORY_META.get(category, ("♻️", category or "Unknown"))


def set_example(example: str):
    st.session_state["item_description"] = example
    st.session_state["analysis_result"] = None
    st.session_state["image_description"] = ""


def clear_analysis():
    st.session_state["analysis_result"] = None
    st.session_state["image_description"] = ""


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .block-container {
            max-width: 980px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .ecosort-hero {
            padding: 1.15rem 1.35rem 1.05rem 1.35rem;
            border: 1px solid rgba(46, 125, 50, 0.16);
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(46,125,50,0.08), rgba(255,255,255,0.98));
            margin-bottom: 1.1rem;
        }

        .ecosort-title {
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 0;
        }

        .ecosort-subtitle {
            margin-top: 0.35rem;
            color: #5d6b61;
            font-size: 0.98rem;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.8rem;
        }

        .pill {
            display: inline-block;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            background: rgba(46,125,50,0.09);
            border: 1px solid rgba(46,125,50,0.14);
            font-size: 0.78rem;
            font-weight: 650;
            color: #2f6b36;
        }

        .section-title {
            font-size: 1.12rem;
            font-weight: 750;
            margin: 0.55rem 0 0.35rem 0;
        }

        .result-card {
            padding: 1.05rem 1.15rem;
            border-radius: 18px;
            border: 1px solid rgba(0,0,0,0.08);
            background: rgba(255,255,255,0.98);
            box-shadow: 0 8px 24px rgba(0,0,0,0.035);
            margin: 0.65rem 0;
        }

        .category-badge {
            display: inline-block;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            background: rgba(46,125,50,0.10);
            color: #27652d;
            font-weight: 800;
            font-size: 0.9rem;
        }

        .muted {
            color: #6b756e;
            font-size: 0.82rem;
        }

        .footer-note {
            text-align: center;
            color: #737b76;
            font-size: 0.78rem;
            padding-top: 1.1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Session state
# -----------------------------
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "image_description" not in st.session_state:
    st.session_state["image_description"] = ""


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="ecosort-hero">
        <div class="ecosort-title">♻️ EcoSort AI <span style="float:right; font-size:0.82rem; font-weight:700; color:#3d7443;">🌱 SDG 12 • SDG 11</span></div>
        <div class="ecosort-subtitle">Intelligent Waste Segregation &amp; Responsible Disposal Assistant</div>
        <div class="pill-row">
            <span class="pill">IBM watsonx.ai</span>
            <span class="pill">Agentic AI</span>
            <span class="pill">RAG</span>
            <span class="pill">Multimodal</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "♻️ Describe a waste item or upload an image. EcoSort AI combines AI classification "
    "with retrieved waste guidance. Local disposal rules can vary, so verify with the "
    "appropriate local authority or authorized collection service.",
)


# -----------------------------
# Example inputs
# -----------------------------
st.markdown('<div class="section-title">Try an example</div>', unsafe_allow_html=True)
example_cols = st.columns(3, gap="small")
for index, example in enumerate(EXAMPLES):
    with example_cols[index]:
        st.button(
            example,
            use_container_width=True,
            on_click=set_example,
            args=(example,),
            key=f"example_{index}",
        )


# -----------------------------
# Input area
# -----------------------------
st.markdown('<div class="section-title">What do you want to identify?</div>', unsafe_allow_html=True)

item_description = st.text_area(
    "",
    placeholder="Example: Used AA battery from a TV remote",
    height=110,
    key="item_description",
    label_visibility="collapsed",
)

col_left, col_right = st.columns([1.25, 1], gap="large")

with col_left:
    st.markdown("**📷 Upload a waste image**")
    uploaded_image = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        help="Upload a clear photo of the waste item.",
    )
    if uploaded_image:
        st.image(uploaded_image, caption="Image ready for analysis", use_container_width=True)

with col_right:
    st.markdown("**📍 Location**")
    location = st.text_input(
        "",
        placeholder="Example: Kolkata, West Bengal, India",
        key="location",
        label_visibility="collapsed",
    )

    st.markdown("**🧭 Analysis mode**")
    if uploaded_image and item_description.strip():
        st.caption("Using both your description and image")
    elif uploaded_image:
        st.caption("Using image-based analysis")
    else:
        st.caption("Using text-based analysis")


# -----------------------------
# Actions
# -----------------------------
action_col1, action_col2 = st.columns([3, 1], gap="small")
with action_col1:
    analyze_clicked = st.button("♻️ Analyze Waste", type="primary", use_container_width=True)
with action_col2:
    reset_clicked = st.button("↺ New", use_container_width=True)

if reset_clicked:
    clear_analysis()
    st.rerun()


# -----------------------------
# Analysis pipeline
# -----------------------------
if analyze_clicked:
    if not item_description.strip() and not uploaded_image:
        st.error("Please describe the waste item or upload an image.")
        st.stop()

    image_description = ""

    if uploaded_image:
        with st.status("🔎 Analyzing image...", expanded=False) as status:
            try:
                image_description = analyze_image(
                    uploaded_image.getvalue(),
                    uploaded_image.type,
                )
                status.update(label="✅ Image analysis complete", state="complete")
            except Exception as error:
                status.update(label="❌ Image analysis failed", state="error")
                st.error("Image analysis could not be completed.")
                st.exception(error)
                st.stop()

    with st.status("🤖 Running EcoSort AI...", expanded=False) as status:
        try:
            result = run_ecosort(
                item_input=item_description,
                image_description=image_description,
                location=location,
            )
            status.update(label="✅ EcoSort analysis complete", state="complete")
        except Exception as error:
            status.update(label="❌ EcoSort analysis failed", state="error")
            st.error("EcoSort AI could not complete the analysis.")
            st.exception(error)
            st.stop()

    st.session_state["analysis_result"] = result
    st.session_state["image_description"] = image_description


# -----------------------------
# Results
# -----------------------------
result = st.session_state.get("analysis_result")

if result:
    st.divider()
    st.markdown('<div class="section-title">AI Result</div>', unsafe_allow_html=True)

    category = result.get("category", "Mixed / Unknown")
    icon, category_label = _category_meta(category)
    item_name = result.get("item_name", "Unknown")
    uncertainty = bool(result.get("uncertainty", False))
    guidance = result.get("retrieved_guidance", []) or []

    if guidance:
        top_score = max(float(item.get("score", 0.0)) for item in guidance)
    else:
        top_score = 0.0

    metric1, metric2, metric3 = st.columns(3, gap="small")
    with metric1:
        st.metric("Detected item", item_name)
    with metric2:
        st.metric("Waste category", f"{icon} {category_label}")
    with metric3:
        st.metric("RAG knowledge match", f"{top_score:.2f}")

    if uncertainty:
        st.warning("⚠️ The system marked this classification as uncertain. It is intentionally avoiding an unsupported disposal instruction.")
    else:
        st.success("✅ The item was classified with sufficient evidence for a practical recommendation.")

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("### ✅ What to do")
    st.markdown(result.get("final_answer", "No recommendation was generated."))
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🔍 Why did EcoSort AI classify it this way?", expanded=False):
        st.write(result.get("classification_reason", "No classification explanation was returned."))

    image_description = st.session_state.get("image_description", "")
    if image_description:
        with st.expander("📷 Image understanding result", expanded=False):
            st.write(image_description)

    with st.expander(f"📚 Knowledge used ({len(guidance)} retrieved records)", expanded=False):
        if guidance:
            for index, item in enumerate(guidance, start=1):
                st.markdown(f"**Record {index}**")
                st.markdown(item.get("text", ""))
                st.caption(f"RAG similarity: {float(item.get('score', 0.0)):.3f}")
                if index != len(guidance):
                    st.divider()
        else:
            st.caption("No retrieved guidance records were returned.")

    with st.expander("⚙️ How EcoSort AI works", expanded=False):
        st.markdown(
            """
            **1. Input** → text description and/or waste image  
            **2. AI understanding** → text and image-capable foundation models  
            **3. Agent workflow** → classification and decision logic  
            **4. RAG** → relevant waste-management guidance is retrieved  
            **5. Recommendation** → practical handling and disposal guidance is generated  
            """
        )


st.markdown(
    '<div class="footer-note">EcoSort AI is a sustainability decision-support prototype. '
    'Always verify current local waste-management requirements before disposal.</div>',
    unsafe_allow_html=True,
)
