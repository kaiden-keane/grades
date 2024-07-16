from os import listdir
from os.path import isfile, join


def load_data(data_directory):
    semesters = []
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


def save_data(semesters):
    for semester in semesters:
        save_semester(semester.name + ".txt", semester.courses)


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


def edit_grade(chosen_grade):
    print(f"current name: {chosen_grade.name}")
    new_name = input("new name [enter nothing to skip]: ")
    if new_name != "":
        chosen_grade.change_name(float(new_name))
    
    print(f"current grade: {chosen_grade.score}")
    new_grade = input("new grade [enter nothing to skip]: ")
    if new_grade != "":
        chosen_grade.change_score(float(new_grade))
    
    print(f"current weight: {chosen_grade.weight}")
    new_weight = input("new weight [enter nothing to skip]: ")
    if new_weight != "":
        chosen_grade.change_weight(float(new_weight))


def edit_grades(chosen_class):
    print("grade editor:")
    grade_choice = ""
    while (grade_choice != "q"):
        print("  1. display grades")
        print("  2. edit grades")
        print("  3. add grade")
        print("  4. remove grade")
        print("q to go back")

        grade_choice = input("Enter option: ")

        if grade_choice == "1":
            print(f"grades for {chosen_class}")
            for grade in chosen_class.grades:
                print(grade)
            print()

        elif grade_choice == "2":
            print(f"grades for {chosen_class}")
            for i in range(len(chosen_class.grades)):
                print(f"\t{i+1}. {chosen_class.grades[i]}")
            
            chosen_grades_num = input(f"select grade number 1-{len(chosen_class.grades)}: ")
            chosen_grade = chosen_class.grades[int(chosen_grades_num) - 1]
            
            print(chosen_grade)
            edit_grade(chosen_grade)
        
        elif grade_choice == "3":
            new_name = input("Enter name of new grade: ")
            currnet_grade = Grade(new_name)
            chosen_class.grades.append(currnet_grade)
            
            new_grade = input("new grade [enter nothing to skip]: ")
            if new_grade != "":
                chosen_grade.change_score(float(new_grade))
            
            new_weight = input("new weight [enter nothing to skip]: ")
            if new_weight != "":
                chosen_grade.change_weight(float(new_weight))

        elif grade_choice == "4":
            print("\nSelect grade to remove:")
            for i in range(len(chosen_class.grades)):
                print(f"  {i+1}. {chosen_class.grades[i]}")

            selected_class = int(input(f"select class to remove numbered 1-{len(chosen_class.grades)}: "))
            check = input(f"are you sure you wish to delete {chosen_class.grades[selected_class-1]}[y/Y]: ")
            if check.lower() == "y":
                chosen_class.grades.pop(selected_class - 1)


def edit_courses(semester):
    print(f"viewing courses for semester {semester.name}:")
    courses = semester.courses

    choice = ""
    while (choice != 'q'):
        print("select option")
        print("1. display classes")
        print("2. select class")
        print("3. add class")
        print("4. remove class")
        
        print("press q to exit")

        choice = input("Enter option: ")

        if choice == "1": # print courses
            
            print("\ncurrent course:")
            print("  " + "Class".ljust(19) + "  " + "Grade")
            print("+" + "-"*20 + "+" + "-" * 10 + "+")
            
            for course in courses:
                print("| " + f"{course}".ljust(19) + "+ " + f"{round(course.adjusted_avg, 3)}".ljust(9) + "|")
                print("+" + "-"*20 + "+" + "-" * 10 + "+")

        elif choice == "2": # select course
            print("\nSelect course from the following:")
            for i in range(len(courses)):
                print(f"  {i+1}. {courses[i]}")
            chosen_num = input(f"select class number 1-{len(courses)}: ")
            chosen_class = courses[int(chosen_num) - 1]
            
            print()
            edit_grades(chosen_class)
            

        elif choice == "3": # add course
            name = input("name of new course: ")
            courses.append(Course(name))
            courses = sorted(courses)

        elif choice == "4": # remove course
            print("\ncurrent courses:")
            for i in range(len(courses)):
                print(f"  {i+1}. {courses[i]}")

            selected_class = int(input(f"select class to remove numbered 1-{len(courses)}: "))
            check = input(f"are you sure you wish to delete {courses[selected_class-1]}[y/Y]: ")
            if check.lower() == "y":
                courses.pop(selected_class - 1)
        print()

def main():
    # load data
    semesters = load_data(data_directory="courses")
    for semester in semesters:
        for course in semester.courses:
            course.calc_adjusted_weighted_avg()
    print()
    
    choice = ""
    while(choice != "q"):
        print("  1. Display semester averages")
        print("  2. view semester")
        print("  3. Add semester")
        print("  4. delete semester")
        print("q to quit")

        choice = input("Enter choice: ")

        if choice == "1":
            print("\ncurrent semester avg:")
            for sem in semesters:
                avg = sem.calc_avg()
                print(f"  {sem.name}: {avg}")

        elif choice == "2":
            view_choice = ""
            while (view_choice != "q"):
                print("\ncurrent semesters:")
                for i in range(len(semesters)):
                    print(f"  {i+1}. {semesters[i].name}")
                
                view_choice = input(f"pick a semester to view (1-{len(semesters)}): ")
                if (choice.isdigit()):
                    if (int(view_choice) > 0 and int(view_choice) <= len(semesters)):
                        print()
                        edit_courses(semesters[int(view_choice) - 1])
                elif choice != "q":
                    print("please inter digit 1-{len(semesters)}")

        elif choice == "3":
            new_name = input("\nEnter name for semester: ")
            semesters.append(Semester(new_name))

        elif choice == "4":
            print("\ncurrent semesters:")
            for i in range(len(semesters)):
                print(f"  {i+1}. {semesters[i].name}")

            selected_sem = input(f"select class to remove numbered 1-{len(semesters)}: ")
            succeed = False
            if selected_sem.isdigit():
                if (int(selected_sem) > 0 and int(selected_sem) <= len(semesters)):
                    check = input(f"are you sure you wish to delete {semesters[selected_sem-1]}[y/Y]: ")
                    if check.lower() == "y":
                        semesters.pop(selected_sem - 1)
                        succeed = True
            if succeed == False:
                print("error deleting semester")
        print()
    save_data(semesters)


if __name__ == "__main__":
    main()