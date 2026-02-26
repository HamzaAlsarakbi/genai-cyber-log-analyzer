import os
import json
import time
import argparse
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from openai import RateLimitError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load API key from .env file
load_dotenv()

# We use the ChatOpenAI class but point it to the OpenRouter base URL
# This allows LangChain to seamlessly interact with OpenRouter's free models
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    max_retries=0
)

# Define the LangChain Prompt Template
template = """
You are a senior cybersecurity analyst. Analyze the following server access logs.
Identify any suspicious behavior, cyber threats, or vulnerabilities.

Server Logs:
{logs}

Provide your analysis in the following JSON format ONLY. Do not include markdown formatting like ```json.
{{
    "threats_detected": [
        {{
            "ip_address": "string",
            "vulnerability_type": "string",
            "risk_level": "Low, Medium, High, or Critical",
            "evidence": "string (the exact log line)",
            "mitigation_strategy": "string"
        }}
    ]
}}
"""

prompt = PromptTemplate(
    input_variables=["logs"],
    template=template
)

def analyze_logs(log_file_path, output_file_path=None, max_retries=3):
    logger.info(f"Reading logs from {log_file_path}...")
    try:
        with open(log_file_path, 'r') as file:
            logs = file.read()
    except FileNotFoundError:
        logger.error(f"Could not find {log_file_path}")
        return

    logger.info("Analyzing logs via Groq (Llama 3.3 70B)...")
    
    # Create the execution chain
    chain = prompt | llm 
    
    # Retry logic with exponential backoff
    for attempt in range(max_retries):
        try:
            # Execute the LLM call
            response = chain.invoke({"logs": logs})
            
            try:
                # Parse the output to ensure it's valid JSON
                result_json = json.loads(response.content.strip())
                logger.info("Cyber Threat Intelligence Report:")
                logger.info(json.dumps(result_json, indent=4))
                
                # Save to file if output path is specified
                if output_file_path:
                    with open(output_file_path, 'w') as f:
                        json.dump(result_json, f, indent=4)
                    logger.info(f"Report saved to {output_file_path}")
                
                return
            except json.JSONDecodeError:
                logger.error("The model failed to return valid JSON. Raw output:")
                logger.error(response.content)
                return
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(f"Rate limited. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries - 1}...")
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limited after {max_retries} attempts.")
                logger.error(f"OpenRouter message: {str(e)}")
                logger.warning("Please try again in a few minutes or switch to a different model.")
                return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze server logs for cyber threats using AI"
    )
    parser.add_argument(
        "-f", "--file",
        default="server_logs.txt",
        help="Path to the log file to analyze (default: server_logs.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save the JSON report (optional)"
    )
    
    args = parser.parse_args()
    analyze_logs(args.file, output_file_path=args.output)