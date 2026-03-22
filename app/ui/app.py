import sys
import os
import subprocess
import hashlib
import logging
import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.components import (
    read_codebase_files,
    embed_and_store,
    search_code,
    generate_java_code,
    clone_repo,
    get_local_repo_path,
    get_project_folder_name,
    run_git_command,
)

# ---------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------
STATIC_CODEBASE_PATH = ""
BASE_CLONE_DIR = "/app/repos"

if not os.path.exists(BASE_CLONE_DIR):
    os.makedirs(BASE_CLONE_DIR)

USE_GIT_REPO = st.sidebar.toggle("📁 Use Git Repository Instead", value=False)
GIT_REPO_URL = None
GIT_REPO_PATH = None

# logger.info(f"Use Git Repository: {USE_GIT_REPO}")

if USE_GIT_REPO:
    st.sidebar.markdown("### 🧬 Git Repository Input")
    GIT_REPO_URL = st.sidebar.text_input("🔗 Git Repository URL", placeholder="https://github.com/user/repo.git")
    username = st.sidebar.text_input("👤 Git Username")
    pat = st.sidebar.text_input("🔑 Personal Access Token (PAT)", type="password")

    st.sidebar.write("📦 Debug")
    st.sidebar.write("GIT_REPO_URL:", GIT_REPO_URL)
    st.sidebar.write("Username:", username)
    st.sidebar.write("PAT Provided:", bool(pat))

    project_name = st.sidebar.text_input("📛 Project Name (used for vector DB)", placeholder="MyTestProject")
    branch_name = st.sidebar.text_input("🌿 Branch Name", placeholder="main")
    
    st.sidebar.write("Project Name:", project_name)
    st.sidebar.write("Branch Name:", branch_name)

    if GIT_REPO_URL and username and pat and project_name and branch_name:
        try:
            if "git_repo_path" not in st.session_state:
                st.sidebar.info("⏳ Cloning or updating repository...")
                cloned_path = clone_repo(GIT_REPO_URL, username, pat, branch_name=branch_name)
                st.session_state.git_repo_path = cloned_path
                st.sidebar.success(f"✅ Repository cloned: `{cloned_path}`")
            GIT_REPO_PATH = st.session_state.git_repo_path
            st.sidebar.write("📂 Final GIT_REPO_PATH:", GIT_REPO_PATH)
        except Exception as e:
            st.sidebar.error("❌ Failed to access repository.")
            st.sidebar.exception(e)
    else:
        st.sidebar.warning("🚨 Please enter all Git credentials.")
else:
    GIT_REPO_PATH = STATIC_CODEBASE_PATH
    # logger.info(f"Using local codebase path: {GIT_REPO_PATH}")

# ---------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="📄 Test Steps ➡️ 💻 Java Code Generator",
    layout="wide",
    page_icon="💻",
)

