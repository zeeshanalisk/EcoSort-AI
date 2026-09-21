import streamlit as st

from agent import run_ecosort
from llm import analyze_image


st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="centered",
)

st.title("♻️ EcoSort AI")
st.subheader("Agentic AI Assistant for Intelligent Waste Segregation and Responsible Disposal")

st.write(
    "Describe a waste item or upload an image. EcoSort AI will classify it, "
    "retrieve relevant guidance, and generate a practical handling recommendation."
)

st.info(
    "Waste-management requirements can vary by location. Verify local authority "
    "or authorized collection guidance before acting on disposal information."
)

location = st.text_input(
    "Your location (optional)",
    placeholder="Example: Kolkata, West Bengal, India",
)

item_description = st.text_area(
    "Describe the waste item",
    placeholder="Example: Used AA battery from a TV remote",
)

uploaded_image = st.file_uploader(
    "Or upload an image of the waste item",
    type=["jpg", "jpeg", "png"],
)


if st.button("Analyze Waste", type="primary"):
    if not item_description.strip() and not uploaded_image:
        st.error("Please describe the waste item or upload an image.")
        st.stop()

    image_description = ""

    if uploaded_image:
        with st.spinner("Analyzing the image..."):
            try:
                image_description = analyze_image(
                    uploaded_image.getvalue(),
                    uploaded_image.type,
                )
            except Exception:
                st.error("Image analysis failed. Check model availability and credentials.")
                st.stop()

        with st.expander("Image analysis result"):
            st.write(image_description)

    with st.spinner("Analyzing the waste item..."):
        try:
            result = run_ecosort(
                item_input=item_description,
                image_description=image_description,
                location=location,
            )
        except Exception as error:
            st.error("EcoSort AI could not complete the analysis.")
            st.exception(error)
            st.stop()

    st.success("Waste analysis completed.")
    st.markdown("## EcoSort AI Recommendation")
    st.markdown(result.get("final_answer", "No recommendation was generated."))

    st.markdown("## AI Classification")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Detected item**")
        st.write(result.get("item_name", "Unknown"))

    with col2:
        st.write("**Waste category**")
        st.write(result.get("category", "Mixed / Unknown"))

    st.markdown("## Retrieved Guidance")
    with st.expander("Show retrieved context"):
        for item in result.get("retrieved_guidance", []):
            st.markdown(item["text"])
            st.caption(f"Retrieval similarity: {item['score']:.3f}")
            st.divider()

st.caption(
    "Prototype for sustainability education and decision support. Local waste rules may differ."
)
