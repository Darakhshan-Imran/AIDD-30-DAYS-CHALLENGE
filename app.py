import streamlit as st
import os
import asyncio
import tempfile
from pathlib import Path
import streamlit.components.v1 as components

# Import our agent and tool
from agent import summarizer_quiz_agent
from extractor import extract_pdf_text
from agents import Runner # Import Runner to run the agent

# --- Configuration ---
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True) # Ensure storage directory exists

st.set_page_config(layout="wide")
st.title("📚 PDF Summarizer & Quiz Generator")

# --- Session State Initialization ---
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = ""
if "pdf_file_path" not in st.session_state:
    st.session_state.pdf_file_path = ""
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

# --- PDF Upload Section ---
st.header("1. Upload your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file to storage
    # Using tempfile to create a unique path for the uploaded file
    # This ensures that multiple uploads don't overwrite each other if they have the same name.
    # We will save it in the STORAGE_DIR.
    file_path = Path(STORAGE_DIR) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.session_state.pdf_file_path = str(file_path)
    st.success(f"File saved to {st.session_state.pdf_file_path}")

    # Reset extracted text and results when a new file is uploaded
    st.session_state.extracted_text = ""
    st.session_state.summary = ""
    st.session_state.quiz = ""

# --- Action Buttons ---
st.header("2. Generate Content")

col1, col2, col3 = st.columns(3)

with col1:
    summary_user_prompt = st.text_input("Enter a prompt for summary (e.g., 'Summarize this PDF in 200 words'):", 
                                          value="Summarize this PDF.",
                                          key="summary_input",
                                          disabled=not st.session_state.pdf_file_path)

    if st.button("Generate Summary", use_container_width=True, disabled=not st.session_state.pdf_file_path):
        if st.session_state.pdf_file_path:
            with st.spinner("Generating summary..."):
                try:
                    # Construct prompt for summarization, instructing the agent to use the tool
                    summary_prompt = (
                        f"{summary_user_prompt} "
                        f"Extract text from the PDF at the following path and then summarize it: {st.session_state.pdf_file_path}"
                    )
                    
                    result = asyncio.run(Runner.run(summarizer_quiz_agent, summary_prompt))
                    st.session_state.summary = result.final_output
                    st.success("Summary generated!")
                except Exception as e:
                    st.error(f"Error generating summary: {e}")
        else:
            st.warning("Please upload a PDF first.")

with col2:
    quiz_user_prompt = st.text_input("Enter a prompt for quiz (e.g., 'Create a 5-question MCQ quiz'):",
                                       value="Create a 5-question mixed-style quiz (MCQs and short answer).",
                                       key="quiz_input",
                                       disabled=not st.session_state.pdf_file_path)

    if st.button("Create Quiz", use_container_width=True, disabled=not st.session_state.pdf_file_path):
        if st.session_state.pdf_file_path:
            with st.spinner("Generating quiz..."):
                try:
                    # Construct prompt for quiz generation, instructing the agent to use the tool
                    quiz_prompt = (
                        f"{quiz_user_prompt} "
                        f"Extract text from the PDF at the following path and then create a quiz from it: {st.session_state.pdf_file_path}"
                    )
                    
                    result = asyncio.run(Runner.run(summarizer_quiz_agent, quiz_prompt))
                    st.session_state.quiz = result.final_output
                    st.success("Quiz generated!")
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")
        else:
            st.warning("Please upload a PDF first.")

with col3:
    flashcards_user_prompt = st.text_input("Enter a prompt for flashcards (e.g., 'Generate 10 flashcards with key points'):",
                                          value="Generate 5-7 flashcards with a main topic and 3-5 key points for each, in JSON format.",
                                          key="flashcards_input",
                                          disabled=not st.session_state.pdf_file_path)

    if st.button("Generate Flashcards", use_container_width=True, disabled=not st.session_state.pdf_file_path):
        if st.session_state.pdf_file_path:
            with st.spinner("Generating flashcards..."):
                try:
                    flashcards_prompt = (
                        f"{flashcards_user_prompt} "
                        f"Extract text from the PDF at the following path: {st.session_state.pdf_file_path}. "
                        f"The JSON output should be a list of dictionaries, where each dictionary has a 'topic' (string) and 'key_points' (list of strings). "
                        f"Example JSON format: "
                        f"```json\n"
                        f"[\n"
                        f"  {{\"topic\": \"Main Topic 1\", \"key_points\": [\"Point 1.1\", \"Point 1.2\"]}},\n"
                        f"  {{\"topic\": \"Main Topic 2\", \"key_points\": [\"Point 2.1\", \"Point 2.2\", \"Point 2.3\"]}}\n"
                        f"]\n"
                        f"```"
                    )
                    
                    result = asyncio.run(Runner.run(summarizer_quiz_agent, flashcards_prompt))
                    flashcards_json_string = result.final_output

                    import json
                    import re # Import re for regex

                    try:
                        # Attempt to extract JSON from agent's output, looking for markdown code blocks first
                        json_match = re.search(r"```json\n(.*?)```", flashcards_json_string, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1).strip()
                        else:
                            # Fallback: assume the entire output is JSON (less robust)
                            json_str = flashcards_json_string.strip()

                        st.session_state.flashcards = json.loads(json_str)
                        st.success("Flashcards generated!")
                    except json.JSONDecodeError:
                        st.error("Failed to parse flashcards from agent output. Please try again or refine the prompt.")
                        st.text("Raw Agent Output:", flashcards_json_string) # Show raw output for debugging
                        st.session_state.flashcards = [] # Clear malformed flashcards
                except Exception as e:
                    st.error(f"Error generating flashcards: {e}")
        else:
            st.warning("Please upload a PDF first.")

# --- Display Results ---
if st.session_state.summary:
    st.header("3. Summary")
    st.markdown(st.session_state.summary)

if st.session_state.quiz:
    st.header("4. Quiz")
    st.markdown(st.session_state.quiz)

if st.session_state.flashcards:
    st.header("5. Flashcards")
    # Display interactive flip-over flashcards
    
    full_html = """
    <style>
    .flashcard-container {
        perspective: 1000px;
        width: 300px; /* Adjust card width as needed */
        height: 200px; /* Adjust card height as needed */
        margin: 10px;
        float: left; /* To display cards in a grid-like fashion */
    }

    .flashcard {
        width: 100%;
        height: 100%;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.6s;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        cursor: pointer;
    }

    .flashcard.flipped {
        transform: rotateY(180deg);
    }

    .flashcard-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        padding: 20px;
        box-sizing: border-box;
        text-align: center;
    }

    .flashcard-front {
        background-color: #f0f8ff; /* Alice Blue */
        color: #333;
        font-size: 1.2em;
        font-weight: bold;
    }

    .flashcard-back {
        background-color: #e6e6fa; /* Lavender */
        color: #333;
        transform: rotateY(180deg);
        font-size: 1em;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }
    .flashcard-back ul {
        list-style-type: disc;
        padding-left: 20px;
    }
    .flashcard-back li {
        margin-bottom: 5px;
    }
    </style>
    <script>
    function flipCard(cardElement) {
        cardElement.classList.toggle('flipped');
    }
    </script>
    <div style='display: flex; flex-wrap: wrap;'>
    """

    for i, card in enumerate(st.session_state.flashcards):
        topic = card.get('topic', 'N/A')
        key_points = card.get('key_points', [])
        key_points_html = "<ul>" + "".join([f"<li>{point}</li>" for point in key_points]) + "</ul>"

        full_html += f"""
        <div class="flashcard-container" onclick="flipCard(this.querySelector('.flashcard'))">
            <div class="flashcard">
                <div class="flashcard-face flashcard-front">
                    {topic}
                </div>
                <div class="flashcard-face flashcard-back">
                    {key_points_html}
                </div>
            </div>
        </div>
        """
    full_html += "</div>" # Close the flex container

    components.html(full_html, height=450, scrolling=True)
