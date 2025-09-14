import chainlit as cl
from agents import Runner,AsyncOpenAI,OpenAIChatCompletionsModel,Agent,RunConfig
from decouple import config


key = config('GEMINI_API_KEY')
base_url = config('base_url') 

client = AsyncOpenAI(
    api_key=key,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client = client,
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

agent = Agent(
    name="Personal Assistant",
    instructions="you are a personal assistant",
)

@cl.on_chat_start
async def handle_chat():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello, I am a personal assistant. How can I help you?").send()

@cl.on_message
async def handle(message : cl.Message):
    history = cl.user_session.get("history")
    history.append({"role":"user","content":message.content})
    result = await Runner.run(
        agent,
        input=history,
        run_config=config
    )
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(content=result.final_output).send()
