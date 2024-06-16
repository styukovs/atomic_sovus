from dataclasses import dataclass
from typing import List

from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from atomic_sovus.retrievers import load_faiss_retriever
from atomic_sovus.settings import EMBED_MODEL_ID, N_DOCS_FAQ, N_DOCS_MANUAL

embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID, model_kwargs={"device": "cpu"})
retriever_manual = load_faiss_retriever("vectorstores/manual/faiss_index", embedding_model, {"k": N_DOCS_MANUAL})
retriever_faq = load_faiss_retriever("vectorstores/faq/faiss_index", embedding_model, {"k": N_DOCS_FAQ})


@dataclass
class RelevantManual:
    filename: str
    titlename: str
    docname: str
    page: int


@dataclass
class RelevantFAQ:
    question: str
    answer: str


def get_relevant_manuals(question: str) -> List[RelevantManual]:
    retrieved_docs = retriever_manual.invoke(question)

    relevant_manuals: List[RelevantManual] = []
    for retrieved_doc in retrieved_docs:
        filename = retrieved_doc.metadata["filename"]
        titlename = retrieved_doc.metadata["titlename"]
        docname = retrieved_doc.metadata["docname"]
        page = retrieved_doc.metadata["page"]
        relevant_manual = RelevantManual(filename=filename, titlename=titlename, docname=docname, page=page)
        relevant_manuals.append(relevant_manual)

    return relevant_manuals


def get_relevant_faq(question: str) -> List[RelevantFAQ]:
    retrieved_docs = retriever_faq.invoke(question)

    relevant_manuals: List[RelevantFAQ] = []
    for retrieved_doc in retrieved_docs:
        question_faq = retrieved_doc.page_content
        answer_faq = retrieved_doc.metadata["answer"]
        relevant_manual = RelevantFAQ(question=question_faq, answer=answer_faq)
        relevant_manuals.append(relevant_manual)

    return relevant_manuals
