from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from backend.core.vector_store import get_vector_store
from dotenv import load_dotenv

load_dotenv()

# We can use flash here as well for fast, conversational responses
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

def ask_chatbot(collection_name: str, query: str) -> str:
    """
    RAG pipeline: Retrieves relevant chunks from ChromaDB and answers the user's question.
    """
    print(f"Querying ChromaDB collection '{collection_name}' for: {query}")
    vector_db = get_vector_store(collection_name)
    
    # Retrieve top 4 most relevant chunks to keep the context window focused
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(query)
    
    # Combine the retrieved chunks into a single context string
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = PromptTemplate.from_template(
        """
        You are a highly capable AI assistant. Answer the user's question using ONLY the provided video transcript context.
        If the answer is not contained within the context, politely state: "I don't have enough information from the video to answer that."
        Do not hallucinate or use outside knowledge.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({"context": context, "query": query})
    
    return response.content