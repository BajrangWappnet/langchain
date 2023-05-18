from flask import Flask, request
from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import json


app = Flask(__name__)

load_dotenv()

@app.route('/api/chatgpt', methods=['POST'])
def post_data():
    data = request.json
    openai_key = os.getenv('OPENAI_API_KEY')
    os.environ["SERPER_API_KEY"]  = os.getenv('SERPAPI_API_KEY')
    # Use the secret key in your code
    
    llm = OpenAI(openai_api_key=openai_key, temperature=0)
    # Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    query = data['query']
    # Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    response = agent.run(query)

    payload = json.dumps({
        "response": response
    })



    return payload


if __name__ == '__main__':
    app.run()

