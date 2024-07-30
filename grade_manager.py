import tkinter as tk
import utils


def bind_children_to_click(widget, callback, button="<Button-1>"):
    """Bind all children of a widget to the click event."""
    widget.bind("<Button-1>", callback)
    for child in widget.winfo_children():
        bind_children_to_click(child, callback, button)


# main window
class App(tk.Tk):
    def __init__(self, title, dimensions) -> None:
        super().__init__()
        self.title(title)

        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(dimensions[0], dimensions[1])

        # load data
        sem_list = utils.load_semesters("courses")
        for sem in sem_list:
            for course in sem.courses:
                course.calc_adjusted_weighted_avg()
            sem.calc_avg()

        GUI_sem_list = GUI_SemesterList(self, sem_list)
        GUI_sem_list.pack(expand=True, fill='both')
        
        self.mainloop()


class GUI_SemesterList(tk.Frame):
    def __init__(self, parent, sem_list=[]) -> None:
        super().__init__(parent, highlightbackground="black", highlightthickness=1)
        self.sem_list = sem_list
        
        title = tk.Label(self, text="Semesters", font=("Arial", 40), highlightbackground="black", highlightthickness=1)
        title.pack(side="top")
        semList = tk.Frame(self, highlightbackground="black", highlightthickness=1)

        self.GUI_sem_list = []

        for sem in self.sem_list:
            self.GUI_sem_list.append(GUI_Semester(semList, sem.name, sem.calc_avg()))
        for sem in self.GUI_sem_list:
            sem.pack(side="top", pady=10)
        

        semList.pack(fill=None, expand=False)
                

class GUI_Semester(tk.Frame):
    def __init__(self, parent, name, average) -> None:
        super().__init__(parent, highlightbackground="black", highlightthickness=1)
        self.name = name
        self.avg = average
        
        sem_name = tk.Label(self, text=self.name, font=("Arial", 25), padx=10)
        sem_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=("Arial", 20), padx=10)

        sem_name.pack(side="left")
        sem_grade.pack(side="right")
        

        bind_children_to_click(self, self.foo)
        self.config(cursor="openhand")
    
    
    def foo(self, event):
        GUI_CourseList(self)
        print(self.name + " has been pressed")


class GUI_CourseList(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        l = tk.Label(self, text=parent.name)
        l.pack()
        
        self.tkraise()


class GUI_Course(tk.Frame):
    def __init__(self, parent, name, grade_list=[]) -> None:
        super().__init__(parent)
        self.name = name
        self.grades = grade_list 


class GUI_GradeList(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)


class GUI_Grade(tk.Frame):
    def __init__(self, parent, name, score=-1, weight=-1) -> None:
        super().__init__(parent)
        self.name = name
        self.score = score
        self.weight = weight


if __name__ == "__main__":
    App("test", (600, 600))