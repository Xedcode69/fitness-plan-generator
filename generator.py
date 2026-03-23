from dotenv import load_dotenv
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.prompts import PromptTemplate

load_dotenv()


def load_documents(text_folder):
    loader = DirectoryLoader(
        text_folder, "*.txt", loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )
    documents = loader.load()

    return documents


def chunk(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    return chunks


def embedding():
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")

    return embedding


def vectordb(chunks, embed):
    client = chromadb.Client()

    if "fitnessplan" not in client.list_collections():
        collection = client.create_collection(name="fitnessplan")

    vectors = embed.embed_documents([chunk.page_content for chunk in chunks])

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=[chunk.page_content for chunk in chunks],
        embeddings=vectors,
    )

    return collection


def retrieve(query, embed, collection):
    query_embed = embed.embed_query(query)

    result = collection.query(
        query_embeddings=[query_embed], n_results=5, include=["documents"]
    )

    return result["documents"][0]


def generate_prompt(result, name, age, gender, goal, equipment, weight, illnesses):

    context = "\n".join(result)

    template = """
            You are a certified fitness coach.

            Given the following user details:
            name: {name}
            age: {age}
            gender: {gender}
            goal: {goal}
            equipment: {equipment}
            weight: {weight}
            illnesses: {illnesses}
            
            Use the following knowledge:{context} 
            generate: 
            1. Weekly workout plan
            2. Exercise instructions
            3. Rest days
            4. Safety tips
            """

    prompt_template = PromptTemplate.from_template(template=template)

    prompt = prompt_template.format(
        name=name,
        age=age,
        gender=gender,
        goal=goal,
        equipment=equipment,
        weight=weight,
        illnesses=illnesses,
        context=context,
    )

    return prompt


def generate_response(prompt):
    agent = ChatOpenAI(model="gpt-4o-mini")

    response = agent.invoke(prompt)
    return response
