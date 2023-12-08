from .utilities import completion, search

def slooth_bot(topic):
    "Generate research questions based on a topic"
    questions = completion(
        system="You are a research assistant, create research questions for the topics and ideas provided.",
        user=f"Write research questions about the following: \n{topic}"
        )
    results = search.run(questions)
    return results
# - Fact check the information
# - if check is passed
#     - Submit research summary with sources
# - else if check is failed repeat

if __name__ == '__main__':
    pass
