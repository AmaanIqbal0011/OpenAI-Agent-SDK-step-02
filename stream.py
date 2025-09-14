import chainlit as cl
from agents import Runner,AsyncOpenAI,OpenAIChatCompletionsModel,Agent,RunConfig
from decouple import config
from openai.types.responses import ResponseTextDeltaEvent


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
    msg = cl.Message(content="")
    await msg.send()
    history.append({"role":"user","content":message.content})
    result = Runner.run_streamed(
        agent,
        input=history,
        run_config=config
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(content=result.final_output).send()













# from agents import Runner,AsyncOpenAI,OpenAIChatCompletionsModel,Agent,RunConfig
# from decouple import config
# import asyncio

# from openai.types.responses.response_text_delta_event import ResponseTextDeltaEvent


# key = config('GEMINI_API_KEY')
# base_url = config('base_url') 

# client = AsyncOpenAI(
#     api_key=key,
#     base_url=base_url,
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client = client,
# )

# config = RunConfig(
#     model=model,
#     model_provider=client,
#     tracing_disabled=True
# )
# async def main():
#     agent = Agent(
#     name="Personal Assistant",
#     instructions="you are a personal assistant",
#     )


#     res = Runner.run_streamed(
#         agent,
#         input="who is the founder of pakistan,what do you know about these person",
#         run_config=config
#     )
#     async for event in res.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
#             print(event.data.delta,end="",flush=True)
    
   
# asyncio.run(main())