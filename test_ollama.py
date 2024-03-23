from langchain_community.llms.ollama import Ollama

llm = Ollama(model="llama2:chat")

output = llm.stream("Where is Ha Noi? More details.")
for chuck in output:
    print(chuck, flush=True, end="")