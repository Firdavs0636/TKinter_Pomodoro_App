from tkinter import *
from math import floor
import pygame.mixer
import os

# Initializes pyGame module
pygame.mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
SECOND = 1000
reps = 0
ticks = ''
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text='00:00')
    title_label.config(text='Timer', fg=GREEN)
    tick_label.config(text=ticks)
    reps = 0
    pygame.mixer.music.stop()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        countdown(long_break)
        title_label.config(text='BREAK', fg=RED)

        pygame.mixer.music.load('/Users/admin/PycharmProjects/TKinter_Pomodoro_App/Break_sounds/long_break.wav')
        pygame.mixer.music.play(loops=0)

    elif reps % 2 == 0:
        countdown(short_break)
        title_label.config(text='BREAK', fg=PINK)

        pygame.mixer.music.load('/Users/admin/PycharmProjects/TKinter_Pomodoro_App/Break_sounds/short_break.wav')
        pygame.mixer.music.play(loops=0)

    else:
        countdown(work_sec)
        title_label.config(text='WORK', fg=GREEN)

        pygame.mixer.music.load('/Users/admin/PycharmProjects/TKinter_Pomodoro_App/Sounds/birds_sound.mp3')
        pygame.mixer.music.play(loops=32)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(remainder):
    global ticks
    global timer
    count_min = floor(remainder / 60)
    count_sec = remainder % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'

    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    if remainder >= 0:
        timer = window.after(SECOND, countdown, remainder - 1)
    else:
        start_timer()
        if reps % 2 == 0:
            ticks += '️✔︎'
            tick_label.config(text=ticks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# Formatting Sound List
def list_box_event(event):
    name = sound_list.get(sound_list.curselection())
    pygame.mixer.music.load('/Users/admin/PycharmProjects/TKinter_Pomodoro_App/Sounds/' + name)
    pygame.mixer.music.play(loops=32)


sound_list = Listbox(height=3, width=12, bg=YELLOW, highlightthickness=0, borderwidth=0, selectbackground=PINK, font=(FONT_NAME, 11, 'italic'), relief=GROOVE)
sound_list.bind('<<ListboxSelect>>', list_box_event)
sound_list.grid(column=2, row=0)

# Takes all files from a given directory
os.chdir("/Users/admin/PycharmProjects/TKinter_Pomodoro_App/Sounds")
song_tracks = os.listdir()

# Loops through all files and inserts to a list
for track in song_tracks:
    sound_list.insert(END, track)

# Labels
title_label = Label(text='Timer', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

tick_label = Label(bg=YELLOW, fg=GREEN, font=22)
tick_label.grid(column=1, row=3)

# Buttons
start_bt = Button(text='Start', highlightthickness=0, bg=YELLOW, command=start_timer)
start_bt.grid(column=0, row=2)

reset_bt = Button(text='Reset', highlightthickness=0, bg='white', command=reset)
reset_bt.grid(column=2, row=2)

# Canvas for picture
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='/Users/admin/PycharmProjects/TKinter_Pomodoro_App/Pic/tomato.png')
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text='00:00', fill='white', font=(FONT_NAME, 35, 'bold'))
canvas.grid(column=1, row=1)

window.mainloop()
