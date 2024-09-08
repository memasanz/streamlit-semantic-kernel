
import asyncio
from typing import Annotated

from semantic_kernel.exceptions import FunctionExecutionException
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel_pydantic import KernelBaseModel

class ColorPlugin:
    """A sample plugin that provides weather information for cities."""

    @kernel_function(name="get_colors_for_city", description="Get the color for a city")
    def get_weather_for_city(self, city: Annotated[str, "The input city"]) -> Annotated[str, "The output is a string"]:
        if city == "Boston":
            return "red"
        elif city == "London":
            return "blue"
        elif city == "Miami":
            return "green"
        elif city == "Paris":
            return "yellow"
        elif city == "Tokyo":
            return "pink"
        elif city == "Sydney":
            return "purple"
        elif city == "Tel Aviv":
            return "black"
        else:
            return "white"