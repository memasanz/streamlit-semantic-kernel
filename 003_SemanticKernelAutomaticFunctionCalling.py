#streamlit web app that uses the semantic kernel to generate jokes
#on local machine run: streamlit run 001_jokewebapp.py

import streamlit as st
import asyncio
from typing import Annotated
import os
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (AzureChatPromptExecutionSettings,)
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel import Kernel
from semantic_kernel.functions import KernelArguments

from service_settings import ServiceSettings
from Plugin.EmailPlugin import EmailPlugin
from Plugin.Time_Plugin import Time_Plugin
from Plugin.WeatherPlugin import WeatherPlugin
from Plugin.WaitPlugin import WaitPlugin
from Plugin.ColorPlugin import ColorPlugin


# A helper method to invoke the agent with the user input
async def invoke_agent(kernel, chat_completion, input_text):
   
    
    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()


    st.session_state["history"].add_user_message(input_text)

    result = (await chat_completion.get_chat_message_contents(
            chat_history=st.session_state["history"],
            settings=execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ))[0]
    print(str(result))

    st.session_state["history"].add_assistant_message(str(result))
    return str(result)



async def setup_kernel_and_chat():
    kernel = Kernel()
    service_settings = ServiceSettings.create()
    # Remove all services so that this cell can be re-run without restarting the kernel
    kernel.remove_all_services()

    service_id = "default"
    kernel.add_service(AzureChatCompletion(service_id=service_id,),)
    kernel.add_plugin(EmailPlugin(),plugin_name="Email",)
    kernel.add_plugin(Time_Plugin(),plugin_name="Time",)
    kernel.add_plugin(WeatherPlugin(),plugin_name="Weather",)
    kernel.add_plugin(WaitPlugin(),plugin_name="Wait",)
    kernel.add_plugin(ColorPlugin(),plugin_name="Color",)

    chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    return kernel, chat_completion

async def run_app():
    st.title("PlugIn Bot")
    st.write('gpt model with Email, Time, Weather, Wait, Color for locatoin Plugin')
    st.write('The known locations are: Boston, London, Miami, Paris, Tokyo, Sydney, Tel Aviv')

    reset = st.button('Reset Messages')

    if reset:
            st.write('Sure thing!')
            history = ChatHistory()
            st.session_state["history"] = history
            st.session_state["history"].add_system_message("You are a helpful assistant.") 
            print("completed reset")
            reset = False

    if "history" not in st.session_state:  
        history = ChatHistory()
        st.session_state["history"] = history
        st.session_state["history"].add_system_message("You are a helpful assistant.") 

    
 
    if "kernel" not in st.session_state or "function" not in st.session_state:
        kernel, function = await setup_kernel_and_chat()
        st.session_state["function"] = function
        st.session_state["kernel"] = kernel
        

    for msg in st.session_state["history"]:
        print(msg.role + ":" + msg.content)
        with st.chat_message(msg.role):
            st.markdown(msg.content)

    # React to user input
    if prompt := st.chat_input("Tell me about an email you want to send...(or something else)"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        result = await invoke_agent(st.session_state["kernel"], st.session_state["function"] , prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(result)

asyncio.run(run_app())  