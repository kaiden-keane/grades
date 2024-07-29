import tkinter as tk
from os import listdir
from os.path import isfile, join
from os import mkdir


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

        sem_list = SemesterList(self)
        sem_list.pack(expand=True, fill='both')
        
        self.mainloop()


class SemesterList(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, highlightbackground="black", highlightthickness=1)
        a = tk.Label(self, text="Semesters", font=("Arial", 25), highlightbackground="black", highlightthickness=1)
        a.pack(side="top")
        semList = tk.Frame(self, width=100, height=100, highlightbackground="black", highlightthickness=1)
        
        # self.sem_list = [Semester(semList, "semester 1"), Semester(semList, "semester 2")]

        self.sem_list = self.load_semesters(semList, "courses")

        for sem in self.sem_list:
            sem.pack(side="top", pady=10)
        
        semList.pack(fill=None, expand=False)
        self.focus()
        

    def load_semesters(self, parent, data_directory):
        semesters = []
        try:
            files = [f for f in listdir(data_directory) if isfile(join(data_directory, f))]
        except FileNotFoundError:
            mkdir(data_directory)
            files = [f for f in listdir(data_directory) if isfile(join(data_directory, f))]
        
        for file in files:
            new_sem = Semester(parent, file.split(".")[0]) # dont include the .txt
            new_sem.courses = self.load_semester(parent, join(data_directory, file))
            semesters.append(new_sem)
        
        return semesters

    def load_semester(self, parent, filename):
        courses = []
        
        try:
            with open(filename, "r") as f:
                course_count = 0
                for line in f:
                    if not (line.startswith("\t") or line.startswith(" ")):
                        courses.append(Course(parent, line.strip()))
                        course_count += 1
                        
                    else:
                        name, data = line.strip().split(": ")
                        grade, weight = data.strip().split(" ")
                        courses[course_count - 1].grades.append( Grade(self, name, float(grade.strip()), float(weight.strip()) ) )
            print(f"successfully loaded {filename}")
        
        except FileNotFoundError:
            print(f"cannot find file {filename}")
        except IsADirectoryError:
            print(f"{filename} is a directory")
        except PermissionError:
            print(f"insufficient permissions for {filename}")
        finally:
            return courses
    
    def save_sem_data(self, data_directory, semesters):
        for semester in semesters:
            self.save_semester(data_directory + "/" + semester.name + ".txt", semester.courses)
    
    def save_semester(filename, courses):
        try:
            with open(filename, "w") as f:
                for course in courses:
                    f.write(course.name)
                    f.write("\n")
                    
                    for grade in course.grades:
                        f.write("\t" + grade.name + ": " + str(grade.score) + " " + str(grade.weight) + "\n")
            print(f"successfully saved to {filename}")
                    
        except FileNotFoundError:
            print(f"cannot find file {filename}")
        except IsADirectoryError:
            print(f"{filename} is a directory")
        except PermissionError:
            print(f"insufficient permissions for {filename}")
            

class Semester(tk.Frame):
    def __init__(self, parent, name) -> None:
        super().__init__(parent, highlightbackground="black", highlightthickness=1)
        self.name = name
        self.courses = []
        self.avg = 0
        
        sem_name = tk.Label(self, text=self.name)
        sem_grade = tk.Label(self, text=self.avg)

        sem_name.pack(side="left")
        sem_grade.pack(side="right")
        

        bind_children_to_click(self, self.foo)
        self.config(cursor="openhand")
    
    def foo(self, event):
        print(self.name + " has been pressed")



class CourseList(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)


class Course(tk.Frame):
    def __init__(self, parent, name) -> None:
        super().__init__(parent)
        self.name = name


class GradeList(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)


class Grade(tk.Frame):
    def __init__(self, parent, name, score=-1, weight=-1) -> None:
        super().__init__(parent)
        self.name = name
        self.score = score
        self.weight = weight


if __name__ == "__main__":
    App("test", (600, 600))