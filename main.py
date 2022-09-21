import os
from tkinter import *
from random import *
import pandas
import tkinter.messagebox

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
current_language = ''

try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_df = pandas.read_csv("data/french_words.csv")
    words_dict = original_df.to_dict(orient='records')
else:
    words_dict = df.to_dict(orient='records')


# --------------------- CREATE NEW FLASHCARDS ------------------------- #
def pick_word():

    if len(words_dict) > 0:
        global current_card, current_language, flip_timer
        window.after_cancel(flip_timer)
        # What teacher did
        current_card = choice(words_dict)
        current_language = choice(list(current_card.keys()))
        random_word = current_card.get(current_language)

        # What I did before knowing about the 'orient'
        # words_dict = df.to_dict()
        # random_language = choice(list(words_dict))
        # random_number = randint(0, len(words_dict[random_language]))
        # random_word = words_dict[random_language][random_number]

        canvas.itemconfig(canvas_word, text=random_word, fill='black')
        canvas.itemconfig(canvas_language, text=current_language, fill='black')
        canvas.itemconfig(canvas_image, image=front_card)
        flip_timer = window.after(3000, func=flip_card)
    else:
        canvas.itemconfig(canvas_image, image=back_card)
        canvas.itemconfig(canvas_language, text='Congrats!!!', fill='white')
        canvas.itemconfig(canvas_word, text='You have learned all the words', font=('Courier', 25, 'bold'), fill='white')
        os.remove('data/words_to_learn.csv')
        right_button.config(state='disabled')
        wrong_button.config(state='disabled')
        window.after_cancel(flip_timer)



def flip_card():
    if current_language == 'French':
        other_language = 'English'
    elif current_language == 'English':
        other_language = 'French'
    canvas.itemconfig(canvas_language, text=other_language, fill='white')
    canvas.itemconfig(canvas_word, text=current_card[other_language], fill='white')
    canvas.itemconfig(canvas_image, image=back_card)


def is_known():
    words_dict.remove(current_card)
    print(len(words_dict))
    data = pandas.DataFrame(words_dict)
    data.to_csv('data/words_to_learn.csv', index=False)

    pick_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file='images/card_front.png')
canvas_image = canvas.create_image(400, 263, image=front_card)
back_card = PhotoImage(file='images/card_back.png')
canvas_language = canvas.create_text(400, 150, text='Title', fill='black', font=('Arial', 40, 'italic'))
canvas_word = canvas.create_text(400, 263, text='test', fill='black', font=('Arial', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_button_image = PhotoImage(file='./images/wrong.png')
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=pick_word)
wrong_button.grid(column=0, row=1)

right_button_image = PhotoImage(file='./images/right.png')
right_button = Button(image=right_button_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

pick_word()

window.mainloop()

