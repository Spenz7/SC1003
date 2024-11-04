import csv

def main():
    classes = openfile()
    final_groups = sortGroups(classes)
    writefile(final_groups)

def openfile():
    file_path = 'records.csv'
    
    classes = [[] for _ in range(120)]  #120 groups
    rowcounter = 0
    classNumber = 0

    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  #Skip the header row

        for row in csv_reader:
            if classNumber >= len(classes):
                print("Maximum number of classes reached.")
                break

            classes[classNumber].append(row)
            rowcounter += 1
            
            if rowcounter == 50:  #50 students per class
                rowcounter = 0
                classNumber += 1

    return classes

def sortGroups(classes):
    sorted_classes = []
    
    for class_list in classes:
        sorted_class = sorted(class_list, key=lambda x: float(x[5]), reverse=True)
        sorted_classes.append(sorted_class)

    #print("Sorted classes by GPA:", sorted_classes)

    AvgGPAlist = []
    for eachClass in sorted_classes:
        SumGPA = sum(float(student[5]) for student in eachClass)
        AvgGPA = round(SumGPA / len(eachClass), 3)  # average GPA per class
        AvgGPAlist.append(AvgGPA)
    print('AvgGPA per class:', AvgGPAlist)

    GenderList = []
    for eachClass in sorted_classes:
        MaleCounter = sum(1 for student in eachClass if student[4] == 'Male')
        FemaleCounter = sum(1 for student in eachClass if student[4] == 'Female')
        GenderList.append([MaleCounter / 10, FemaleCounter / 10])
    print('Avg Male/Female per Grp:', GenderList)

    final_groups = []
    for eachClass in sorted_classes:
        TenGrp = []  # Initialize a list for 10 groups

        while len(TenGrp) < 10:  # We need 10 groups
            Grp = []  # Current group
            first_member = eachClass.pop(0)  # Add the first member
            Grp.append(first_member)

            checkDir = 'right'

            while len(Grp) < 5:  # We need 5 members in each group
                found_member = False

                # Check based on the current direction
                if checkDir == 'right':
                    for student in range(len(eachClass) - 1, -1, -1):
                        if eachClass[student][2] != Grp[-1][2] and eachClass[student][4] != Grp[-1][4]:
                            Grp.append(eachClass.pop(student))
                            found_member = True
                            checkDir = 'left'
                            break
                    if not found_member:
                        for student in range(len(eachClass) - 1, -1, -1):
                            if eachClass[student][2] != Grp[-1][2]:
                                Grp.append(eachClass.pop(student))
                                found_member = True
                                checkDir = 'left'
                                break
                    if not found_member:
                        for student in range(len(eachClass) - 1, -1, -1):
                            if eachClass[student][4] != Grp[-1][4]:
                                Grp.append(eachClass.pop(student))
                                found_member = True
                                checkDir = 'left'
                                break
                    if not found_member and len(eachClass) > 0:
                        Grp.append(eachClass.pop(-1))
                        found_member = True
                        checkDir = 'right'
                elif checkDir == 'left':
                    for student in range(len(eachClass)):
                        if eachClass[student][2] != Grp[-1][2] and eachClass[student][4] != Grp[-1][4]:
                            Grp.append(eachClass.pop(student))
                            found_member = True
                            checkDir = 'right'
                            break
                    if not found_member:
                        for student in range(len(eachClass)):
                            if eachClass[student][2] != Grp[-1][2]:
                                Grp.append(eachClass.pop(student))
                                found_member = True
                                checkDir = 'right'
                                break
                    if not found_member:
                        for student in range(len(eachClass)):
                            if eachClass[student][4] != Grp[-1][4]:
                                Grp.append(eachClass.pop(student))
                                found_member = True
                                checkDir = 'right'
                                break
                    if not found_member and len(eachClass) > 0:
                        Grp.append(eachClass.pop(0))
                        found_member = True
                        checkDir = 'right'

            TenGrp.append(Grp)

        final_groups.append(TenGrp)

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

main()
