
import tkinter as tk
from utils import Course, Grade, Semester, load_data, save_data



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
            current_grade = Grade(new_name)
            chosen_class.grades.append(current_grade)
            
            new_grade = input("mark recieved [enter nothing to skip]: ")
            if new_grade != "":
                current_grade.change_score(float(new_grade))
            
            new_weight = input("weight [enter nothing to skip]: ")
            if new_weight != "":
                current_grade.change_weight(float(new_weight))

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
            if len(courses) == 0:
                print("No courses exist. Not Completed")
            else:
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
            
            if len(courses) == 0:
                print("No courses exist. Not Completed")
            else:
                selected_class = int(input(f"select class to remove numbered 1-{len(courses)}: "))
                check = input(f"are you sure you wish to delete {courses[selected_class-1]}[y/Y]: ")
                if check.lower() == "y":
                    courses.pop(selected_class - 1)
        print()

def main():
    data_directory = "courses"
    # load data
    semesters = load_data(data_directory)
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
                
                if len(semesters) == 0:
                    print("No courses exist. Not Completed")
                    break
                else:
                    view_choice = input(f"pick a semester to view (1-{len(semesters)}): ")
                    if (view_choice.isdigit()):
                        if (int(view_choice) > 0 and int(view_choice) <= len(semesters)):
                            print()
                            edit_courses(semesters[int(view_choice) - 1])
                            break
                    elif choice != "q":
                        print(f"please enter digit 1-{len(semesters)}")

        elif choice == "3":
            new_name = input("\nEnter name for semester: ")
            semesters.append(Semester(new_name))

        elif choice == "4":
            print("\ncurrent semesters:")
            for i in range(len(semesters)):
                print(f"  {i+1}. {semesters[i].name}")

            if len(semesters) == 0:
                print("No courses exist. Not Completed")
            else:
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
    save_data(data_directory, semesters)

# courses = []
# for i in range(len(courses)):
#     col = i % 2
#     row = i // 2
# add_courses:
#     col = (len(courses)) % 2
#     row = (len(courses)) // 2



if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("grade manager")
    course_frame = tk.Frame(root)

    a = tk.Label(root, text="course 1")
    b = tk.Label(root, text="course 2")
    a.pack(side=tk.LEFT)
    b.pack(side=tk.RIGHT)
    

    root.mainloop()