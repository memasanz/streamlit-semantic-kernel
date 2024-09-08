import streamlit as st  
from streamlit_chat import message  
import asyncio  
from semantic_kernel import Kernel  
  
async def main():  
    st.title("Semantic Kernel Demo")    
  
    kernel = Kernel()  
    funFunctions = kernel.add_plugin(parent_directory=".", plugin_name="FunPlugin")  
    jokeFunction = funFunctions["Joke"]  
    result = await kernel.invoke(jokeFunction, input="travel to dinosaur age", style="silly")  
    st.write(result)  
  
# Run the main function using the st.asyncio decorator  
asyncio.run(main())  