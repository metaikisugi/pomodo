import tkinter as tk
import os

WORK_MIN = 25
SHORT_BREAK_MIN = 5

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("ポモドーロタイマー")
        self.root.geometry("400x300")
        
        # 背景色なども少し見やすく
        self.root.configure(bg="#f0f0f0")

        self.timer_id = None
        self.is_running = False
        self.is_work_time = True
        self.time_left = WORK_MIN * 60

        # UI設定 (expand=True, fill='both' で画面いっぱいに広がるように設定)
        self.title_label = tk.Label(text="作業 (25分) - 準備完了", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        self.title_label.pack(expand=True, fill='both')

        self.time_label = tk.Label(text="25:00", font=("Helvetica", 60, "bold"), bg="#f0f0f0")
        self.time_label.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        # フォントサイズを動的に変更するためのバインド
        self.root.bind('<Configure>', self.resize_font)

        self.start_button = tk.Button(self.button_frame, text="開始", command=self.start_timer, width=8, font=("Helvetica", 12))
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(self.button_frame, text="一時停止", command=self.pause_timer, width=8, font=("Helvetica", 12))
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="リセット", command=self.reset_timer, width=8, font=("Helvetica", 12))
        self.reset_button.grid(row=0, column=2, padx=10)

    def resize_font(self, event):
        # ウィンドウのリサイズイベントにのみ反応
        if event.widget == self.root:
            w = event.width
            h = event.height
            
            # ウィンドウサイズに応じてフォントサイズを計算
            time_size = max(20, min(w // 4, h // 3))
            title_size = max(10, min(w // 15, h // 10))
            
            self.time_label.config(font=("Helvetica", time_size, "bold"))
            self.title_label.config(font=("Helvetica", title_size, "bold"))

    def update_timer_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.title_label.config(text="作業 (25分)" if self.is_work_time else "休憩 (5分)")
            self.count_down()

    def pause_timer(self):
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def reset_timer(self):
        self.pause_timer()
        self.is_work_time = True
        self.time_left = WORK_MIN * 60
        self.title_label.config(text="作業 (25分) - 準備完了", fg="black")
        self.root.configure(bg="#f0f0f0")
        self.title_label.config(bg="#f0f0f0")
        self.time_label.config(bg="#f0f0f0")
        self.button_frame.config(bg="#f0f0f0")
        self.update_timer_display()

    def play_sound(self):
        # OSにあわせてシステム音を鳴らす
        if os.name == 'nt':
            # Windowsの場合
            import winsound
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        else:
            # Mac/Linuxの場合（必要に応じてベルを鳴らす）
            self.root.bell()

    def count_down(self):
        if not self.is_running:
            return

        self.update_timer_display()

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.count_down)
        else:
            # 状態を切り替えてループする
            self.is_work_time = not self.is_work_time
            
            # ウィンドウを最前面に持ってきて音を鳴らす
            self.root.attributes('-topmost', True)
            self.play_sound()
            self.root.attributes('-topmost', False)
            
            if self.is_work_time:
                self.title_label.config(text="作業 (25分)", fg="black", bg="#f0f0f0")
                self.root.configure(bg="#f0f0f0")
                self.time_label.config(bg="#f0f0f0")
                self.button_frame.config(bg="#f0f0f0")
                self.time_left = WORK_MIN * 60
            else:
                self.title_label.config(text="休憩 (5分)", fg="#004d00", bg="#e6ffe6")
                self.root.configure(bg="#e6ffe6")
                self.time_label.config(bg="#e6ffe6")
                self.button_frame.config(bg="#e6ffe6")
                self.time_left = SHORT_BREAK_MIN * 60
                
            self.update_timer_display()
            # 次のカウントダウンを自動で開始（ループ）
            self.timer_id = self.root.after(1000, self.count_down)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
