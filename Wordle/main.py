import random

guesses = 10
word_list = []
feedback_word = ["_", "_", "_", "_", "_"]
correct_letters = ""
incorrect_letters = ""

with open("words.txt", "r") as connection:
    content = connection.readlines()

for line in content:
    word_list.append(line.strip().lower())

random_word = random.choice(word_list)
user_input = ""

while guesses > 0:
    user_input = ""
    while len(user_input) != 5:
        user_input = input(f"Enter a 5 letter word as your guess? {guesses} guesses left...\n").lower()
        if len(user_input) != 5:
            print("That is not a 5 letter word,")

    guesses -= 1
    if user_input == random_word:
        break
    else:
        for index in range(0, 5):
            if user_input[index] == random_word[index]:
                feedback_word[index] = user_input[index]

        for letter in random_word:
            if letter in user_input:
                if letter not in correct_letters:
                    correct_letters += letter

        for letter in user_input:
            if letter not in random_word:
                if letter not in incorrect_letters:
                    incorrect_letters += letter

    print(f"{feedback_word}    (✅: {correct_letters}) (❌: {incorrect_letters})")

print(f"The word was {random_word}")
if user_input == random_word:
    print("Correct, you win!")
else:
    print("Game Over.")
