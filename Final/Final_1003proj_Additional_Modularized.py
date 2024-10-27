import csv

def getInput():
    # Get the number of students per group from the user
    while True:
        try:
            studentsPerGrp = int(input('Enter no of students per group from 4 to 10: '))
            if 4 <= studentsPerGrp <= 10:
                return studentsPerGrp
            else:
                print("Please enter a number between 4 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def openfile(file_path, studentsPerGrp):
    # Open the CSV file and read student data
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        # Skip the header row
        next(csv_reader)

        # Initialize variables
        class_size = 50  # Number of students per class
        classes = [[] for _ in range(50)]  # Create a list for each class

        rowcounter = 0
        classNumber = 0
        for row in csv_reader:
            if classNumber >= len(classes):
                print("Maximum number of classes reached.")
                break
            
            classes[classNumber].append(row)
            rowcounter += 1
            
            # Check if we've reached the batch size
            if rowcounter == class_size:
                rowcounter = 0
                classNumber += 1

        return classes, studentsPerGrp

def sortGroups(classes, studentsPerGrp):
    noOfGrps = 50 // studentsPerGrp
    final_groups = []

    # Sort via GPA first
    sorted_classes = []
    for class_list in classes:
        sorted_class = sorted(class_list, key=lambda x: float(x[5]), reverse=True)
        sorted_classes.append(sorted_class)

    for eachClass in sorted_classes:
        GrpList = []
        while len(GrpList) < noOfGrps:
            Grp = []  # Current group
            first_member = eachClass[0]
            Grp.append(first_member)
            eachClass.pop(0)

            checkDir = 'right'

            while len(Grp) < studentsPerGrp:
                found_member = False

                if checkDir == 'right':
                    for student in range(len(eachClass) - 1, -1, -1):
                        if eachClass[student][2] != Grp[-1][2] and eachClass[student][4] != Grp[-1][4]:
                            studentToAdd = eachClass.pop(student)
                            Grp.append(studentToAdd)
                            found_member = True
                            checkDir = 'left'
                            break

                    if not found_member:
                        for student in range(len(eachClass) - 1, -1, -1):
                            if eachClass[student][2] != Grp[-1][2]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'left'
                                break

                    if not found_member:
                        for student in range(len(eachClass) - 1, -1, -1):
                            if eachClass[student][4] != Grp[-1][4]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'left'
                                break

                    if not found_member and len(eachClass) > 0:
                        studentToAdd = eachClass.pop(-1)
                        Grp.append(studentToAdd)
                        found_member = True
                        checkDir = 'right'

                elif checkDir == 'left':
                    for student in range(len(eachClass)):
                        if eachClass[student][2] != Grp[-1][2] and eachClass[student][4] != Grp[-1][4]:
                            studentToAdd = eachClass.pop(student)
                            Grp.append(studentToAdd)
                            found_member = True
                            checkDir = 'right'
                            break

                    if not found_member:
                        for student in range(len(eachClass)):
                            if eachClass[student][2] != Grp[-1][2]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'right'
                                break

                    if not found_member:
                        for student in range(len(eachClass)):
                            if eachClass[student][4] != Grp[-1][4]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'right'
                                break

                    if not found_member and len(eachClass) > 0:
                        studentToAdd = eachClass.pop(0)
                        Grp.append(studentToAdd)
                        found_member = True
                        checkDir = 'right'

            GrpList.append(Grp)

        # Check if got leftover students
        if len(eachClass) > 0:
            #sort leftovers in desc order, highest gpa first ele
            sorted_leftovers = sorted(eachClass, key=lambda x: float(x[5]), reverse=True)
            #sort grps by avg gpa in asc order, lowest avg gpa first ele
            sorted_GrpList = sorted(GrpList, key=lambda group: sum(float(student[5]) for student in group) / len(group), reverse=False)
            #add leftover w highest gpa to grp w lowest avg gpa and so on
            for i in range(len(sorted_leftovers)):
                sorted_GrpList[i].append(sorted_leftovers[i])
            final_groups.append(sorted_GrpList)
        else:
            final_groups.append(GrpList)

    return final_groups

def writefile(final_groups):
    output_file_path = 'final_team_formation.csv'
    
    with open(output_file_path, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(["Tutorial Group", "Student ID", "School", "Name", "Gender", "CGPA", "Team Assigned"])

        for class_index, class_groups in enumerate(final_groups):
            for group_index, group in enumerate(class_groups):
                for student in group:
                    team_assigned = f"Team {group_index + 1}"
                    csv_writer.writerow([student[0], student[1], student[2], student[3], student[4], student[5], team_assigned])

    print(f"Final team formation saved to {output_file_path}")

def main():
    studentsPerGrp = getInput()
    file_path = 'records.csv'
    classes, studentsPerGrp = openfile(file_path, studentsPerGrp)
    final_groups = sortGroups(classes, studentsPerGrp)
    writefile(final_groups)

main()
