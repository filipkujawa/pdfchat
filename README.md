# PDF CHAT

A CLI Application to interact with PDF's semantically, primarily a demo app
built to learn llm and embedding fundamentals. 

Built with using:

 - [LangChain](https://github.com/hwchase17/langchain)
 - [Chroma](https://github.com/chroma-core/chroma)
 - [OpenAI](https://openai.com/)
 - [Rich](https://github.com/Textualize/rich)
 - [Python](https://github.com/python)


## Usage Guide

Step 1. Clone the repository 

    git clone https://github.com/filipkujawa/pdfchat.git

Step 2. Install requirements 

    cd pdfchat
    pip install -r requirements.txt

Step 3. Add API Key to config
Open `config.ini` and add an api key to the `open_ai_api_key` property.
You can obtain an api key [here](https://platform.openai.com/account/api-keys).

Step 4. Run the program


    py chat.py

And follow the instructions given. 

#### Flags
Usage: `chat.py [OPTIONS]`

| Options   | Description |
|--|--|
|`--path TEXT`|Path to the pdf|
|`--clear_db BOOLEAN`  | Clear the chroma db |
|`--chunk_size INTEGER`|Text splitter chunk size|
|`--max_tokens INTEGER`|LLM max token config|
|`--context_size INTEGER`|Number of documents to include in prompt context|

#### Prompt

The default prompt is
```
Given the following sections from a text, answer the question using only that information. 
If you are unsure and the answer is not explicitly written in the provided text, 
say 'Sorry, I don't know how to help with that'. Answer in Markdown. Context sections: {docs} Question: '''{question}'''
```

You can edit and experiment with the prompt by changing the value of `prompt` in `chat.py` following LangChain's `PromptTemplate` structure. 
