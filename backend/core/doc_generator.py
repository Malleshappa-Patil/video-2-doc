import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini model for generation. 
# gemini-1.5-flash is extremely fast and cost-effective for MVP tasks.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

def generate_documentation(chunks: list[str]) -> str:
    """
    Generates structured markdown documentation from the text chunks.
    For an MVP, we will do a map-reduce style combination: summarize chunks, then combine.
    """
    print("Generating documentation with Gemini...")
    
    prompt_template = PromptTemplate.from_template(
        """
        You are an expert educational technical writer. 
        Convert the following video transcript chunk into highly structured, clear markdown notes.
        Include headings, bullet points, and highlight key concepts.
        If there is code or technical terms, format them properly.
        
        Transcript Chunk:
        {text}
        
        Structured Notes:
        """
    )
    
    chain = prompt_template | llm
    
    doc_sections = []
    # Process each chunk and generate a section of notes
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        response = chain.invoke({"text": chunk})
        doc_sections.append(response.content)
        
    # Merge all generated sections into a final document
    final_documentation = "\n\n---\n\n".join(doc_sections)
    
    # Optional: You could run one more prompt here to create a "Table of Contents" 
    # or an "Executive Summary" of the final_documentation.
    
    return final_documentation