from .config import config
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.callbacks import AsyncIteratorCallbackHandler


class Gpt:
    def __init__(self) -> None:
        print(config.ollama_model)
        print(f"{config.ollama_host}:{config.ollama_port}")

        # Initialize embedding
        embedding = HuggingFaceEmbeddings(cache_folder="./modal")
        # Initialize chroma persistentClient
        db = Chroma(
            collection_name="sql-wiki",
            embedding_function=embedding,
            persist_directory="./chroma",
        )

        # Define vector store db as retriever
        retriever = db.as_retriever(
            search_type="similarity",  # similarity, mmr
            search_kwargs={"k": 3},
        )

        # Initialize callback
        self.callback = AsyncIteratorCallbackHandler()

        # Define llm
        llm = Ollama(
            model=config.ollama_model,
            base_url=f"{config.ollama_host}:{config.ollama_port}",
            timeout=3000,
            temperature=0,
            callbacks=[self.callback],
        )

        # Define prompt template for llm
        template = """You are an assistant for question-answering tasks. 
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Keep the answer as concise as possible.
        Always say "thanks for asking!" at the end of the answer.

        {context}

        Question: {question}

        Helpful Answer: """
        custom_prompt = PromptTemplate.from_template(template=template)

        # Form LLM Retrieval QA chain
        self.chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
            chain_type_kwargs={"prompt": custom_prompt},
        )

    # Return llm callback function
    def callback(self):
        return self.callback

    # Form LLM chain
    async def query(self, question: str):
        return await self.chain.ainvoke({"query": question})