from rich import print
from rich.console import Console
from rich.markdown import Markdown
from util import clear, printLogo, handleApiKeyInput
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from time import sleep
from chroma import Chroma
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import configparser
import click


@click.command()
@click.option('--path', default="", help="Path to the pdf")
@click.option('--clear_db', default=False, help="Clear the chroma db")
@click.option('--chunk_size', default=1000, help="Text splitter chunk size")
@click.option('--max_tokens', default=512, help="LLM max token config")
@click.option('--context_size', default=5, help="Number of documents to include in prompt context")
def main(path, clear_db, chunk_size, max_tokens, context_size):
    console = Console()
    config = configparser.ConfigParser()
    config.read("config.ini")

    clear()
    printLogo()

    if path == "":
        # Choose a PDF to interact with if flag not set
        console.print("\n\nEnter the path to the pdf: ", style="bold white")
        pdfPath = input()
        if pdfPath == "":
            pdfPath = "bitcoin.pdf"
        clear()

    else:
        pdfPath = path

    # Load PDF
    with console.status("[bold blue]Loading PDF...", spinner_style="bold blue") as status:
        loader = PyPDFLoader(pdfPath)
        pages = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=0)
        docs = text_splitter.split_documents(pages)
        sleep(1)

    console.print("[bold blue]Loaded [bold white]", len(
        pages), "[bold blue]  pages.", highlight=False)
    console.print("[bold blue]Loaded [bold white]", len(
        docs), "[bold blue] docs.", highlight=False)

    if config.get("keys", "open_ai_api_key", fallback=-1) == -1 or config.get("keys", "open_ai_api_key", fallback=-1) == "":
        OPENAI_API_KEY = handleApiKeyInput(console)
    else:
        OPENAI_API_KEY = config.get("keys", "open_ai_api_key")

    cc = Chroma(OPENAI_API_KEY, pdfPath, clear_db)

    with console.status("[bold blue]Working on tasks...", spinner_style="bold blue") as status:
        for doc in docs:
            cc.add(doc.page_content, console)

    llm = OpenAI(openai_api_key=OPENAI_API_KEY, max_tokens=max_tokens)
    prompt = PromptTemplate(
        input_variables=["docs", "question"],
        template="""Given the following sections from a text, answer the question using only that information. 
        If you are unsure and the answer is not explicitly written in the provided text, 
        say 'Sorry, I don't know how to help with that'. Answer in Markdown. Context sections: {docs} Question: '''{question}'''"""
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    clear()
    printLogo()
    console.print(
        "Embeddings have been generated, you can now interact with the pdf\n\n", style="bold blue")
    while True:

        console.print(
            "\n\n\n[bold white]Ask a question or type [bold blue]'S'[bold white] for stats & more info", highlight=False)
        question = input("Question: ")

        if question == 'S':
            console.print('\n\n---\nCount: ',
                          cc.collection.count(), "\n---\n\n\n")
        else:
            console.print("[bold blue]Answer: ")
            with console.status("[bold white] Thinking...", spinner="pong", spinner_style="bold white") as status:
                console.print(Markdown(chain.run({
                    'docs': cc.query(question, context_size),
                    'question': question
                })), style="bold white")


if __name__ == "__main__":
    main()
