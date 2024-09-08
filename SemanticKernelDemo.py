from semantic_kernel import __version__
from semantic_kernel import Kernel
import logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from LightsPlugin import LightsPlugin
import os

import asyncio

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

class SemanticKernelDemo:
    def __init__(self):
        self.version = __version__
        self.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.history = ChatHistory()

       
        service_id = "default"
        self.kernel = Kernel()

        # Create the plugin
        lights_plugin = LightsPlugin(self.lights)
        
        #Add Chat Completion
        self.kernel.add_service(AzureChatCompletion(deployment_name=self.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,api_key=self.AZURE_OPENAI_API_KEY,base_url=self.AZURE_OPENAI_ENDPOINT))
        self.kernel.add_plugin(lights_plugin, plugin_name="Lights")

        logging.basicConfig(format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",datefmt="%Y-%m-%d %H:%M:%S",)
        logging.getLogger("kernel").setLevel(logging.DEBUG)


        self.chat_completion : AzureChatCompletion = self.kernel.get_service(type=ChatCompletionClientBase)
        #To enable automatic function calling
        # we first need to create the appropriate execution settings so that Semantic Kernel knows to automatically invoke the functions in the kernel when the AI agent requests them.

        behaviro = FunctionChoiceBehavior
        behaviro.auto_invoke_kernel_functions = True
        behaviro.maximum_auto_invoke_attempts = 3

        #execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto", function_call_behavior=behaviro)
        self.execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
        #execution_settings.function_call_beshavior = FunctionCallBehavior.EnableFunctions(auto_invoke=True, filters={})
        #execution_settings.function_choice_behavior = execution_settings.function_choice_behavior.Auto


        # for attr_name, attr_value in self.__dict__.items():  
        #         logging.info(f"{attr_name}: {attr_value}")
        #         print(f"{attr_name}: {attr_value}")

    def get_response_from_ai(self, message):
        result = self.chat_completion.get_chat_message_contents(chat_history=self.history,
                                                                  settings=self.execution_settings,
                                                                  kernel=self.kernel,
                                                                  arguments=KernelArguments(),)
        return str(result)


    def process(self):
        print("Processing data with semantic kernel")
