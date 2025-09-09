from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from DB.VectorDB import VectorDB
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

queryRouter = APIRouter( tags=["Query"] ,prefix="/query")   

class QueryRequest(BaseModel):
    query: str

@queryRouter.post("/")
async def query_data(request: QueryRequest):
    """
    Endpoint to query data from vector DB.
    """
    try:
        vector_db = VectorDB(persist_directory="../DB/vector_db")
        context = vector_db.query(request.query)

        llm = ChatOpenAI(model="gpt-4", temperature=0)
        # need to fix this template part
        template = ChatPromptTemplate(
         [
        ("system", "You are a helpful assistant that provides concise and accurate answers based on the provided context. if context is insufficient, say 'I don't know' do not make up information if its in context then only give the answer."),
        ("human", "{user_input}"),
        ]
)
        
        chain = template | llm
        response = chain.invoke(request={"user_input": request.query, "context": context})
        return {"status": "success", "data": response.choices[0].message.content, "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  