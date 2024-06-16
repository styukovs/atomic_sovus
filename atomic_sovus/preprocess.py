import re
from copy import deepcopy
from typing import List

from langchain_core.documents import Document


def remove_closing_whitespaces(text: str) -> str:
    return re.sub(r"(^[ \t]+)|([ \t]+$)", "", text, flags=re.MULTILINE)


def clean_extra_whitespaces(text: str) -> str:
    return re.sub(r"( {2,})|(\t+)", " ", text, flags=re.MULTILINE)


def filter_text_documents(docs: List[Document]) -> List[Document]:
    """Remove table documents and clean up document contents.

    Parameters
    ----------
    docs : List[Document]
        List of documents from `Unstructured loader`.

    Returns
    -------
    clean_narrative_documents : List[Document]
        Clean narrative documents.
    """
    text_idxs = [idx for idx, doc in enumerate(docs) if doc.metadata["category"] != "Table"]

    text_documents: List[Document] = []
    for idx in text_idxs:
        metadata = deepcopy(docs[idx].metadata)
        page_content = docs[idx].page_content

        page_content = clean_extra_whitespaces(page_content)
        page_content = remove_closing_whitespaces(page_content)
        page_content = page_content.replace("\xa0", " ")

        _doc = Document(page_content=page_content, metadata=metadata)
        text_documents.append(_doc)

    return text_documents
