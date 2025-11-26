import os
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel
from tools import pdf_text_extractor # Our custom tool
from dotenv import load_dotenv

load_dotenv()
# Load Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Initialize the Gemini model via LitellmModel
# Using a common Gemini model, you can replace with a more specific one if needed.
gemini_model = LitellmModel(
    model="gemini/gemini-2.5-flash", # Explicitly use gemini provider via Google AI Studio
    api_key=GEMINI_API_KEY
)

# Create the agent
summarizer_quiz_agent = Agent(
    name="PDF Summarizer and Quiz Generator",
    instructions=(
        "You are a helpful assistant that summarizes academic PDFs and generates quizzes (MCQs or mixed). "
        "You have access to a tool called `pdf_text_extractor` which can read the content of a PDF file "
        "given its file path. When a user asks you to summarize or create a quiz from a PDF, "
        "you MUST first use the `pdf_text_extractor` tool with the provided file path to get the text, "
        "and then proceed with summarization or quiz generation using that extracted text. "
        "Always use the original extracted PDF text for quiz generation. "
        "If the `pdf_text_extractor` tool returns an error or empty text, inform the user."
    ),
    model=gemini_model,
    tools=[pdf_text_extractor], # Register our PDF extraction tool
)

# You can add a main block here for testing the agent if needed
if __name__ == "__main__":
    import asyncio

    async def test_agent():
        # This is a placeholder for actual testing.
        # In a real scenario, you'd use Runner.run with a specific task
        # and a file_path for pdf_text_extractor.
        print("Agent configured successfully. This is a placeholder for testing.")
        print("To test the agent, you would typically use Runner.run(agent, input, ...)")
        print("Example: await Runner.run(summarizer_quiz_agent, 'Summarize this PDF: /path/to/doc.pdf')")
        # Example of how you might run a tool directly for a test (not how agent uses it)
        # print(pdf_text_extractor(file_path="dummy.pdf"))
        pass # The actual running of the agent will be in app.py

    asyncio.run(test_agent())
