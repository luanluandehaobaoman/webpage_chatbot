import os
from langchain.document_loaders import SeleniumURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Setup Chrome Driver, may need to change based on system
service = Service("/usr/bin/chromedriver")
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)


def load_html_text(url):
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    texts = text_splitter.split_documents(data)

    return texts


def embed_text(texts, save_loc):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = FAISS.from_documents(texts, embeddings)

    docsearch.save_local(save_loc)


def embedding(url_list) -> None:
    """
    Purpose:
        Ingest data into a a local db
    Args:
        url_list (list): A list of URLs
    Returns:
        N/A
    """

    for url in url_list:
        # Get the raw html text
        texts = load_html_text(url)

        # Save embeddings to local_index
        embed_text(texts, "local_index")

if __name__ == "__main__":
    # Single Wikipedia page URL
    url = "https://zh.wikipedia.org/wiki/2023%E5%B9%B4%E4%B8%96%E7%95%8C%E4%B8%80%E7%BA%A7%E6%96%B9%E7%A8%8B%E5%BC%8F%E9%94%A6%E6%A0%87%E8%B5%9B"
    url1="https://aws.amazon.com/cn/blogs/machine-learning/how-medidata-used-amazon-sagemaker-asynchronous-inference-to-accelerate-ml-inference-predictions-up-to-30-times-faster/"
    url2= "https://docs.aws.amazon.com/zh_cn/sagemaker/latest/dg/serverless-endpoints.html"
    embedding([url1,url2])
