from helper_functions import print_llm_response
from task_list import get_llm_response
from IPython.display import Markdown, display

messages = [
    {"role": "system", "content": "You are an IT professional with over 30 years of experience."}
]


while True:
    user_input = input("\n>>: ")
    if user_input.lower() in ["conversation done", "done", "exit", "quit"]:
        print("Conversation ended.")
        break
    reply = get_llm_response(user_input)
    display(Markdown(f"\nAI: {reply}"))