from typing import Optional

from langchain_community.vectorstores.faiss import FAISS
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever


def load_faiss_retriever(
    path_to_vectorstore: str,
    embedding_model: Embeddings,
    dense_search_kwargs: Optional[dict] = None,
) -> VectorStoreRetriever:
    """Get the `faiss_retriever`.

    Parameters
    ----------
    path_to_vectorstore : str
        Path to the FAISS vectorstore.
    embedding_model : Embeddings
        Embedding model.
    dense_search_kwargs : Optional[dict] = None
        Search kwargs for the FAISS vectorstore retriever. Default is `{"k": 4}`.

    Returns
    -------
    retriever : VectorStoreRetriever
        FAISS vectorstore retriever.
    """
    dense_search_kwargs = dense_search_kwargs or {"k": 4}
    faiss_index = FAISS.load_local(
        folder_path=path_to_vectorstore,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True,
    )
    faiss_retriever = faiss_index.as_retriever(search_kwargs=dense_search_kwargs)
    return faiss_retriever
