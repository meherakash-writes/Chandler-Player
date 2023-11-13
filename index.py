import tkinter as tk
from tkinter import *
import vlc
from tkinter import filedialog
from datetime import timedelta

class ChandlerPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chandler's Player")
        self.geometry("500x500")      
        self.configure(bg="black")         
        self.cplayer_init()
        
    def cplayer_init(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.current_file = None
        self.playing_video = False
        self.video_paused = False 
        #self.iconbitmap("assets/icon.ico")
        self.cplayer_widgets()  

    def cplayer_widgets(self):        
        self.media_canvas = tk.Canvas(self, bg="black", width=500, height=100)
        self.media_canvas.pack(pady=5, fill=tk.BOTH, expand=True)  
        self.select_file_button = tk.Button(
            self,
            text="I'll   be   there   for   you",
            font=("Gabriel Weiss' Friends Font", 11),
            fg="white",
            bg="black",
            command=self.select_file,
        )
        self.progress_bar = CplayerProgressBar(
        self, self.set_video_position, bg="black", highlightthickness=0.7
        )
        self.progress_bar.pack(fill=tk.X, padx=0, pady=0)

        self.control_buttons_frame = tk.Frame(self, bg="black")
        self.control_buttons_frame.pack(pady=5)
        self.select_file_button.pack(pady=5)
        self.play_button = tk.Button(
            self.control_buttons_frame,
            text="P. l. a. y",
            font=("Gabriel Weiss' Friends Font", 9),
            bg="black",
            fg="#F44336",
            command=self.play_video,
        )
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.pause_button = tk.Button(
            self.control_buttons_frame,
            text="P. a. u. s. e",
            font=("Gabriel Weiss' Friends Font", 9),
            bg="black",
            fg="#2196F3",
            command=self.pause_video,
        )
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.stop_button = tk.Button(
            self.control_buttons_frame,
            text="S. t. o. p",
            font=("Gabriel Weiss' Friends Font", 9),
            bg="black",
            fg="#FF9800",
            command=self.stop,
        )
        self.stop_button.pack(side=tk.LEFT, pady=5)
        self.fast_forward_button = tk.Button(
            self.control_buttons_frame,
            text="F. o. r. w. a. r. d",
            font=("Gabriel Weiss' Friends Font", 9),
            bg="black",
            fg="#F44336",
            command=self.fast_forward,
        )
        self.fast_forward_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.rewind_button = tk.Button(
            self.control_buttons_frame,
            text="R. e. w. i. n. d",
            font=("Gabriel Weiss' Friends Font", 9),
            bg="black",
            fg="#FF9800",
            command=self.rewind,
        )
        self.rewind_button.pack(side=tk.LEFT, pady=5)        

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Media Files", "*.mp4 *.avi *.mkv")]
        )
        if file_path:
            self.current_file = file_path
            #self.time_label.config(text="00:00:00 / " + self.get_duration_str())
            self.play_video()

    def get_duration_str(self):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
            return total_duration_str
        return "00:00:00"

    def play_video(self):
        if not self.playing_video:
            media = self.instance.media_new(self.current_file)
            self.media_player.set_media(media)
            self.media_player.set_hwnd(self.media_canvas.winfo_id())
            self.media_player.play()
            self.playing_video = True

    def fast_forward(self):
        if self.playing_video:
            current_time = self.media_player.get_time() + 10000
            self.media_player.set_time(current_time)

    def rewind(self):
        if self.playing_video:
            current_time = self.media_player.get_time() - 10000
            self.media_player.set_time(current_time)

    def pause_video(self):
        if self.playing_video:
            if self.video_paused:
                self.media_player.play()
                self.video_paused = False
                self.pause_button.config(text="Pause")
            else:
                self.media_player.pause()
                self.video_paused = True
                self.pause_button.config(text="Resume")

    def stop(self):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False
        #self.time_label.config(text="00:00:00 / " + self.get_duration_str())

    def set_video_position(self, value):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            position = int((float(value) / 100) * total_duration)
            self.media_player.set_time(position)

    def update_video_progress(self):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            current_time = self.media_player.get_time()
            progress_percentage = (current_time / total_duration) * 100
            self.progress_bar.set(progress_percentage)
            #current_time_str = str(timedelta(milliseconds=current_time))[:-3]
            #total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
            #self.time_label.config(text=f"{current_time_str} / {total_duration_str}")
        self.after(1000, self.update_video_progress)


class CplayerProgressBar(tk.Scale):
    def __init__(self, master, command, **kwargs):
        kwargs["showvalue"] = False
        super().__init__(
            master,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=800,
            command=command, 
            bd=0,  
            width=10,                  
            **kwargs,
        )
        self.bind("<Button-1>", self.on_click)  

    def on_click(self, event):
        if self.cget("state") == tk.NORMAL:
            value = (event.x / self.winfo_width()) * 100
            self.set(value)


if __name__ == "__main__":
    app = ChandlerPlayer()
    app.update_video_progress()
    app.mainloop()