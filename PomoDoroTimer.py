import tkinter as tk
from tkinter import messagebox
import time
import winsound

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("300x300")
        self.master.config(bg="#E5E5E5")
        self.master.iconbitmap('C:\\Users\\baeum\\Documents\\dev\\PomodoroTimer\\icon.ico')  # Pfad zum ICO-Bild hinzufügen

        self.work_duration = tk.IntVar(value=25)
        self.break_duration = tk.IntVar(value=5)

        self.timer_label = tk.Label(self.master, text="25:00", font=("Helvetica", 48), bg="#E5E5E5")
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer, bg="#1E90FF", fg="white", font=("Helvetica", 12))
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer, state=tk.DISABLED, bg="#1E90FF", fg="white", font=("Helvetica", 12))
        self.pause_button.pack(pady=5)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_timer, bg="#1E90FF", fg="white", font=("Helvetica", 12))
        self.reset_button.pack(pady=5)

        self.is_running = False
        self.is_pause = False
        self.remaining_time = 0

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.is_pause = False
            self.work_duration_minutes = self.work_duration.get() * 60
            self.break_duration_minutes = self.break_duration.get() * 60

            if self.remaining_time == 0:
                self.remaining_time = self.work_duration_minutes

            self.update_timer()
            self.start_button.pack_forget()  # Start-Button wird ausgeblendet
            self.reset_button.config(state=tk.DISABLED)
            self.work_duration_entry.config(state=tk.DISABLED)
            self.break_duration_entry.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL, text="Pause")

    def pause_timer(self):
        if self.is_running:
            self.is_pause = not self.is_pause
            if self.is_pause:
                self.pause_button.config(text="Weiter")
            else:
                self.pause_button.config(text="Pause")
                self.update_timer()

    def stop_timer(self):
        self.is_running = False
        self.is_pause = False
        self.remaining_time = 0
        self.start_button.pack()  # Start-Button wird wieder angezeigt
        self.pause_button.config(text="Pause")
        self.reset_button.config(state=tk.NORMAL)
        self.work_duration_entry.config(state=tk.NORMAL)
        self.break_duration_entry.config(state=tk.NORMAL)

    def update_timer(self):
        if self.is_running and not self.is_pause:
            if self.remaining_time == 0:
                self.is_running = False
                self.remaining_time = self.break_duration_minutes if self.remaining_time == self.work_duration_minutes else self.work_duration_minutes
                self.timer_label.config(text=self.format_time(self.remaining_time))
                self.play_sound()  # Sound am Ende der Arbeitsphase
                messagebox.showinfo("Pomodoro Timer", "Pomodoro session completed!")  # Anzeige der Meldung am Ende der Arbeitsphase
                self.stop_timer()
                return

            self.timer_label.config(text=self.format_time(self.remaining_time))
            self.remaining_time -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.stop_timer()

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def reset_timer(self):
        self.stop_timer()
        self.timer_label.config(text=self.format_time(self.work_duration.get() * 60))
        self.remaining_time = 0

    def play_sound(self):
        # Hier den Code einfügen, um den Sound am Ende der Arbeitsphase abzuspielen.
        pass

if __name__ == "__main__":
    root = tk.Tk()
    timer = PomodoroTimer(root)
    timer.work_duration_entry = tk.Entry(root, textvariable=timer.work_duration, width=5, font=("Helvetica", 12))
    timer.work_duration_entry.pack(pady=10)

    timer.break_duration_entry = tk.Entry(root, textvariable=timer.break_duration, width=5, font=("Helvetica", 12))
    timer.break_duration_entry.pack(pady=10)

    root.mainloop()


