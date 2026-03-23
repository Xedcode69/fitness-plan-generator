from fastapi import FastAPI
from generator import (
    load_documents,
    chunk,
    embedding,
    vectordb,
    retrieve,
    generate_prompt,
    generate_response,
)


app = FastAPI()


@app.get("/getplan")
def get_plan(
    qry: str,
    name: str,
    age: int,
    gender: str,
    goal: str,
    equipment: str,
    weight: float,
    illnesses: str,
):

    docs = load_documents("text")
    chunks = chunk(docs)
    embed = embedding()
    collection = vectordb(chunks, embed)

    retrieved_data = retrieve(qry, embed, collection)

    prompt = generate_prompt(
        retrieved_data, name, age, gender, goal, equipment, weight, illnesses
    )

    response = generate_response(prompt)

    return {"response": response.content}
