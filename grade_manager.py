import tkinter as tk

class Course():
    def __init__(self, master, name) -> None:
        self.name = name
        frame = tk.Frame(master)
        frame.pack()

# main window
class App(tk.Tk):
    def __init__(self, title, dimensions) -> None:
        super().__init__()
        self.title(title)

        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(dimensions[0], dimensions[1])

        self.course_list = courseList(self)
        self.mainloop()

class courseList(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        tk.Label(self, background="grey").pack(expand=True, fill="both")
        self.place(x=parent.winfo_width(), y=0, relwidth=0.7, relheight=1)

        self.courses = []



if __name__ == "__main__":
    App("grade manager", (600, 600))