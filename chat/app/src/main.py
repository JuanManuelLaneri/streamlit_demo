import os
import streamlit as st
from langchain.llms import OpenAI
from dotenv import load_dotenv
from pm_policy_chat.retriever import get_retriever
from langchain.embeddings.openai import OpenAIEmbeddings
from textwrap import dedent
from langchain.schema import SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits.conversational_retrieval.openai_functions import \
    create_conversational_retrieval_agent
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.prompts.chat import MessagesPlaceholder

st.title('🦜🔗 Quickstart App')

load_dotenv(override=True)

system_message = dedent(
    """
        You are an AI assistant that helps the user to get code snippet and solutions for the team. 
        You have tools available to retrieve corresponding defenitions of current credit variables code, make sure to analyse the code snippets to provide the answers.
        When answering a complex question make sure to split this question to simpler questins and use tools available to you to answer them.

        Feel free to provide code examples when neede to explain it better to the user.
        
        

        Constraints:
        - You can only use tools available to you.
        - You can use same tool multiple times if you need to fetch additional information.
        - If you did not find the answer by using tools available to you then ask the user ask the user for more information.
        - Do not use the same tool more than 4 times in a row. If you need to use the same tool more than 4 times in a row, ask the user for more information.
    """
)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me about Credit Variables!"}
    ]

# Integrate langchain memory with streamlit
msgs = StreamlitChatMessageHistory()
memory_key = "chat_history"
memory = ConversationBufferMemory(
    chat_memory=msgs,
    return_messages=True,
    memory_key=memory_key,
    output_key="output",
)

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.status(
                    f"**{step[0].tool}**: {step[0].tool_input}", state="complete"
            ):
                st.write(step[0].log)
                st.write(step[1])
        st.write(msg.content)

if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    msgs.add_ai_message("Ask me about Credit Variables!")
    st.session_state.steps = {}

if prompt := st.chat_input(placeholder="How should I build a new variable"):
    st.chat_message("user").write(prompt)

    llm = ChatOpenAI(streaming=True, temperature=0.2, model="gpt-4-0613")

    functions_prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=SystemMessage(content=system_message),
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)],
    )

    agent = OpenAIFunctionsAgent(llm=llm, tools=get_retriever().get_tools(), prompt=functions_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=get_retriever().get_tools(),
        memory=memory,
        verbose=True,
        streaming=True
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(
            st.container(), expand_new_thoughts=True, collapse_completed_thoughts=True
        )
        response = agent_executor(prompt, callbacks=[st_cb])
        st.write(response["output"])