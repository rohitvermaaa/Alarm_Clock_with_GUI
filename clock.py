import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()

alarm_set = False
alarm_time = None

blink_color = "red"

def update_clock():
    global blink_color
    while True:
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%A, %B %d, %Y')
        clock_label.config(text=current_time, font=("Helvetica", 48), bg="black", fg="white")
        date_label.config(text=current_date, font=("Helvetica", 16), bg="black", fg="white")
        if alarm_set and alarm_time:
            time_left = time_until_alarm(current_time, alarm_time)
            if time_left == "Time to wake up!":
                time_left_label.config(fg="red")
            else:
                if time_left <= "00:00:30":
                    if blink_color == "red":
                        blink_color = "black"
                    else:
                        blink_color = "red"
                    time_left_label.config(fg=blink_color)
                else:
                    blink_color = "black" 
                time_left_label.config(text=time_left, font=("Helvetica", 16), bg="black", fg=blink_color)
        else:
            time_left_label.config(text="No alarm is set", font=("Helvetica", 16), bg="black", fg="white")
        time.sleep(1)

def set_alarm():
    global alarm_set, alarm_time
    selected_hour = hour_combobox.get()
    selected_minute = minute_combobox.get()
    alarm_time = f"{selected_hour}:{selected_minute}"
    try:
        alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        if alarm_hour < current_hour or (alarm_hour == current_hour and alarm_minute <= current_minute):
            alarm_time = f'{alarm_hour + 24:02}:{alarm_minute:02}'
        alarm_set = True
        alarm_thread = threading.Thread(target=wait_for_alarm, args=(alarm_time,))
        alarm_thread.start()
        stop_button.config(state="normal")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please select a valid time.")



def wait_for_alarm(alarm_time):
    while True:
        current_time = time.strftime('%H:%M')
        if current_time == alarm_time:
            play_alarm_sound()
            break
        time.sleep(1)

def play_alarm_sound():
    pygame.mixer.music.load('alram_sound.mp3')
    pygame.mixer.music.play()
    result = messagebox.showinfo("Alarm", "Time to wake up!")
    if result == "ok":
        stop_alarm()

def stop_alarm():
    global alarm_set, alarm_time
    alarm_set = False
    alarm_time = None
    pygame.mixer.music.stop()
    time_left_label.config(text="No alarm is set", font=("Helvetica", 16))
    stop_button.config(state="disabled")

def time_until_alarm(current_time, alarm_time):
    current_hour, current_minute, current_second = map(int, current_time.split(':'))
    alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
    total_current_seconds = current_hour * 3600 + current_minute * 60 + current_second
    total_alarm_seconds = alarm_hour * 3600 + alarm_minute * 60
    time_left_seconds = total_alarm_seconds - total_current_seconds

    if time_left_seconds < 0:
        time_left_seconds += 24 * 3600

    hours_left, remainder = divmod(time_left_seconds, 3600)
    minutes_left, seconds_left = divmod(remainder, 60)

    return f"{hours_left} hours {minutes_left} minutes {seconds_left} seconds"

root = tk.Tk()
root.title("Alarm Clock")

root.attributes('-fullscreen', True)

bg_image = Image.open('bgimage.jpg')
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

custom_font = ("Helvetica", 30, "bold")
label = tk.Label(root, text="Set Alarm Time:", font=custom_font, bg='black', bd=0, fg='white')
label.place(relx=0.5, rely=0.45, anchor='center')

title_bar = tk.Frame(root, bg="black", relief="raised", borderwidth=1)
title_bar.pack(fill="x", side="top", anchor="n")

minimize_button = tk.Button(title_bar, text="_", bg="black", fg="white", bd=0, font=("Helvetica", 16),
                            command=root.iconify)
minimize_button.pack(side="left")

close_button = tk.Button(title_bar, text="X", bg="black", fg="white", bd=0, font=("Helvetica", 16),
                         command=root.destroy)
close_button.pack(side="right")

clock_thread = threading.Thread(target=update_clock)
clock_thread.daemon = True
clock_thread.start()

def handle_cursor(event):
    y = event.y_root
    if y <= 40:
        title_bar.pack(fill="x", side="top", anchor="n")
    else:
        title_bar.pack_forget()

root.bind("<Motion>", handle_cursor)

hour_values = [str(i).zfill(2) for i in range(24)]
minute_values = [str(i).zfill(2) for i in range(60)]

hour_label = tk.Label(root, text="Hours", font=("Helvetica", 20, "bold"), bg='black', fg='white')
hour_label.place(relx=0.38, rely=0.55, anchor='center')

hour_combobox = ttk.Combobox(root, values=hour_values, font=("Helvetica", 24), state="normal", width=4)
hour_combobox.set("00")
hour_combobox.place(relx=0.45, rely=0.55, anchor='center')

minute_label = tk.Label(root, text="Minutes", font=("Helvetica", 22, "bold"), bg='black', fg='white')
minute_label.place(relx=0.63, rely=0.55, anchor='center')

minute_combobox = ttk.Combobox(root, values=minute_values, font=("Helvetica", 24), state="normal", width=4)
minute_combobox.set("00")
minute_combobox.place(relx=0.55, rely=0.55, anchor='center')

clock_label = tk.Label(root, text="", font=("Helvetica", 24), bg="black", fg="white")
clock_label.place(relx=0.5, rely=0.25, anchor='center')

colon_label = tk.Label(root, text=":", font=("Helvetica", 24, "bold"), bg="black", fg="white")
colon_label.place(relx=0.5, rely=0.55, anchor='center')

date_label = tk.Label(root, text="", font=("Helvetica", 16), bg="black", fg="white")
date_label.place(relx=0.5, rely=0.35, anchor='center')

time_left_label = tk.Label(root, text="", font=("Helvetica", 16), bg="black", fg="white")
time_left_label.place(relx=0.5, rely=0.65, anchor='center')

button_style = ttk.Style()
button_style.configure("Beautiful.TButton", font=("Helvetica", 20, "bold"))
set_button = ttk.Button(root, text="Set Alarm", command=set_alarm, style="Beautiful.TButton")
set_button.place(relx=0.4, rely=0.75, anchor='center')

stop_button = ttk.Button(root, text="Stop Alarm", command=stop_alarm, style="Beautiful.TButton", state="disabled")
stop_button.place(relx=0.6, rely=0.75, anchor='center')

clock_thread = threading.Thread(target=update_clock)
clock_thread.daemon = True
clock_thread.start()

root.mainloop()
