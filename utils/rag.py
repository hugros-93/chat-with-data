import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate


DATA_PATH = "data/"
CHROMA_PATH = "chroma/"
OPEN_AI_KEY = os.environ.get("OPENAI_KEY")

EMBEDDING = OpenAIEmbeddings(openai_api_key=OPEN_AI_KEY)


class DocStore:

    def __init__(self) -> None:
        self.data_path = DATA_PATH
        self.chroma_path = CHROMA_PATH
        self.embedding = EMBEDDING

    def load(self):
        loader = DirectoryLoader(
            self.data_path,
            glob="*.pdf",
            show_progress=True,
            use_multithreading=False,
            loader_cls=PyPDFLoader,
        )
        docs = loader.load()
        self.docs = docs
        print(f"> {len(self.docs)} document loaded.")

    def split(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=250,
            length_function=len,
            add_start_index=True,
        )
        self.splits = text_splitter.split_documents(self.docs)
        print(f"> {len(self.splits)} splits created.")

    def create_vector_db(self):
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)

        db = Chroma.from_documents(
            self.splits, self.embedding, persist_directory=self.chroma_path
        )

        db.persist()
        print(f"> Vector DB created ('{self.chroma_path}')")


class DocSearch:
    def __init__(self) -> None:
        self.chroma_path = CHROMA_PATH
        self.embedding = EMBEDDING
        self.openai_key = os.environ.get("OPENAI_KEY")
        self.db = Chroma(
            persist_directory=self.chroma_path, embedding_function=self.embedding
        )

    def get_results(self, question_string, k, thresold):
        if k == None:
            k = len(self.db.get()['ids'])
        results = self.db.similarity_search_with_relevance_scores(question_string, k=k)
        if thresold == None:
            thresold = 0.0
        if len(results) == 0:
            raise Exception("No results.")
        else:
            results = [x for x in results if x[1] >= thresold]
            if len(results) == 0:
                raise Exception("No results satisfying thresold.")
            else:
                return results

    def get_prompt(self, question_string, results):
        context_string = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

        PROMPT_TEMPLATE = """
        Answer the question by writing a quick summary based only on the following context:

        {context}


        ---
        Answer the question by writing a quick summary based on the above context: {question}
        """

        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_string, question=question_string
        )
        return prompt

    def get_answer(self, prompt):
        model = ChatOpenAI(api_key=self.openai_key)
        answer = model.invoke(prompt)
        return answer.content

    def ask(self, question, k=None, thresold=None):
        results = self.get_results(question, k, thresold)
        prompt = self.get_prompt(question, results)
        answer = self.get_answer(prompt)
        references = [
            {
                "score": r[1],
                "source": r[0].metadata["source"],
                "page": r[0].metadata["page"],
                "text": r[0].page_content,
            }
            for r in results
        ]
        return answer, references


if __name__ == "__main__":
    # Create store
    store = DocStore()
    store.load()
    store.split()
    store.create_vector_db()

    # Show of split
    split_example = store.splits[10]
    print("Example of split:")
    print(split_example.page_content)
    print(split_example.metadata)
