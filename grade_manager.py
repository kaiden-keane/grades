import tkinter as tk


TITLEFONT = ("Arial", 35)
ITEMNAMEFONT = ("Arial", 25)
ITEMDATAFONT = ("Arial", 20)

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

        semList = GUI_SemesterList(container, self, container)
        self.show_frame(semList)


    def show_frame(self, frame):
        frame.tkraise()



class GUI_SemesterList(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk, container: tk.Frame): 
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew")
         
        title = tk.Label(self, text="Semesters", font=TITLEFONT)

        self.semList = tk.Frame(self)
        self.GUI_sem_list = [GUI_Semester(self, controller, container, self.semList, "sem 1", 20),
                             GUI_Semester(self, controller, container, self.semList, "sem 2", 20)]

        # pack children
        title.pack(side="top")
        for sem in self.GUI_sem_list:
            sem.pack(side="top", pady=10)
        # pack self
        self.semList.pack(fill=None, expand=False)




class GUI_Semester(tk.Frame):
    def __init__(self, parent: GUI_SemesterList, controller: tk.Tk, container: tk.Frame, list_container: tk.Frame, name: str, average: float):
        tk.Frame.__init__(self, list_container, highlightbackground="black", highlightthickness=1)
        self.name = name
        self.avg = average
        self.screen = parent

        sem_name = tk.Label(self, text=self.name, font=ITEMNAMEFONT, padx=10)
        sem_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=ITEMDATAFONT, padx=10)

        sem_name.pack(side="left")
        sem_grade.pack(side="right")

        # set the children to bind to the same input as self
        course_list = GUI_CourseList(self, controller, container)
        self.bind("<Button-1>", lambda e: controller.show_frame(course_list))
        sem_name.bind("<Button-1>", lambda e: controller.show_frame(course_list))
        sem_grade.bind("<Button-1>", lambda e: controller.show_frame(course_list))

        self.config(cursor="openhand") # changes hand icon on hover
        


class GUI_CourseList(tk.Frame):
    def __init__(self, parent: GUI_Semester, controller: tk.Tk, container: tk.Frame):
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew")
        
        title = tk.Label(self, text=parent.name, font=TITLEFONT)
        
        back_btn = tk.Button(self, text="back", command=lambda : controller.show_frame(parent.screen))
        
        self.courseList = tk.Frame(self)
        self.GUI_course_list = [GUI_Course(self, controller, container, self.courseList, "course 1", 97.3234),
                             GUI_Course(self, controller, container, self.courseList, "course 2", 67.3)]

        # pack children
        title.pack(side="top")
        back_btn.pack()
        for course in self.GUI_course_list:
            course.pack(side="top", pady=10)
        
        # pack self
        self.courseList.pack(fill=None, expand=False)



class GUI_Course(tk.Frame):
    def __init__(self, parent: GUI_CourseList, controller: tk.Tk, container: tk.Frame, list_container: tk.Frame, name: str, average: float):
        tk.Frame.__init__(self, list_container, highlightbackground="black", highlightthickness=1)
        self.name = name
        self.avg = average
        self.screen = parent

        course_name = tk.Label(self, text=self.name, font=ITEMNAMEFONT, padx=10)
        course_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=ITEMDATAFONT, padx=10)

        course_name.pack(side="left")
        course_grade.pack(side="right")

        grade_list = GUI_GradeList(self, controller, container)
        self.bind("<Button-1>", lambda e: controller.show_frame(grade_list))
        course_name.bind("<Button-1>", lambda e: controller.show_frame(grade_list))
        course_grade.bind("<Button-1>", lambda e: controller.show_frame(grade_list))

        self.config(cursor="openhand")




class GUI_GradeList(tk.Frame):
    def __init__(self, parent: GUI_Course, controller: tk.Tk, container: tk.Frame):
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew")
        
        title = tk.Label(self, text=parent.name, font=TITLEFONT)
        back_btn = tk.Button(self, text="back", command=lambda : controller.show_frame(parent.screen))

        self.gradeList = tk.Frame(self)
        self.GUI_grade_list = [GUI_Grade(self, controller, container, self.gradeList, "grade 1", 34.3),
                             GUI_Grade(self, controller, container, self.gradeList, "grade 2", 53.0)]

        # pack children
        title.pack(side="top")
        back_btn.pack()
        for grade in self.GUI_grade_list:
            grade.pack(side="top", pady=10)
        
        # pack self
        self.gradeList.pack(fill=None, expand=False)

  


class GUI_Grade(tk.Frame):
    def __init__(self, parent: GUI_CourseList, controller: tk.Tk, container: tk.Frame, list_container: tk.Frame, name: str, average: float):
        tk.Frame.__init__(self, list_container, highlightbackground="black", highlightthickness=1)
        self.name = name
        self.avg = average
        self.screen = parent

        course_name = tk.Label(self, text=self.name, font=ITEMNAMEFONT, padx=10)
        course_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=ITEMDATAFONT, padx=10)

        course_name.pack(side="left")
        course_grade.pack(side="right")




if __name__ == "__main__":
    app = App("test", (600, 600))
    app.mainloop()