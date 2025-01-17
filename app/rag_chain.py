import asyncio
import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

from config import PG_COLLECTION_NAME
from langchain_openai import OpenAIEmbeddings

load_dotenv()

vector_store = PGVector(
    collection_name=PG_COLLECTION_NAME,
    connection_string=os.getenv("POSTGRES_URL"),
    embedding_function=OpenAIEmbeddings()
)

template = """
Answer given the following context:
{context}

Question: {question}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", streaming=True)


class RagInput(TypedDict):
    question: str


# final_chain = (
#         RunnableParallel(
#             context=(itemgetter("question") | vector_store.as_retriever()),
#             question=itemgetter("question")
#         ) |
#         RunnableParallel(
#             answer=(ANSWER_PROMPT | llm),
#             docs=itemgetter("context")
#         )
#
# ).with_types(input_type=RagInput)

final_chain = (
        {
            "context": itemgetter("question") | vector_store.as_retriever(),
            "question": itemgetter("question")
        }
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
).with_types(input_type=RagInput)
