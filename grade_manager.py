import tkinter as tk


TITLEFONT = ("Arial", 35)
ITEMNAMEFONT = ("Arial", 25)
ITEMDATAFONT = ("Arial", 20)


# main window
class App(tk.Tk):
    def __init__(self, title, dimensions) -> None:
        super().__init__()
        self.title(title) # set the title of the window

        # set the size of the window
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(dimensions[0], dimensions[1])

        # container that holds all the frames that are switched between
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        container.pack()

        gui_semester_list = SemesterList(container, self, container)
        self.show_frame(gui_semester_list)


    def show_frame(self, frame):
        frame.tkraise()



class SemesterList(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: App, container: tk.Frame): 
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew") # position inside container
        
        self.parent = parent
        self.controller = controller
        self.container = container
        
        self.semesters = [] # list of all semesters (type Semester)
        self.gui_semester_list = tk.Frame(self) # GUI containing all the semesters

        title = tk.Label(self, text="Semesters", font=TITLEFONT) # title of page

        # button at bottom for adding new semester
        self.add_btn = tk.Button(self.gui_semester_list, text="click to add new semester", command=self.add)
        self.add_btn.config(cursor="openhand")

        # pack children
        title.pack(side="top")
        self.pack_semesters()
        # pack self
        self.gui_semester_list.pack(fill=None, expand=False)
        
    
    def add(self):
        self.semesters.append(Semester(self, self.controller, self.container, self.gui_semester_list, "added sem", 999))
        self.pack_semesters()
        self.controller.show_frame(self)

    
    def remove(self, item):
        print(item)
        for i in range(len(self.semesters)):
            print(self.semesters[i])
            if item is self.semesters[i]:
                self.semesters[i].destroy()
                self.semesters.pop(i)
                break
        
        self.pack_semesters()
        self.controller.show_frame(self)
    

    def pack_semesters(self):
        for sem in self.semesters:
            sem.pack(side="top", pady=10)
        self.add_btn.pack(side="bottom", pady=10)



class Semester(tk.Frame):
    def __init__(self, parent: SemesterList, controller: tk.Tk, container: tk.Frame, list_container: tk.Frame, name: str, average: float):
        tk.Frame.__init__(self, list_container, highlightbackground="black", highlightthickness=1)
        self.parent = parent
        self.controller = controller
        self.container = container
        
        self.name = name
        self.avg = average
        self.screen = parent
        self.courses = []

        sem_name = tk.Label(self, text=self.name, font=ITEMNAMEFONT, padx=10)
        sem_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=ITEMDATAFONT, padx=10)

        sem_name.pack(side="left")
        sem_grade.pack(side="left")

        # set the children to bind to the same input as self
        gui_course_list = CourseList(self, controller, container)
        self.bind("<Button-1>", lambda e: controller.show_frame(gui_course_list))
        sem_name.bind("<Button-1>", lambda e: controller.show_frame(gui_course_list))
        sem_grade.bind("<Button-1>", lambda e: controller.show_frame(gui_course_list))

        # button to delete semester
        self.del_btn = tk.Button(self, text="delete", command=self.delete)
        self.del_btn.config(cursor="openhand")
        self.del_btn.pack(side="left")

        self.config(cursor="openhand") # changes hand icon on hover
    

    def delete(self):
        self.parent.remove(self)
        


class CourseList(tk.Frame):
    def __init__(self, parent: Semester, controller: tk.Tk, container: tk.Frame):
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew") # position inside container
        
        self.parent = parent
        self.controller = controller
        self.container = container
        
        self.courses = parent.courses # list of all courses (type Course)
        self.gui_course_list = tk.Frame(self) # GUI container for course list
        
        title = tk.Label(self, text=parent.name, font=TITLEFONT)
        
        # button at bottom for adding new course
        self.add_btn = tk.Button(self.gui_course_list, text="click to add new course", command=self.add)
        self.add_btn.config(cursor="openhand")

        # button at top to go to previous page
        self.back_btn = tk.Button(self, text="back", command=lambda : controller.show_frame(self.parent.screen))
        self.back_btn.config(cursor="openhand")
        
        # pack children
        title.pack(side="top")
        self.back_btn.pack()
        self.pack_courses()
        # pack self
        self.gui_course_list.pack(fill=None, expand=False)
        
    
    def add(self):
        self.courses.append(Course(self, self.controller, self.container, self.gui_course_list, "added course", 32.54))
        self.pack_courses()
        self.controller.show_frame(self)
    

    def remove(self, item):
        print(item)
        for i in range(len(self.courses)):
            print(self.courses[i])
            if item is self.scourses[i]:
                self.courses[i].destroy()
                self.courses.pop(i)
                break
        
        self.pack_semesters()
        self.controller.show_frame(self)
    

    def pack_courses(self):
        for course in self.courses:
            course.pack(side="top", pady=10)
        self.add_btn.pack(side="bottom", pady=10)



