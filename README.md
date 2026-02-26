# GenAI Cyber Log Analyzer 🛡️🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

An automated cybersecurity threat detection tool that leverages Generative AI (via LangChain and Groq's Llama 3.3 70B) to parse, analyze, and classify raw server access logs.

This project demonstrates the integration of LLMs into traditional DevSecOps pipelines by converting unstructured log data into actionable, structured JSON threat intelligence.

## 🚀 Features

* **GenAI Orchestration:** Utilizes LangChain to dynamically construct prompts and enforce strict JSON output schemas from the LLM.
* **DevSecOps Ready:** Designed to run as an ephemeral, non-root Docker microservice, adhering to the principle of least privilege.
* **Volume Mounted I/O:** Securely reads logs and writes reports across host-container volume bridges without persistent storage risks.
* **Threat Classification:** Automatically identifies vectors such as SQL injections, Brute-Force attempts, and unauthorized access, assigning risk levels and mitigation strategies.

---

## ⚙️ Setup & Configuration

### 1. Environment Variables

Create a `.env` file in the root directory and add your API key:

```text
GROQ_API_KEY=your_actual_api_key_here
```

## 🐳 Execution: Docker (Recommended)

This is the preferred method as it runs the analyzer in an isolated, non-root environment. You can either pull the pre-built image from the GitHub Container Registry (GHCR) or build it locally.

### Option A: Pull from GHCR (Fastest)

1. Pull the pre-built image:

```bash
docker pull ghcr.io/hamzaalsarakbi/cyber_log_analyzer:latest
```

2. Run the Analyzer:

```bash
docker run --rm --env-file .env \
-v $(pwd):/app/ ghcr.io/hamzaalsarakbi/cyber_log_analyzer:latest \
-f server_logs.txt \
-o output.json
```

### Option B: Build Locally

1. Clone the repository

```bash
git clone https://github.com/HamzaAlsarakbi/genai-cyber-log-analyzer
cd genai-cyber-log-analyzer
```

2. Build the Image:

```bash
docker build -t cyber_log_analyzer .
```

3. Run the Analyzer

This command mounts your current directory, feeds the target log file to the container, saves the output locally, and then instantly destroys the container.

```bash
docker run --rm --env-file .env \
-v $(pwd):/app/ cyber_log_analyzer \
-f server_logs.txt \
-o output.json
```

## 🐍 Execution: Bare Metal (Python)

1. Clone the repository

```bash
git clone https://github.com/HamzaAlsarakbi/genai-cyber-log-analyzer
cd genai-cyber-log-analyzer
```

2. Setup the Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the Script

```bash
python main.py -f server_logs.txt -o output.json
```

## 📊 Example Output (`output.json`)

```json
{
    "threats_detected": [
        {
            "ip_address": "172.16.0.8",
            "vulnerability_type": "SQL Injection",
            "risk_level": "Critical",
            "evidence": "GET /products.php?id=1' OR '1'='1 HTTP/1.1",
            "mitigation_strategy": "Implement parameterized queries or prepared statements in the application code."
        }
    ]
}
```

## ⚖️ License & Disclaimer

Copyright (c) 2026 Hamza Alsarakbi

This project is licensed under the MIT License - see the `LICENSE` file for details.

Disclaimer: This tool is designed for educational and prototyping purposes to demonstrate the intersection of Generative AI and cybersecurity. It is not intended to be a standalone replacement for a dedicated SIEM (Security Information and Event Management) system or professional security auditing. Use at your own risk.
