from langchain_huggingface import HuggingFaceEmbeddings


def download_embeddings() -> None:
    HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": "cpu"},
    )


if __name__ == "__main__":
    download_embeddings()
