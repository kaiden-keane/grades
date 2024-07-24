from os import listdir
from os.path import isfile, join
from os import mkdir


class Semester():
    def __init__(self, name) -> None:
        self.name = name
        self.courses = []
        self.avg = 0
    
    def calc_avg(self):
        total_avg = 0
        count = 0
        for course in self.courses:
            total_avg += course.adjusted_avg
            count += 1
        if count == 0:
            self.avg = 0
        else:
            self.avg = total_avg / count
        
        return self.avg


class Course():
    def __init__(self, name) -> None:
        self.name = name
        self.grades = []
        self.adjusted_avg = 0
    
    def calc_adjusted_weighted_avg(self):
        total_weighted_score = 0
        total_weights = 0
        for grade in self.grades:
            total_weighted_score += grade.score * grade.weight
            total_weights += grade.weight
        if total_weights == 0:
            self.adjusted_avg = 0
        else:
            self.adjusted_avg = total_weighted_score / total_weights

    def __str__(self) -> str:
        return self.name

    def __lt__(self, other):
        return self.name < other.name


class Grade():
    def __init__(self, name, score=-1, weight=-1) -> None:
        self.name = name
        self.score = score
        self.weight = weight
    
    def change_name(self, new_name):
        self.name = new_name

    def change_score(self, new_score):
        self.score = new_score
    
    def change_weight(self, new_weight):
        self.weight = new_weight
    
    def __str__(self) -> str:
        if self.score == -1:
            if self.weight == -1:
                return f"{self.name}:\tgrade: N/A\tweight: N/A"
            else:
                return f"{self.name}:\tgrade: N/A\tweight: {self.weight}"
        elif self.weight == -1:
            return f"{self.name}:\tgrade: {self.score}\tweight: N/A"
        else:
            return f"{self.name}:\tgrade: {self.score}\tweight: {self.weight}"



def load_data(data_directory):
    semesters = []
    try:
        files = [f for f in listdir(data_directory) if isfile(join(data_directory, f))]
    except FileNotFoundError:
        mkdir(data_directory)
        files = [f for f in listdir(data_directory) if isfile(join(data_directory, f))]
    
    for file in files:
        new_sem = Semester(file.split(".")[0]) # dont include the .txt
        new_sem.courses = load_semester(join(data_directory, file))
        semesters.append(new_sem)
    
    return semesters


def load_semester(filename):
    courses = []
    
    try:
        with open(filename, "r") as f:
            course_count = 0
            for line in f:
                if not (line.startswith("\t") or line.startswith(" ")):
                    courses.append(Course(line.strip()))
                    course_count += 1
                    
                else:
                    name, data = line.strip().split(": ")
                    grade, weight = data.strip().split(" ")
                    courses[course_count - 1].grades.append( Grade(name, float(grade.strip()), float(weight.strip()) ) )
        print(f"successfully loaded {filename}")
    
    except FileNotFoundError:
        print(f"cannot find file {filename}")
    except IsADirectoryError:
        print(f"{filename} is a directory")
    except PermissionError:
        print(f"insufficient permissions for {filename}")
    finally:
        return courses


def save_data(data_directory, semesters):
    for semester in semesters:
        save_semester(data_directory + "/" + semester.name + ".txt", semester.courses)


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