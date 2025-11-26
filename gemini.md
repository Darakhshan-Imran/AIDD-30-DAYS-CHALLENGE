# Role: Senior Python AI Engineer

**Objective:** Build a "**PDF Summarizer + Quiz Generator Agent**" using the **OpenAI Agents SDK**, **Streamlit**, **PyPDF**, **Gemini CLI**, and **Context7 MCP**.

---

## 1. Project Overview

The goal is to create an AI agent that processes uploaded PDF files, extracts textual content, summarizes them, and generates quizzes (MCQs or mixed styles).

* **UI:** Streamlit (recommended) or custom HTML/CSS frontend.
* **Model:** Gemini model accessed via **OpenAI Agents SDK** and **Gemini CLI**.
* **PDF Processing:** PyPDF for text extraction.
* **Tooling:** Context7 MCP tool provider to supply additional utilities if required.
* **Core Deliverables:**

  * A clean PDF summary.
  * A quiz generated from original PDF text.

---

## 2. Critical Technical Constraints

**You must adhere to the following strict configuration rules:**

### 1. Zero-Bloat Protocol (CRITICAL)

* **Do NOT write extra code.**
* No unnecessary abstractions, no over-engineering, no additional error-handling unless explicitly specified.
* **Focus strictly on the integration:** PDF → Extract → Agent → Summary/Quiz → UI.
* **No hallucinated SDK functionalities.** Only use what is verified from OpenAgents SDK documentation.

### 2. API & SDK Configuration

* Use **OpenAI Agents SDK** (NOT the standard OpenAI library).
* Integrate the Gemini model using the **documented OpenAgents model loader**.
* Load the **Gemini API key** from environment variables.
* Use PyPDF **only** for extraction (not custom parsers, not OCR).

### 3. SDK Specificity

* Tools MUST follow the exact pattern required by OpenAgents and Context7 MCP.
* Confirm:

  * Tool decorator syntax.
  * Agent initialization pattern.
  * Message/response structure.
  * How to register external tools (Context7 MCP).

### 4. Error Recovery Protocol

If during development you encounter:

* `SyntaxError`
* `ImportError`
* `AttributeError`
  …related to **OpenAI Agents SDK**, **Context7 MCP**, or **Gemini CLI**:

➡️ **STOP IMMEDIATELY**
➡️ RE-FETCH the SDK documentation
➡️ Re-check exact syntax
➡️ Rewrite only after confirming correctness.

### 5. Dependency Management

* Use **uv** or **pip** (your choice, but stick to one).
* Avoid installing anything not required by specs.
* Only install:

  * openai agents
  * pypdf
  * streamlit
  * context7-mcp
  * gemini-cli (optional global)

---

## 3. Architecture & File Structure

**Use this exact structure:**

```text
.
├── .env                    # API keys (Gemini key required)
├── tools.py                # Tool functions for PDF extraction + MCP tools
├── agent.py                # Agent configuration with OpenAgents
├── app.py                  # Streamlit UI
├── extractor.py            # PyPDF logic for reading PDF content
├── storage/                # (Optional) Temp save space for uploaded files
└── pyproject.toml          # Project dependencies
```

> **Note:** Do NOT create folders not listed above unless absolutely required by the SDK.

---

## 4. Implementation Steps

**Follow this exact flow. No skipping or reordering.**

---

### Step 1: Documentation & Pattern Analysis

Before writing ANY code:

1. Use **Gemini CLI** or MCP query to fetch documentation for:

   * **OpenAI Agents SDK**
   * **Context7 MCP tool provider**

2. Analyze:

   * Tool format (`@tool` or `FunctionTool`)
   * Agent initialization pattern
   * How context/tools are attached
   * Expected message schema
   * Recommended model initialization syntax

3. If anything is unclear:
   **Re-run documentation query and confirm.**

---

### Step 2: PDF Extraction Tools (`tools.py` + `extractor.py`)

Create the PDF extraction functions using the strict SDK tool format.

**Functions:**

* `extract_pdf_text(file_path: str) -> str`

  * Uses PyPDF.
  * Returns raw combined text.
  * Handles missing text by returning `""`.

* Additional MCP tools (if required by Context7 format).

**Constraints:**

* No custom OCR, no token merging logic, no cleanup beyond `.strip()` and whitespace normalization.

---

### Step 3: Agent Configuration (`agent.py`)

Configure the agent exactly as documented:

1. Initialize the Gemini model through OpenAgents SDK.
2. Register tools:

   * PDF extraction tool
   * Any Context7 MCP tools
3. Create system prompt:

   ```
   You summarize academic PDFs and generate quizzes (MCQs or mixed). 
   Always use the original extracted PDF text for quiz generation.
   ```
4. Do NOT enable streaming unless explicitly required (default: off).

---

### Step 4: UI & Application Logic (`app.py`)

Using Streamlit:

#### **PDF Upload Section**

* A file uploader that writes PDF to `storage/`.
* On upload → call `extract_pdf_text()`.

#### **Summary Section**

* A button: **Generate Summary**
* Calls agent with extracted text.
* Renders summary in any UI style:

  * Card
  * Block
  * Scrollable container
  * Anything simple and non-bloat

#### **Quiz Section**

* A button: **Create Quiz**
* Sends original extracted PDF text to the agent.
* The agent generates:

  * MCQs
  * OR mixed-style quizzes
* The UI displays them neatly (list, questions block, etc.)

#### Constraints:

* No stateful memory unless available in Streamlit session state.
* No database allowed.

---

### Step 5: Environment & Dependencies

* Create `.env` template:

  ```
  GEMINI_API_KEY=
  ```

* Add dependencies to `pyproject.toml`:

  * openagents
  * pypdf
  * streamlit
  * context7-mcp

* **Avoid reinstalling** packages if already present.

---

## 5. Testing Scenarios

### **1. PDF Summarization**

* User uploads a PDF with 3+ pages.
* Summary is short, clean, and meaningful.
* No hallucinated content.

### **2. Quiz Generation**

* User clicks **Create Quiz**.
* Agent produces:

  * 5–10 MCQs **OR**
  * Mixed (MCQ + short questions).
* All questions must come from the **original PDF**, not the summary.

### **3. Robust PDF Handling**

* Works on text-heavy PDFs.
* Works even if some pages have minimal text.

### **4. UI Flow**

* Summary button appears only after upload.
* Quiz button appears only after summary.
* No crashes if PDF is short.

---

## 6. Deliverables

* `tools.py` — PDF extraction + MCP tools
* `extractor.py` — PyPDF logic
* `agent.py` — Agent configuration
* `app.py` — Streamlit UI
* `.env` — template
* `pyproject.toml` — dependencies
* `README.md` — run instructions

---

## 7. Non-Functional Requirements

* Keep code minimal and copy-paste ready.
* Only one-line comments allowed.
* No complex error handling.
* No unnecessary imports.
* No extra features unless optional.

---


