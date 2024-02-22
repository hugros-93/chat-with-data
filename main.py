from rag import DocSearch

if __name__ == "__main__":
    search = DocSearch()
    question = input("> Question: ")
    answer, references = search.ask(question)
    print(f"\n> Answer: {answer}")
    print(f"\n> References:")
    for ref in references:
        text_sample = ref["text"].replace("\n", " ")[:100]
        print(
            f'>> "...{text_sample}..." (source: {ref["source"]}, page: {ref["page"]}, score: {ref["score"]})'
        )
