def load_data():
    courses = []
    
    try:
        with open(save_filename, "r") as f:
            course_count = 0
            for line in f:
                if not (line.startswith("\t") or line.startswith(" ")):
                    courses.append(Course(line.strip()))
                    course_count += 1
                    
                else:
                    name, data = line.strip().split(": ")
                    grade, weight = data.strip().split(" ")
                    courses[course_count - 1].grades.append( Grade(name, float(grade.strip()), float(weight.strip()) ) )
    
    except FileNotFoundError:
        print(f"cannot find file {save_filename}")
    except IsADirectoryError:
        print(f"{save_filename} is a directory")
    except PermissionError:
        print(f"insufficient permissions for {save_filename}")
    
    return courses

      
def save_data(courses):
    try:
        with open(save_filename, "w") as f:
            
            
            for course in courses:
                f.write(course.name)
                f.write("\n")
                
                for grade in course.grades:
                    f.write("\t" + grade.name + ": " + str(grade.score) + " " + str(grade.weight) + "\n")
                
    except FileNotFoundError:
        print(f"cannot find file {save_filename}")
    except IsADirectoryError:
        print(f"{save_filename} is a directory")
    except PermissionError:
        print(f"insufficient permissions for {save_filename}")


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
        return f"{self.name}:\tgrade: {self.score}\tweight: {self.weight}"


def main():
    # load data
    courses = load_data()
    # for course in courses:
    #     course.calc_adjusted_weighted_avg()
    print("\n")


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
            for course in courses:
                print(f"\t{course}")
        
        elif choice == "2": # select course
            print("\ncurrent course:")
            for i in range(len(courses)):
                print(f"\t{i+1}. {courses[i]} | avg: {courses[i].adjusted_avg}")
            chosen_num = input(f"select class number 1-{len(courses)}: ")
            chosen_class = courses[int(chosen_num) - 1]
            
            print()
            
            grade_choice = ""
            while (grade_choice != "q"):
                print("1. display grades")
                print("2. edit grades")
                print("3. add grade")
                print("4. remove grade")
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
                    
                    chosen_grades_num = input(f"select grade number 1-{len(courses)}: ")
                    chosen_grade = chosen_class.grades[int(chosen_grades_num) - 1]
                    
                    print(chosen_grade)
                    
                    print(f"current name: {chosen_grade.name}")
                    chosen_grade.change_name(input("new name: "))
                    
                    print(f"current grade: {chosen_grade.score}")
                    chosen_grade.change_score(float(input("new grade: ")))
                    
                    print(f"current weight: {chosen_grade.weight}")
                    chosen_grade.change_weight(float(input("new weight: ")))

        elif choice == "3": # add course
            name = input("name of new course: ")
            courses.append(Course(name))
            courses = sorted(courses)

        elif choice == "4": # remove course
            print("\ncurrent course:")
            for i in range(len(courses)):
                print(f"\t{i+1}. {courses[i]}")

            selected_class = int(input(f"select class to remove numbered 1-{len(courses)}: "))
            check = input(f"are you sure you wish to delete {courses[selected_class-1]}[y/Y]: ")
            if check.lower() == "y":
                courses.pop(selected_class - 1)
        print()

        save_data(courses)
    
    # save data

if __name__ == "__main__":
    save_filename = "courses.txt"
    main()