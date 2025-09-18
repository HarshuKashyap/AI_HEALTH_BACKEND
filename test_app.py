from ai_logic import get_answer

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    answer = get_answer(user_input)
    print("AI:\n" + answer)
