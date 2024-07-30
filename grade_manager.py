import tkinter as tk
from tkinter import ttk


TITLEFONT =("Verdana", 35)


# main window
class App(tk.Tk):
    def __init__(self, title, dimensions) -> None:
        super().__init__()
        self.title(title)

        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(dimensions[0], dimensions[1])


        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (GUI_SemesterList, GUI_CourseList, GUI_GradeList):
  
            frame = F(container, self)
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(GUI_SemesterList)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class GUI_SemesterList(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
         
        title = ttk.Label(self, text ="Semesters", font = TITLEFONT)
         
        title.grid(row = 0, column = 4, padx = 10, pady = 10) 
  
        courses_btn = ttk.Button(self, text ="Courses",
        command = lambda : controller.show_frame(GUI_CourseList))
     
        courses_btn.grid(row = 1, column = 1, padx = 10, pady = 10)



class GUI_CourseList(tk.Frame):
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        title = ttk.Label(self, text ="Courses", font = TITLEFONT)
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        
        semesters_btn = ttk.Button(self, text ="Go back",
                            command = lambda : controller.show_frame(GUI_SemesterList))
     
        semesters_btn.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        grades_btn = ttk.Button(self, text ="Grades",
                            command = lambda : controller.show_frame(GUI_GradeList))
     
        grades_btn.grid(row = 2, column = 1, padx = 10, pady = 10)



class GUI_GradeList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = ttk.Label(self, text ="Grades", font = TITLEFONT)
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        courses_btn = ttk.Button(self, text ="Go back",
                            command = lambda : controller.show_frame(GUI_CourseList))
     
        courses_btn.grid(row = 1, column = 1, padx = 10, pady = 10)



if __name__ == "__main__":
    app = App("test", (600, 600))
    app.mainloop()