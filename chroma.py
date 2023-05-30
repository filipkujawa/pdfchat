import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import hashlib
from rich import print


class Chroma:
    def __init__(self, api_key: str, collection_name: str, reset: bool):
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet", persist_directory=".chroma_persist"
            )
        )
        self.collection_name = collection_name

        if reset:
            self.client.reset()

        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key, model_name="text-embedding-ada-002"
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.openai_ef,
            metadata={"hnsw:space": "cosine"},
        )
        self.client.persist()

    def query(self, text: str, count=5):
        return self.collection.query(query_texts=[text], n_results=count)

    def add(self, doc, console):
        # Check for duplicates
        result = self.collection.get(ids=[self.generateID(doc)])

        if len(result["documents"]) > 0:
            console.print("[bold yellow]Duplicate document detected. Skipping")
            return
        else:
            console.print("[bold green]New document detected. Adding")
            self.collection.add(documents=[doc], ids=self.generateID(doc))

    # Takes a paragraph of text as input and returns a unique ID using the SHA-256 hashing algorithm.

    def generateID(self, text) -> str:
        encoded_text = text.encode("utf-8")
        hash_object = hashlib.sha256(encoded_text)
        unique_id = hash_object.hexdigest()
        return unique_id
