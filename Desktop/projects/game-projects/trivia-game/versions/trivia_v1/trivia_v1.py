import sys
import random
from questions_v1 import (
    open_ended_questions,
    multiple_choice_questions,
    true_or_false_questions,
)

def play_game():
    """
    Run a single game session.
    """
    print("Welcome to the Trivia Game!")
    print("\nYou'll be asked some very interesting questions of multiple kinds...")
    print("\nGood luck!\n")

    open_ended_score = 0
    multiple_choice_score = 0
    true_or_false_score = 0
    question_index = 1
    
    shuffled_open_ended = open_ended_questions.copy()
    random.shuffle(shuffled_open_ended)
    
    print("For open-ended questions, type your answer... Here we go!\n")
    for open_question in shuffled_open_ended:
        print(f"Question {question_index}:")
        print(open_question.get("question"))
        answer = input("My answer: ")
        correct_answer = open_question.get("answer", "")
        if answer.strip().lower() == correct_answer.strip().lower():
            print("And you are... correct!")
            open_ended_score += 1
        else:
           print("And you are... wrong...") 
           print(f"The correct answer is {correct_answer}")
        print(f"Your current score is {open_ended_score} out of 10\n")
        question_index += 1

    print(f"You answered {open_ended_score} out of 10 questions correctly.")
    if open_ended_score > 7:
        print("That is awesome!\n")
    elif open_ended_score > 4:
        print("That's not bad.\n")
    else:
        print("That's... oh, well...\n")

    print("For multiple choice questions, enter the number of your choice... and GO!\n")
    
    shuffled_multiple_choice = multiple_choice_questions.copy()
    random.shuffle(shuffled_multiple_choice)

    for multiple_choice_question in shuffled_multiple_choice:
        print(f"Question {question_index}:")
        print(multiple_choice_question.get("question"))
        options = multiple_choice_question.get("options", [])
        for i, option in enumerate(options, start=1):
            print(f"  {i}. {option}")
        validate = True
        while validate:
            answer = input("My answer: ")
            try:
                answer = int(answer)
                if answer >= 1 and answer <= 4:
                    validate = False
                else:
                    print("That's not a valid answer...")
            except:
                print("That's not a valid answer...")
        answer_index = answer - 1
        correct_answer_index = multiple_choice_question.get("correct")
        if answer_index == correct_answer_index:
            print("And you are... correct!")
            multiple_choice_score += 1
        else:
           print("And you are... wrong...") 
           correct_answer_number = correct_answer_index + 1
           correct_answer_text = options[correct_answer_index]
           print(f"The correct answer is {correct_answer_number}. {correct_answer_text}")
        print(f"Your current score is {multiple_choice_score} out of 10\n")
        question_index += 1

    print(f"You answered {multiple_choice_score} out of 10 questions correctly.")
    if multiple_choice_score > 7:
        print("That is fantastic!\n")
    elif multiple_choice_score > 4:
        print("That's pretty nice.\n")
    else:
        print("That's... what can I say?\n")


    shuffled_true_or_false = true_or_false_questions.copy()
    random.shuffle(shuffled_true_or_false)
    
    print("For true or false questions, answer with 'true'/'t' or 'false'/'f'... And Voilà!\n")
    for true_or_false_question in shuffled_true_or_false:
        print(f"Question {question_index}:")
        print(true_or_false_question.get("question"))
        validate = True
        while validate == True:
            answer = input("My answer: ").strip().lower()
            if answer in ['true', 'false', 't', 'f']:
                validate = False
                # Convert shortcuts to full words
                if answer == 't':
                    answer = 'true'
                elif answer == 'f':
                    answer = 'false'
            else:
                print("That's not a valid answer...")
        correct_answer = true_or_false_question.get("answer", "")
        if answer == correct_answer.strip().lower():
            print("And you are... correct!")
            true_or_false_score += 1
        else:
           print("And you are... wrong...") 
           print(f"It is actually {correct_answer}")
        print(f"Your current score is {true_or_false_score} out of 10\n")
        question_index += 1

    print(f"You answered {true_or_false_score} out of 10 questions correctly.")
    if true_or_false_score > 7:
        print("That is insane!\n")
    elif true_or_false_score > 4:
        print("That's quite alright.\n")
    else:
        print("That's... god help us...\n")


    total_score = open_ended_score + multiple_choice_score + true_or_false_score
    print(f"Your total score is {total_score} out of 30 questions.")
    print(f"That is {(total_score / 30 * 100):.2f}% of the questions.")
    print("This is just the beginning with this game... Thank you for playing!")


def main():
    """
    Main game loop with play again option.
    """
    while True:
        play_game()
        
        # Ask if user wants to play again
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
            if play_again in ["yes", "y", "no", "n"]:
                break
            print("Invalid choice. Please enter 'yes' or 'no'.")
        
        if play_again in ["no", "n"]:
            print("\nWe'll talk later! 👋")
            break
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()