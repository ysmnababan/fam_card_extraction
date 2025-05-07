import tkinter as tk

class ScreenUtils:
    @staticmethod
    def get_screen_size():
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height