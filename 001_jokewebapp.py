import streamlit as st
from semantic_kernel.contents.chat_history import ChatHistory

import asyncio
from typing import Annotated
import os

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel import Kernel
from service_settings import ServiceSettings
from semantic_kernel.functions import KernelArguments



# A helper method to invoke the agent with the user input
async def invoke_agent(mykernel, myfunction, input_text):
    """Invoke the kernel to create a joke for a topic with the user input."""
    st.session_state["history"].add_user_message(input_text)

    result = await mykernel.invoke(myfunction,KernelArguments(input=input_text, style="super silly"),)
    print(result)
    joke = result.value[0].inner_content.choices[0].message.content
    st.session_state["history"].add_assistant_message(joke)
    return joke


async def setup_kernel_and_agent():
    kernel = Kernel()
    service_settings = ServiceSettings.create()
    # Remove all services so that this cell can be re-run without restarting the kernel
    kernel.remove_all_services()

    service_id = "default"
    kernel.add_service(AzureChatCompletion(service_id=service_id,),)
    parent_directory = os.getcwd()
    plugin = kernel.add_plugin(parent_directory=parent_directory, plugin_name="FunPlugin")
    joke_function = plugin["Joke"]
    return kernel, joke_function

async def run_app():
    st.title("Joke Bot")
    st.write('Give a topic so I can give you back a joke')

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
        kernel, function = await setup_kernel_and_agent()
        st.session_state["function"] = function
        st.session_state["kernel"] = kernel
        

    for msg in st.session_state["history"]:
        print(msg.role + ":" + msg.content)
        with st.chat_message(msg.role):
            st.markdown(msg.content)

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        result = await invoke_agent(st.session_state["kernel"], st.session_state["function"] , prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(result)

asyncio.run(run_app())  