# ---------------------------------------------------------------------
# GLOBAL STYLE
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: #2e2e2e;
        font-family: 'Segoe UI', sans-serif;
    }
    section.main > div {
        min-height: 100vh;
    }
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
        height: 100%;
    }
    div[data-testid="column"]:nth-of-type(2) > div {
        height: 100%;
        display: flex;
        align-items: stretch;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------
with st.container():
    st.markdown("""
        <style>
        .header-container {
            text-align: center;
            padding: 2rem 1rem 1.2rem 1rem;
            background: linear-gradient(to right, #c8102e, #f39200);
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            color: white;
        }
        .header-container h1 {
            font-size: 2.4rem;
            margin-bottom: 0.2rem;
        }
        .header-container p {
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 0;
            opacity: 0.95;
        }
        </style>

        <div class="header-container">
            <h1>🧪 Smart Test Steps ➡️ Java Code Generator</h1>
            <p>AI-powered automation to turn test scenarios into clean, production-ready Java code</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------------------
st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .how-it-works-container {
        font-size: 1rem;
        line-height: 1.6;
    }
    .step-box {
        background-color: #f4f4f4;
        border-left: 6px solid #c8102e;
        padding: 0.9rem 1.2rem;
        margin-bottom: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    .step-box h4 {
        margin: 0;
        font-size: 1.15rem;
        font-weight: 600;
        color: #c8102e;
    }
    .step-box p {
        margin: 0.3rem 0 0;
        color: #333;
    }
    .step-box small {
        font-size: 0.9rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

with st.expander("📘 How It Works", expanded=False):
    st.markdown("""
<div class="how-it-works-container">
    <div class="step-box">
        <h4>📝 Step 1: Enter or Upload Test Steps</h4>
        <p>Provide your functional test steps either manually, by pasting, or uploading a <code>.txt</code> file.</p>
        <small>Each line is treated as a separate instruction for conversion.</small>
    </div>
    <div class="step-box">
        <h4>📂 Step 2: Load Your Java Codebase</h4>
        <p>The app reads your provided Java project and builds an index using semantic vectors.</p>
        <small>This allows for contextual code matching.</small>
    </div>
    <div class="step-box">
        <h4>🤖 Step 3: Generate Matching Java Code</h4>
        <p>LLMs process your steps and suggest Java code using reusable methods and patterns.</p>
        <small>It considers class/method structure for better integration.</small>
    </div>
    <div class="step-box">
        <h4>📥 Step 4: Review & Download</h4>
        <p>Inspect the output Java code, make refinements if needed, and download it instantly.</p>
        <small>You can plug it directly into your automation framework.</small>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------
left_col, divider_col, right_col = st.columns([1, 0.02, 1], gap="large")

# LEFT: INPUT
with left_col:
    st.markdown("### ✍️ How would you like to provide the test steps?")
    st.markdown("<div style='margin-bottom: -0.4rem;'><strong style='font-size: 1.1rem;'>Choose input method:</strong></div>", unsafe_allow_html=True)

    input_mode = st.radio(
        "",
        options=["Enter Manually", "Paste All Steps", "Upload File"],
        horizontal=True,
        key="input_mode_radio",
    )

    if "test_steps" not in st.session_state:
        st.session_state.test_steps = [""]

    test_steps = []

    if input_mode == "Enter Manually":
        for idx in range(len(st.session_state.test_steps)):
            step = st.session_state.test_steps[idx]
            text_col, del_col = st.columns([10, 1], gap="small")
            with text_col:
                st.session_state.test_steps[idx] = st.text_input(
                    f"**Test Step {idx + 1}:**", value=step, key=f"step_{idx}"
                )
            with del_col:
                st.markdown("<div style='margin-top: 1.9rem'></div>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.test_steps.pop(idx)
                    st.rerun()

        add_col, _, clear_col = st.columns([3, 6, 3])
        with add_col:
            if st.button("➕ Add Step", key="add_step_btn"):
                st.session_state.test_steps.append("")
                st.rerun()
        with clear_col:
            if st.button("🗑️ Clear All", key="clear_steps_btn"):
                st.session_state.test_steps = [""]
                st.rerun()

        test_steps = st.session_state.test_steps

    elif input_mode == "Paste All Steps":
        pasted_steps = st.text_area("Paste your test steps here (one per line):", height=200)
        if pasted_steps:
            test_steps = [line.strip() for line in pasted_steps.splitlines() if line.strip()]

    elif input_mode == "Upload File":
        uploaded_file = st.file_uploader("Upload a `.txt` file with test steps:", type=["txt"])
        if uploaded_file:
            try:
                file_content = uploaded_file.read().decode("utf-8")
                test_steps = [line.strip() for line in file_content.splitlines() if line.strip()]
                st.success("✅ Test steps extracted from file.")
            except UnicodeDecodeError:
                st.error("❌ Uploaded file is not UTF-8 encoded.")

    if input_mode != "Enter Manually" and test_steps:
        st.markdown("### ✅ Current Test Steps")
        for i, step in enumerate(test_steps):
            st.markdown(f"- **Test Step {i + 1}:** {step}")

# MIDDLE DIVIDER
with divider_col:
    st.markdown("""
        <div style='
            width: 3px;
            height: 3000px;
            background-color: #c8102e;
            margin: auto;
        '></div>
    """, unsafe_allow_html=True)

# RIGHT: OUTPUT
with right_col:
    st.markdown("""
        <style>
        .heading-style h3 {
            margin: 0;
            font-size: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    heading_col, button_col = st.columns([4, 2])
    with heading_col:
        st.markdown('<div class="heading-style"><h3>⚙️ Generate Java Code</h3></div>', unsafe_allow_html=True)
    with button_col:
        run_clicked = st.button("🚀 Run Code Generation", use_container_width=True)

    status_placeholder = st.empty()
    output_placeholder = st.empty()

    if run_clicked:
        if not test_steps or not any(s.strip() for s in test_steps):
            status_placeholder.error("❌ Please enter at least one test step.")
        elif not GIT_REPO_PATH or not os.path.exists(GIT_REPO_PATH):
            status_placeholder.error(f"❌ Codebase path is invalid or Git repo failed:\n`{GIT_REPO_PATH}`")
        else:
            try:
                status_placeholder.info("🔍 Reading codebase files…")
                test_steps_str = "\n".join([s.strip() for s in test_steps if s.strip()])
                files = read_codebase_files(GIT_REPO_PATH)
                status_placeholder.info(GIT_REPO_PATH)
                status_placeholder.info("🧠 Performing Embedding Additions")
                embed_and_store(files,project_name=project_name)
                    
                status_placeholder.info("🧠 Performing semantic search…")
                chunks, _ = search_code(test_steps_str, project_name=project_name,top_k=5)

                status_placeholder.info("⚙️ Generating Java code…")
                java_code = generate_java_code(test_steps_str, chunks, placeholder=output_placeholder)

                encoded_java = quote(java_code)
                download_button_html = f"""
                    <div style="margin-top: 1rem; padding: 1rem; background-color: #f4f4f4; border-left: 6px solid #f39200; border-radius: 8px;">
                        ✅ Java code generated successfully!<br><br>
                        <a href="data:text/plain;charset=utf-8,{encoded_java}"
                           download="{project_name}.java"
                           style="
                               display: inline-block;
                               padding: 0.5rem 1rem;
                               background-color: #c8102e;
                               color: white;
                               border-radius: 6px;
                               text-decoration: none;
                               font-weight: bold;
                           ">
                            📥 Download Java Code
                        </a>
                    </div>
                """
                status_placeholder.markdown(download_button_html, unsafe_allow_html=True)

            except Exception as e:
                status_placeholder.error("❌ Failed to generate Java code.")
                st.exception(e)
