import tkinter as tk
from tkinter import ttk


TITLEFONT =("Verdana", 35)

# binds all children to event
def bind_show_frame_to_children(widget, controller, target_page, button="<Button-1>"):
    widget.bind(button, lambda e: controller.show_frame(target_page))
    for child in widget.winfo_children():
            child.bind(button, lambda e: controller.show_frame(target_page))

# main window
class App(tk.Tk):
    def __init__(self, title, dimensions) -> None:
        super().__init__()
        self.title(title)

        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(dimensions[0], dimensions[1])


        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        container.pack()

        semList = GUI_SemesterList(container, self)
        self.show_frame(semList)


    def show_frame(self, frame):
        frame.tkraise()



class GUI_SemesterList(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        container = parent
        self.grid(row=0, column=0, sticky="nsew")
         
        title = tk.Label(self, text="Semesters", font=TITLEFONT, highlightbackground="black", highlightthickness=1)
        title.pack(side="top")

        self.semList = tk.Frame(self)
        self.GUI_sem_list = [GUI_Semester(self, controller, container, self.semList, "sem 1", 20),
                             GUI_Semester(self, controller, container, self.semList, "sem 2", 20)]

        for sem in self.GUI_sem_list:
            sem.pack(side="top", pady=10)
        
        self.semList.pack(fill=None, expand=False)




class GUI_Semester(tk.Frame):
    def __init__(self, parent, controller, container, list_container, name, average):
        tk.Frame.__init__(self, list_container)

        self.name = name
        self.avg = average
        self.screen = parent

        sem_name = tk.Label(self, text=self.name, font=("Arial", 25), padx=10)
        sem_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=("Arial", 20), padx=10)

        sem_name.pack(side="left")
        sem_grade.pack(side="right")

        bind_show_frame_to_children(self, controller, GUI_CourseList(self, controller, container))

        self.config(cursor="openhand")
        


class GUI_CourseList(tk.Frame):
    def __init__(self, parent, controller, container):
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew")
        
        title = ttk.Label(self, text=parent.name, font=TITLEFONT)
        title.pack()
  
        
        semesters_btn = ttk.Button(self, text ="Go back",
                            command = lambda : controller.show_frame(parent.screen))
     
        semesters_btn.pack()



class GUI_GradeList(tk.Frame):
    def __init__(self, parent, controller, container):
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text=parent.name, font=TITLEFONT)
        title.pack()
  
        courses_btn = ttk.Button(self, text ="Go back",
                            command = lambda : controller.show_frame(GUI_CourseList))
     
        courses_btn.pack()



if __name__ == "__main__":
    app = App("test", (600, 600))
    app.mainloop()