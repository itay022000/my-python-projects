import sys
import os
import numpy as np

from questions_v2 import (
    open_ended_questions,
    multiple_choice_questions,
    true_or_false_questions,
)

def play_game():
    """
    Run a single game session.
    """
    print("Welcome to the Trivia Game... more specifically, to the second version of it!")
    print("\nYou'll be asked some very interesting questions of multiple kinds...")
    print("\nGood luck!\n")

    open_ended_results = np.array([], dtype=int)
    multiple_choice_results = np.array([], dtype=int)
    true_or_false_results = np.array([], dtype=int)

    question_index = 1
    
    print("For open-ended questions, type your answer... Here we go!\n")
    
    shuffled_indices = np.random.permutation(10)
    
    for idx in shuffled_indices:
        question = open_ended_questions[idx]
        print(f"Question {question_index}:")
        print(question.get("question"))
        answer = input("My answer: ")
        correct_answer = question.get("answer", "")
        
        if answer.strip().lower() == correct_answer.strip().lower():
            print("And you are... correct!")
            open_ended_results = np.append(open_ended_results, 1)
        else:
            print("And you are... wrong...")
            print(f"The correct answer is {correct_answer}")
            open_ended_results = np.append(open_ended_results, 0)
        
        current_score = np.sum(open_ended_results)
        print(f"Your current score is {current_score} out of 10\n")
        question_index += 1
    
    total_correct = np.sum(open_ended_results)
    percentage = total_correct * 10
    print(f"You answered {total_correct} out of 10 questions correctly ({percentage}%).")
    
    conditional_feedback = np.where(total_correct > 7, "awesome!", np.where(total_correct > 4, "not bad", ", um... oh well"))
    print(f"You were {conditional_feedback}")
    
    print("\nFor multiple choice questions, enter the number of your choice... and GO!\n")
    
    shuffled_indices = np.random.permutation(10)
    for idx in shuffled_indices:
        question = multiple_choice_questions[idx]
        print(f"Question {question_index}:")
        print(question.get("question"))
        options = question.get("options", [])
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
        correct_answer_index = question.get("correct")
        
        if answer_index == correct_answer_index:
            print("And you are... correct!")
            multiple_choice_results = np.append(multiple_choice_results, 1)
        else:
            print("And you are... wrong...")
            correct_answer_number = correct_answer_index + 1
            correct_answer_text = options[correct_answer_index]
            print(f"The correct answer is {correct_answer_number}. {correct_answer_text}")
            multiple_choice_results = np.append(multiple_choice_results, 0)
        
        current_score = np.sum(multiple_choice_results)
        print(f"Your current score is {current_score} out of 10\n")
        question_index += 1
    
    total_correct = np.sum(multiple_choice_results)
    percentage = total_correct * 10
    print(f"You answered {total_correct} out of 10 questions correctly ({percentage}%).")

    conditional_feedback = np.where(total_correct > 7, "fantastic!", np.where(total_correct > 4, "pretty good", "... what can I say?"))
    print(f"You were {conditional_feedback}")
    
    print("\nFor true or false questions, answer with 'true'/'t' or 'false'/'f'... And Voilà!\n")
    
    shuffled_indices = np.random.permutation(10)
    for idx in shuffled_indices:
        question = true_or_false_questions[idx]
        print(f"Question {question_index}:")
        print(question.get("question"))
        
        validate = True
        while validate:
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
        
        correct_answer = question.get("answer", "")
        if answer == correct_answer.strip().lower():
            print("And you are... correct!")
            true_or_false_results = np.append(true_or_false_results, 1)
        else:
            print("And you are... wrong...")
            print(f"It is actually {correct_answer}")
            true_or_false_results = np.append(true_or_false_results, 0)
        
        current_score = np.sum(true_or_false_results)
        print(f"Your current score is {current_score} out of 10\n")
        question_index += 1
    
    total_correct = np.sum(true_or_false_results)
    percentage = total_correct * 10
    print(f"You answered {total_correct} out of 10 questions correctly ({percentage}%).")

    conditional_feedback = np.where(total_correct > 7, "insane!", np.where(total_correct > 4, "quite alright", "... god help us..."))
    print(f"You were {conditional_feedback}")

    all_results = np.concatenate([open_ended_results, multiple_choice_results, true_or_false_results])
    total_score = np.sum(all_results)

    print(f"Your total score is {total_score} out of 30 questions ({(total_score / 30 * 100):.2f}%).")

    print("This version is certainly more interesting than the last one... but there's more to come!")
    print("And again, thank you for playing!")


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