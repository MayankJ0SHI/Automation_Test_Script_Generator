import streamlit as st
import os
from app.components import (
    read_codebase_files,
    embed_and_store,
    search_code,
    generate_java_code
)

STATIC_CODEBASE_PATH = ""  # Update this path as needed

st.set_page_config(page_title="Test Step to Java Code Generator", layout="centered")
st.title("🧪 Test Step to Java Code Generator")

# --- Step input mode ---
st.markdown("### ✍️ How would you like to provide the test steps?")
input_mode = st.radio(
    "Choose input method:",
    options=["Enter Manually", "Paste All Steps", "Upload File"]
)

test_steps = []

if input_mode == "Enter Manually":
    if "test_steps" not in st.session_state:
        st.session_state.test_steps = [""]
    for i, step in enumerate(st.session_state.test_steps):
        st.session_state.test_steps[i] = st.text_input(f"Test Step {i + 1}", value=step, key=f"step_{i}")
    if st.button("➕ Add Step"):
        st.session_state.test_steps.append("")
        st.rerun()
    test_steps = st.session_state.test_steps

elif input_mode == "Paste All Steps":
    pasted_steps = st.text_area("Paste all test steps (one per line):")
    if pasted_steps:
        test_steps = pasted_steps.strip().splitlines()

elif input_mode == "Upload File":
    uploaded_file = st.file_uploader("Upload a .txt file with test steps:", type=["txt"])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        test_steps = file_content.strip().splitlines()
        st.success("✅ File uploaded and test steps extracted!")

# Display parsed test steps
if test_steps and any(s.strip() for s in test_steps):
    st.markdown("### ✅ Current Test Steps:")
    for i, step in enumerate(test_steps):
        st.markdown(f"{i+1}. {step}")

# --- Run code generation directly ---
if st.button("🚀 Generate Java Code"):
    if not any(s.strip() for s in test_steps):
        st.error("Please enter at least one valid test step.")
    elif not os.path.isdir(STATIC_CODEBASE_PATH):
        st.error(f"Static codebase path is invalid: {STATIC_CODEBASE_PATH}")
    else:
        try:
            st.info("⏳ Processing...")

            # 1. Prepare test step string
            test_steps_str = "\n".join([s.strip() for s in test_steps if s.strip()])

            # 2. Read codebase files
            files = read_codebase_files(STATIC_CODEBASE_PATH)

            # 3. Embed and store in ChromaDB (or whatever backing you're using)
            embed_and_store(files)

            # 4. Perform semantic search
            chunks, _ = search_code(test_steps_str)

            # 5. Generate Java code
            java_code = generate_java_code(test_steps_str, chunks)

            st.success("✅ Java code generated!")
            with st.expander("📄 Response: Generated Java Code"):
                st.code(java_code, language="java")

        except Exception as e:
            st.error("❌ Failed to generate Java code.")
            st.code(str(e))
