# WhatsApp AI Agent Setup

## Prerequisites

1. **Meta Business Account** - Required for WhatsApp Cloud API
2. **Phone Number** - A phone number for your WhatsApp Business Account
3. **OpenAI API Key** - For LangChain integration

## Setup Steps

### 1. Get WhatsApp Credentials

1. Go to [Meta for Developers](https://developers.facebook.com)
2. Create a new Business app (or use existing one)
3. Add WhatsApp product to your app
4. In WhatsApp > API Setup:
   - Copy your **Phone Number ID**
   - Copy your **Access Token** (or create a permanent one)

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```
OPENAI_API_KEY=your_openai_api_key
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_TOKEN=your_access_token
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Agent

```bash
python whatsapp_agent.py
```

The agent will:
- Listen for incoming WhatsApp messages
- Process them with LangChain + GPT-4o-mini
- Send responses back to the user
- Support tool calling (example: `get_weather`)

## How It Works

1. User sends a WhatsApp message
2. `handle_message()` receives the message
3. LangChain agent processes it with access to tools
4. Response is sent back to the user

## Testing Locally

For testing without a real number, use Meta's test phone numbers (up to 5 allowed numbers).

## Adding More Tools

Modify `whatsapp_agent.py` and add more tools using the `@tool` decorator:

```python
@tool
def your_custom_tool(param: str) -> str:
    """Tool description."""
    return "Result"
```

Then add to the tools list when creating the agent.
