from langchain_huggingface import HuggingFaceEmbeddings

from atomic_sovus.settings import EMBED_MODEL_ID


def download_embeddings() -> None:
    HuggingFaceEmbeddings(
        model_name=EMBED_MODEL_ID,
        model_kwargs={"device": "cpu"},
    )


if __name__ == "__main__":
    download_embeddings()
