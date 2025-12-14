from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()
model=init_chat_model(model="gpt-4o-mini")

app = FastAPI()

# Create agent once at startup
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}! with a temperature of 70 degrees Fahrenheit"

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/chat")
async def chat(request: MessageRequest):
    """Send a message to the agent."""
    result = agent.invoke({
        "messages": [{"role": "user", "content": request.message}]
    })
    
    # Extract response text from agent output
    response_text = result["messages"][-1].content
    
    return MessageResponse(response=response_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)