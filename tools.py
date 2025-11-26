import os
from agents import function_tool
from extractor import extract_pdf_text

@function_tool
def pdf_text_extractor(file_path: str) -> str:
    """
    Extracts text from a PDF file located at the given file_path.
    Returns the extracted text as a string.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    extracted_text = extract_pdf_text(file_path)
    if not extracted_text:
        return f"Could not extract text from {file_path} or PDF is empty."
    return extracted_text

# Additional MCP tools would go here if required by Context7 format.
# Based on the current problem statement, only PDF extraction is explicitly required as a tool.
# The Context7 MCP was mentioned as a "tool provider to supply additional utilities if required",
# and for "Tools MUST follow the exact pattern required by OpenAgents and Context7 MCP."
# Since openai-agents is being used, and the documentation for it shows direct function tools,
# I will assume for now that direct @function_tool is the way to expose tools.
# If Context7 MCP requires a specific wrapping or registration, that will need further investigation
# when we get to integrating with Context7 MCP specifically, but for now, the PDF extraction tool
# for the agent will be defined directly.
