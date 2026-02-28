# ensemble_retriever.py
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from typing import List, Optional
from collections import defaultdict

class EnsembleRetriever(BaseRetriever):
    retrievers: List[BaseRetriever]
    weights: List[float] = None
    c: int = 60
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, retrievers: List[BaseRetriever], weights: Optional[List[float]] = None, c: int = 60, **kwargs):
        if weights is None:
            weights = [1.0] * len(retrievers)
        super().__init__(retrievers=retrievers, weights=weights, c=c, **kwargs)
    
    def _get_relevant_documents(self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None) -> List[Document]:
        doc_lists = []
        for retriever in self.retrievers:
            # FIXED: Use invoke() instead of get_relevant_documents()
            docs = retriever.invoke(query)
            doc_lists.append(docs)
        
        doc_scores = defaultdict(float)
        doc_map = {}
        
        for doc_list, weight in zip(doc_lists, self.weights):
            for rank, doc in enumerate(doc_list):
                doc_key = hash(doc.page_content)
                doc_scores[doc_key] += weight / (self.c + rank)
                if doc_key not in doc_map:
                    doc_map[doc_key] = doc
        
        sorted_doc_keys = sorted(doc_scores.keys(), key=lambda k: doc_scores[k], reverse=True)
        return [doc_map[key] for key in sorted_doc_keys]
    
    async def _aget_relevant_documents(self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None) -> List[Document]:
        return self._get_relevant_documents(query, run_manager=run_manager)
