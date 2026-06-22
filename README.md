# CrewAI Text Processor Demo

This is a demonstration project showcasing how to use **CrewAI** with a local or open-source LLM provider (in this case, Groq) via LiteLLM.

It implements a simple web interface using **Flask** where users can input text. A CrewAI agent ("Text Analyst") is then deployed to analyze the text using a custom Python tool ("Text Statistics Analyzer") before generating a summary and extracting key points.

## Features

- **Flask Web Interface:** Clean, single-page UI for submitting text.
- **CrewAI Agentic Workflow:**
  - Defines an `Agent` with a specific persona ("Text Analyst").
  - Gives the agent access to a custom tool via the `@tool` decorator (`analyze_text_stats`).
  - Instructs the agent via a `Task` to first use the tool to get objective statistics, and *then* generate a summary and bullet points.
- **Groq Integration (Llama 3):** Uses the `groq/llama-3.3-70b-versatile` model for high-speed, free-tier compatible inference.

## Prerequisites

- Python 3.9+
- A [Groq API Key](https://console.groq.com/keys)

## Installation

1. **Clone the repository:**
   (Or simply navigate to the project directory)

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: We specifically pin `crewai==0.80.0` to avoid a `cache_breakpoint is unsupported` error with the Groq API.*

5. **Set up your Environment Variables:**
   Create a `.env` file in the root directory (same level as `app.py`) and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

## Running the Application

1. Ensure your virtual environment is activated.
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## How it Works

1. **`app.py`:** The main entry point for the Flask server. It serves the `index.html` frontend and exposes a `/process` POST endpoint.
2. **`crew_setup.py`:** Defines the CrewAI `Agent`, `Task`, and `Crew`. It initializes the LLM connection to Groq and maps the tools.
3. **`text_tools.py`:** Contains the `@tool` decorated Python function (`analyze_text_stats`) that the agent is permitted to execute during its reasoning loop.
4. **`templates/index.html`:** The frontend UI where users paste text and view the agent's results.

## Troubleshooting

- **`metadata-generation-failed` when installing numpy:** This happens if your system is missing a C compiler. Run `pip install numpy --only-binary=:all:` to force downloading pre-compiled binaries instead of building from source.
- **`litellm.BadRequestError: ... property 'cache_breakpoint' is unsupported`**: This indicates your version of CrewAI/LiteLLM is attempting to send Anthropic-specific prompt caching headers to Groq (which doesn't support them). Ensure you are using `crewai==0.80.0` as defined in the `requirements.txt`.
