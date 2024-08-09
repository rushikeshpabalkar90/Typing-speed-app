from tkinter import Tk, Text, END, WORD, Label
from pynput import keyboard
import math
from contents import content_dict
import random

content = random.choice(list(content_dict.values()))


letter_index = 0
incorrect_letters = 0
time_sec = 60
timer = ''

num_pad_keys = {
    '<96>': '0', '<97>': '1', '<98>': '2', '<99>': '3', '<100>': '4',
    '<101>': '5', '<102>': '6', '<103>': '7', '<104>': '8', '<105>': '9'
     }


# ---------------------------- Countdown mechanism -------------------------------#
def count_down(count):
    global timer, time_sec

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_text.config(text=f"Timer {count_min}:{count_sec}")

    if count > 0:
        time_sec -= 1
        timer = window.after(1000, count_down, count - 1)
    else:
        window.after_cancel(timer)
        listener.stop()
        calculate(count, incorrect_letters, letter_index)


# ---------------------------- Give response on Keyboard event -------------------------------#
def on_release(key):
    global letter_index, incorrect_letters, timer

    # getting numpad keys
    if str(key) in num_pad_keys:
        key = f"'{num_pad_keys[str(key)]}'"

    # start countdown
    if letter_index == 0:
        count_down(time_sec)

    # deal with backspace key
    if key == keyboard.Key.backspace:
        try:
            if paragraph.tag_names(f'1.{letter_index - 1}')[0] == 'wrong':
                incorrect_letters -= 1
        except IndexError:
            pass

        # remove tag from text
        paragraph.tag_remove('correct', f'1.{letter_index - 1}', f'1.{letter_index}')
        paragraph.tag_remove('wrong', f'1.{letter_index - 1}', f'1.{letter_index}')

        if letter_index > 0:
            letter_index -= 1

    # deal with shift key
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
        pass

    # deal with space key
    elif key == keyboard.Key.space:
        key = "' '"
        if str(key) == f"'{content[letter_index]}'":
            pass

        # if user key is ' ' and our letter is not ' '
        elif str(key) == "' '" and f"'{content[letter_index]}'" != ' ':
            paragraph.tag_add('wrong', f'1.{letter_index}', f'1.{letter_index + 1}')
            paragraph.tag_configure('wrong', underline=True, foreground='red')
            incorrect_letters += 1
        letter_index += 1

    # if user press correct key
    elif str(key) == f"'{content[letter_index]}'" or str(key) == f'"{content[letter_index]}"':
        paragraph.tag_add('correct', f'1.{letter_index}', f'1.{letter_index + 1}')
        paragraph.tag_config("correct", foreground="green")
        letter_index += 1

    # if user don't press correct key
    elif str(key) != f"'{content[letter_index]}'":
        paragraph.tag_add('wrong', f'1.{letter_index}', f'1.{letter_index + 1}')
        paragraph.tag_config("wrong", foreground="red", underline=True)
        incorrect_letters += 1

        letter_index += 1

    # End of string
    if letter_index >= len(content):
        window.after_cancel(timer)
        listener.stop()
        calculate(time_sec, incorrect_letters, letter_index)
        # window.destroy()


# --------------------------------- Typing Speed Calculator ----------------------------------#
def calculate(time_taken, incorrect, index):

    accuracy = (index - incorrect) / index * 100

    total_word = (index / 5)
    total_time = ((60 - (time_taken + 1)) / 60)
    wpm = total_word / total_time

    accuracy_label.config(text=f"Accuracy: \n\n{round(accuracy)}%")
    WPM_label.config(text=f"Word Per Minute: \n\n{round(wpm)}")
    total_incorrect_letter.config(text=f'Incorrect letters typed: \n\n{incorrect}')


# --------------------------------- UI ----------------------------------#


window = Tk()
window.title('Typing Speed Test')
window.config(height=800, bg="#dfdfdf", pady=40)

timer_text = Label(text='Timer 00:00', font=('Arial', 15, 'bold'), bg='#dfdfdf', fg='black')
timer_text.grid(pady=30, row=0, column=0, columnspan=3)

paragraph = Text(
    width=50,
    height=round(len(content) / 70),
    font=("Product Sans", 13),
    relief='flat',
    wrap=WORD,
    padx=80,
    pady=30
)

paragraph.insert(END, content)
paragraph.grid(padx=60, pady=10, column=0, row=1, columnspan=3)
paragraph.config(state='disabled')

accuracy_label = Label(text="Accuracy: ", font=('Arial', 12), bg='#dfdfdf', fg='black')
accuracy_label.grid(pady=60, column=0, row=2)

WPM_label = Label(text="Word Per Minute: ", font=('Arial', 12), bg='#dfdfdf', fg='black')
WPM_label.grid(column=1, row=2)

total_incorrect_letter = Label(text="Incorrect letters typed: ", font=('Arial', 12), bg='#dfdfdf', fg='black')
total_incorrect_letter.grid(column=2, row=2)

# listener for key enter
listener = keyboard.Listener(on_release=on_release)
listener.start()

window.mainloop()
