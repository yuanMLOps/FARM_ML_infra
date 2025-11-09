from fastapi import Body, HTTPException
from .graph import graph_app
from .schemas import RAGRequest


async def get_generation(body: RAGRequest=Body(...)) -> dict:
    try:
        generation = await graph_app.ainvoke({"question": body.prompt})
        quality = generation.get("quality", {})
        return {
            "answer": generation.get("generation", ""),
            "hallucination_grade": quality.get("hallucination_grade", False),
            "relavant_grade": quality.get("relavant_grade", False),
            "num_orginial_documents": quality.get("num_document", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    # rag_content = await vector_service.search("knowledgebase", embed(body.prompt), 3, 0.7)
    # rag_content_str = "\n".join([c.payload["original_text"] for c in rag_content])

   