class Course(tk.Frame):
    def __init__(self, parent: CourseList, controller: tk.Tk, container: tk.Frame, list_container: tk.Frame, name: str, average: float):
        tk.Frame.__init__(self, list_container, highlightbackground="black", highlightthickness=1)
        self.parent = parent
        self.controller = controller
        self.container = container
        
        self.name = name
        self.avg = average
        self.screen = parent
        self.grades = []

        course_name = tk.Label(self, text=self.name, font=ITEMNAMEFONT, padx=10)
        course_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=ITEMDATAFONT, padx=10)

        course_name.pack(side="left")
        course_grade.pack(side="left")

        # set the children to bind to the same input as self
        gui_grade_list = GradeList(self, controller, container)
        self.bind("<Button-1>", lambda e: controller.show_frame(gui_grade_list))
        course_name.bind("<Button-1>", lambda e: controller.show_frame(gui_grade_list))
        course_grade.bind("<Button-1>", lambda e: controller.show_frame(gui_grade_list))

        # button to delete course
        self.del_btn = tk.Button(self, text="delete", command=self.delete)
        self.del_btn.config(cursor="openhand")
        self.del_btn.pack(side="left")

        self.config(cursor="openhand") # changes hand icon on hover
    

    def delete(self):
        self.parent.remove(self)



class GradeList(tk.Frame):
    def __init__(self, parent: Course, controller: tk.Tk, container: tk.Frame):
        tk.Frame.__init__(self, container)
        self.grid(row=0, column=0, sticky="nsew") # position inside container
        
        self.parent = parent
        self.controller = controller
        self.container = container

        self.grades = parent.grades # list of all grades (typ Grade)
        self.gui_grade_list = tk.Frame(self) # GUI container for grade list

        title = tk.Label(self, text=parent.name, font=TITLEFONT)
        
        # button at bottom for adding new course
        self.add_btn = tk.Button(self.gui_grade_list, text="click to add new grade", command=self.add)
        self.add_btn.config(cursor="openhand")
        
        # button at top to go to previous page
        self.back_btn = tk.Button(self, text="back", command=lambda : controller.show_frame(parent.screen))
        self.back_btn.config(cursor="openhand")

        # pack children
        title.pack(side="top")
        self.back_btn.pack()
        self.pack_grades()
        # pack self
        self.gui_grade_list.pack(fill=None, expand=False)
        
    
    def add(self):
        self.grades.append(Grade(self, self.controller, self.container, self.gui_grade_list, "added grade", 543.54))
        self.pack_grades()
        self.controller.show_frame(self)
    

    def remove(self, item):
        print(item)
        for i in range(len(self.grades)):
            print(self.grades[i])
            if item is self.grades[i]:
                self.grades[i].destroy()
                self.grades.pop(i)
                break
        
        self.pack_grades()
        self.controller.show_frame(self)
    

    def pack_grades(self):
        for grade in self.grades:
            grade.pack(side="top", pady=10)
        self.add_btn.pack(side="bottom", pady=10)
  


class Grade(tk.Frame):
    def __init__(self, parent: CourseList, controller: tk.Tk, container: tk.Frame, list_container: tk.Frame, name: str, average: float):
        tk.Frame.__init__(self, list_container, highlightbackground="black", highlightthickness=1)
        self.parent = parent
        self.controller = controller
        self.container = container
        
        self.name = name
        self.avg = average
        self.screen = parent

        course_name = tk.Label(self, text=self.name, font=ITEMNAMEFONT, padx=10)
        course_grade = tk.Label(self, text=f"avg: {round(self.avg, 2)}", font=ITEMDATAFONT, padx=10)

        course_name.pack(side="left")
        course_grade.pack(side="left")

        self.del_btn = tk.Button(self, text="delete", command=self.delete)
        self.del_btn.config(cursor="openhand")
        self.del_btn.pack(side="left")

        self.config(cursor="openhand")
    
    def delete(self):
        self.parent.remove(self)




if __name__ == "__main__":
    app = App("test", (600, 600))
    app.mainloop()