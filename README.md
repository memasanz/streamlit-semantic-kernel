## Getting your Semantic-Kernel Streamlit webapp moving

This repo is intended to show how to do things in a jupyter notebook, then followed up wiht a streamlit web app.

### Requirements:
- Pip install the requirements.txt file.
- .env file which should look like the one below:

```
GLOBAL_LLM_SERVICE="AzureOpenAI"
AZURE_OPENAI_API_KEY="XXX"
AZURE_OPENAI_ENDPOINT="https://xxx.openai.azure.com/"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4-1106"
AZURE_OPENAI_TEXT_DEPLOYMENT_NAME="gpt-4-1106"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="text-embedding-ada-002"
AZURE_OPENAI_API_VERSION="2024-05-01-preview"
##Semantic Kernel Settings:
AZURE_AISEARCH_API_KEY=""
AZURE_AISEARCH_URL=""
```

### Notebook Overview:

- [001_JokePlugIn.ipynb](001_JokePlugIn.ipynb): Using a Semantic Kernel Plugin from the Plugin directory.  If this won't work, we need to do some work.
- if that notebook works, then we should be able to leverage streamlit 
```
streamlit run 001_jokewebapp.py
```




## Semantic Kernel with Automatic Function Calling
https://devblogs.microsoft.com/semantic-kernel/planning-with-semantic-kernel-using-automatic-function-calling/


## Parallel Function Calling Support Models:
https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling

- gpt-35-turbo (1106)
- gpt-35-turbo (0125)
- gpt-4 (1106-Preview)
- gpt-4 (0125-Preview)
- gpt-4 (vision-preview)
- gpt-4 (2024-04-09)
- gpt-4o (2024-05-13)
- gpt-4o-mini (2024-07-18)


