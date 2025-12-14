"""WhatsApp AI agent using pywa and LangChain."""
from pywa import WhatsApp
from pywa.types import Message
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define tools (module-level OK)
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's sunny in {city} with a temperature of 70°F"


def start_whatsapp_agent():
    """Initialize env, model, WhatsApp client and start the message loop."""
    load_dotenv()

    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    token = os.getenv("WHATSAPP_TOKEN")
    if not phone_id or not token:
        raise ValueError("WHATSAPP_PHONE_ID and WHATSAPP_TOKEN must be set in .env")

    # Initialize WhatsApp
    wa = WhatsApp(phone_id=phone_id, token=token)

    # Initialize LangChain model
    model = ChatOpenAI(model="gpt-4o-mini")

    # Create agent using latest LangChain API
    agent = create_agent(
        model=model,
        tools=[get_weather],
        system_prompt="You are a helpful WhatsApp assistant. Answer questions concisely."
    )

    # Register handler after wa is created so imports don't fail
    @wa.on_message()
    def handle_message(message: Message):
        """Handle incoming WhatsApp messages."""
        logger.info(f"Message from {message.from_user.phone_number}: {message.text}")
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": message.text}]
            })
            reply_text = result["messages"][-1].content
            wa.send_message(to=message.from_user.phone_number, text=reply_text)
            logger.info(f"Sent reply to {message.from_user.phone_number}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            wa.send_message(
                to=message.from_user.phone_number,
                text="Sorry, something went wrong. Please try again."
            )

    # Run the client (blocking)
    wa.run()


if __name__ == "__main__":
    start_whatsapp_agent()
