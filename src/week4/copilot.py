import asyncio
import os
from typing import Tuple
import openai
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from langchain.document_loaders import AzureBlobStorageFileLoader
from langchain.text_splitter import CharacterTextSplitter
from semantic_kernel.connectors.search_engine import BingConnector
from semantic_kernel.planning import StepwisePlanner
from semantic_kernel.planning.stepwise_planner.stepwise_planner_config import (
    StepwisePlannerConfig,
)


openai.api_key = os.getenv("OPENAI_API_KEY")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

kernel = sk.Kernel()

kernel.add_chat_service("chat_completion", AzureChatCompletion("startping_deploymodel", azure_endpoint, azure_api_key))
kernel.add_text_embedding_generation_service("ada", AzureTextEmbedding("startping_embedding", azure_endpoint, azure_api_key))

kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
kernel.import_skill(sk.core_skills.TextMemorySkill())

# load txt file from azure storage
conn_str=os.getenv('AZURE_STORAGE_CONN_STR')

loader = AzureBlobStorageFileLoader(
    conn_str=conn_str,
    container="project",
    blob_name="wmt-20230430.txt",
)
documents = loader.load()

# split into chunks
text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)


async def load_semanticmemory(docs):
    memory_collection_name = "wmt10Q12023"
    print("Adding WalMart 2023 Quarter Report and their descriptions to a volatile Semantic Memory.");
    i = 0
    for entry, value in enumerate(docs):
        await kernel.memory.save_reference_async(
        collection=memory_collection_name,
        description=value.page_content,
        text=value.page_content,
        external_id=entry,
        external_source_name="wmt10Q12023"
        )


async def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # a parameter that controls the randomness or creativity of the generated text, examples are 0,1,0.5
    )
    return response.choices[0].message["content"]


class ChatGPTSearchEngineSkill:
    """
    A ChatGPT search engine skill.
    """
    from semantic_kernel.orchestration.sk_context import SKContext
    from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter

    def __init__(self, connector) -> None:
        self._connector = connector

    @sk_function(
        description="Performs a ChatGPT search on sector according to the Global Industry Classification Standard (GICS)", name="searchAsync"
    )
    @sk_function_context_parameter(
        name="query",
        description="The search query",
    )
    async def search_async(self, query: str, context: SKContext) -> str:
        query = query or context.variables.get("query")
        result = await self._connector(query)
        return result


class WebSearchEngineSkill:
    """
    A search engine skill.
    """
    from semantic_kernel.orchestration.sk_context import SKContext
    from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter

    def __init__(self, connector) -> None:
        self._connector = connector

    @sk_function(
        description="Performs NEGATIVE news web search for a given query", name="searchAsync"
    )
    @sk_function_context_parameter(
        name="query",
        description="The search query",
    )
    async def search_async(self, query: str, context: SKContext) -> str:
        query = query or context.variables.get("query")
        # print("debug {query}")
        result = await self._connector.search_async(query, num_results=5, offset=0)
        return str(result)


class VectorSearchEngineSkill:
    """
    A vector search engine skill.
    """
    from semantic_kernel.orchestration.sk_context import SKContext
    from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter

    @sk_function(
        description="find context relevent to Consolidated net income or \
            Rating agency for Long-term debt or \
            legal proceedings or \
            cash equivalents and restricted cash at end of period \
            ", name="searchAsync"
    )
    @sk_function_context_parameter(
        name="query",
        description="The search query",
    )
    async def search_async(self, query: str, context: SKContext) -> str:
        query = query or context.variables.get("query")
        ask = f"find context relevent to {query}"
        # print(f"debug query: {ask}")
        # msg= context.variables.get("query")
        # print(f"debug msg: {query}")

        memories = await kernel.memory.search_async(memory_collection_name, ask, limit=1, min_relevance_score=0.77)
        result = memories[0].description
        # print(memories[0].relevance)
        # print(f"debug: {result}")
        return result    
    

asyncio.run(load_semanticmemory(docs))

BING_API_KEY = os.getenv("BING_SEARCH_V7_SUBSCRIPTION_KEY")
connector = BingConnector(BING_API_KEY)

kernel.import_skill(VectorSearchEngineSkill(), skill_name="vectorsearch")
kernel.import_skill(WebSearchEngineSkill(connector), skill_name="websearch")
kernel.import_skill(ChatGPTSearchEngineSkill(get_completion), skill_name="chatgptsearch")

planner = StepwisePlanner(
    kernel, StepwisePlannerConfig(max_iterations=2, min_iteration_time_ms=1000)
)

async def execute_plan(ask):
    plan = planner.create_plan(goal=ask)

    # for step in plan._steps:
    #     print(step.description, ":", step._state.__dict__)

    result = await plan.invoke_async()
    print("===========================\n" + "Query: " + ask + "\n")
    print("===========================\n" + "Result: \n")
    print(result)
    print("===========================\n" + "Thoughts: \n")
    for index, step in enumerate(plan._steps):
        print("Step:", index)
        print("Description:",step.description)
        print("Function:", step.skill_name + "." + step._function.name)
        if len(step._outputs) > 0:
            print( "  Output:\n", str.replace(result[step._outputs[0]],"\n", "\n  "))
    print("============END===============\n\n")
    return result


questions = [
    "What is the sector of Walmart according to the Global Industry Classification Standard (GICS)?",
    # "Are there any negatives news about Walmart in last 12 months?",
    # "find context relevent to amount for {cash equivalents and restricted cash at end of period} as of April 30, 2023 ",
    # "find context relevent to amount for {Consolidated net income} as of April 30, 2023",
    # "find context relevent to information for {legal proceedings or certain regulatory matters}",
    # "find context relevent to Rating for {Rating agency for Long-term debt}",
]

for question in questions:
    result = asyncio.run(execute_plan(question))
    print(f"output==>: {result}")
