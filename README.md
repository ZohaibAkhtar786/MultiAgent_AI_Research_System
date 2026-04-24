# 🧠 Multi-Agent Research System

An AI-powered research pipeline built with **LangChain**, **GPT-4o mini**, **Tavily Search**, and **BeautifulSoup** — wrapped in a sleek **Streamlit** UI.

## 🔄 Pipeline Overview

```
🔍 Search Agent → 📄 Reader Agent → ✍️ Writer Chain → 🧠 Critical Thinking Chain
```

1. **Search Agent** — Uses Tavily to find recent, reliable information on your topic
2. **Reader Agent** — Scrapes the most relevant URL for deeper content
3. **Writer Chain** — Generates a structured research report (Intro, Key Findings, Conclusion, Sources)
4. **Critical Thinking Chain** — Critiques the report and gives it a score out of 10

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and add your API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

- Get your OpenAI key: https://platform.openai.com/api-keys
- Get your Tavily key: https://app.tavily.com

### 4. Run the app

```bash
streamlit run app.py
```

## 📁 Project Structure

```
├── app.py          # Streamlit UI
├── pipeline.py     # Orchestrates the full research pipeline
├── Agents.py       # Search Agent, Reader Agent, Writer & Critic chains
├── tools.py        # web_search and scrape_url tools
├── requirements.txt
├── .env.example    # Template for environment variables
└── .gitignore
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain + LangGraph | Agent orchestration |
| GPT-4o mini (OpenAI) | Language model |
| Tavily | Web search API |
| BeautifulSoup | Web scraping |
| Streamlit | Frontend UI |

## ☁️ Deployment on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Under **Advanced settings → Secrets**, add:
   ```
   OPENAI_API_KEY = "your_key_here"
   TAVILY_API_KEY = "your_key_here"
   ```
5. Click **Deploy** — done!

## ⚠️ Important

- **Never commit your `.env` file** — it's listed in `.gitignore`
- Always use `.env.example` to share the required key names safely

## 📄 License

MIT License
