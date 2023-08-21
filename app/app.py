import logging
import os

import chainlit as cl
import openai
from database import create_index
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFacePipeline
from llama_index import (GPTVectorStoreIndex, LLMPredictor, ServiceContext,
                         SimpleDirectoryReader, StorageContext,
                         load_index_from_storage)
from llama_index.callbacks.base import CallbackManager
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.query_engine.retriever_query_engine import \
    RetrieverQueryEngine
from llama_index.response.schema import Response, StreamingResponse
from llama_index.vector_stores import PGVectorStore
from psycopg2 import OperationalError

openai.api_key = os.environ.get("OPENAI_API_KEY")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
postgres_host = os.environ.get("POSTGRES_HOST")
postgres_db = os.environ.get("POSTGRES_DB")
postgres_user = os.environ.get("POSTGRES_USER")

STREAMING = True

logging.info("Run started...")
required_exts = [".md", ".txt", ".html"]
documents = SimpleDirectoryReader("./data", required_exts=required_exts, recursive=False).load_data()
logging.info(f"Loaded {len(documents)} documents")
try:
    index = create_index(
        database=postgres_db,
        host=postgres_host,
        password=postgres_password,
        port=5432,
        user=postgres_user,
        table_name="data",
        documents=documents
    )
    index.vector_store.query
except OperationalError:
    logging.error("Error connecting to PostgreSQL. Ensure the service is running and the connection details are correct.")
except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")

@cl.on_chat_start
async def factory():
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            streaming=STREAMING,
        ),
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        chunk_size=512,
        callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]),
    )

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=STREAMING,
    )

    cl.user_session.set("query_engine", query_engine)


@cl.on_message
async def main(message):
    query_engine = cl.user_session.get("query_engine")  # type: RetrieverQueryEngine
    response = await cl.make_async(query_engine.query)(message)

    response_message = cl.Message(content="")

    if isinstance(response, Response):
        response_message.content = str(response)
        await response_message.send()
    elif isinstance(response, StreamingResponse):
        gen = response.response_gen
        for token in gen:
            await response_message.stream_token(token=token)

        if response.response_txt:
            response_message.content = response.response_txt

        await response_message.send()