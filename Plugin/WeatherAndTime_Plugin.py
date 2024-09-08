
import asyncio
from typing import Annotated
import datetime

from semantic_kernel.exceptions import FunctionExecutionException
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel_pydantic import KernelBaseModel

class WeatherAndTime_Plugin:
    """A sample plugin that provides weather information for cities."""

    @kernel_function(name="get_weather_for_city", description="Get the weather for a city")
    def get_weather_for_city(self, city: Annotated[str, "The input city"]) -> Annotated[str, "The output is a string"]:
        if city == "Boston":
            return "61 and rainy"
        elif city == "London":
            return "55 and cloudy"
        elif city == "Miami":
            return "80 and sunny"
        elif city == "Paris":
            return "60 and rainy"
        elif city == "Tokyo":
            return "50 and sunny"
        elif city == "Sydney":
            return "75 and sunny"
        elif city == "Tel Aviv":
            return "80 and sunny"
        else:
            return "31 and snowing"
        
    @kernel_function(description="Get the current date and time in the local time zone")
    def now(self) -> str:
        """Get the current date and time in the local time zone.

        Example:
            {{time.now}} => Sunday, January 12, 2031 9:15 PM
        """
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y %I:%M %p")