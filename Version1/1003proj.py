import csv

file_path = 'records.csv'
with open(file_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file) #csv_reader is an obj w each record as a list
    #skip the header row
    next(csv_reader)

    # Initialize variables
    class_size = 50  # Number of students per class
    classes = [[] for i in range(2)] #do for 2 classes first
    print(classes)

    rowcounter=0
    classNumber = 0
    for row in csv_reader:
    # Append the row to the current class
        classes[classNumber].append(row)
        rowcounter += 1  # Increment the row counter
        
    # Check if we've reached the batch size
        if rowcounter == class_size:
            rowcounter = 0  # Reset row counter
            classNumber += 1  # Move to the next class

    #read the GPA of each student, then add them up and /50 to find avg
    #means avg GPA per grp = avg GPA per student that we found earlier
    #school, count how many diff schools there r, 2nd person in Grp A check if diff sch and gender against 3rd person
    #optional: count how many students per sch there r
    #gender, count how many Male and Female, then /10, then round up Male, round down female
    #when reach last few groups, then prioritize gpa first, then school, then gender

    #sort via GPA first
    sorted_classes = []
    for class_list in classes:
        # sorted() takes in a list and returns a sorted list
        # key is a fn that takes in 1 argument and returns a val to be used for sorting
        # lambda x: float(x[5]) is an anony fn that takes in a single ele in the list and returns the CGPA of that student
        # float(x[5]) is to convert the CGPA which is initially str to a float for sorting
        # reverse = True cuz u wan to sort them in desc order via GPA
        # Sort each class list by CGPA (fifth column, index 5) in descending order
        sorted_class = sorted(class_list, key=lambda x: float(x[5]), reverse=True)
        sorted_classes.append(sorted_class)

    print(sorted_classes)

    #calc avg gpa per student = avg gpa each grp shd have
    AvgGPAlist = []
    SumGPA=0
    for eachClass in sorted_classes:
        SumGPA=0
        for student in eachClass:
            SumGPA += float(student[5])
        AvgGPA = [round(SumGPA/50,3)]
        AvgGPAlist.append(AvgGPA)
    print(AvgGPAlist)

    #calc avg male female per grp
    GenderList = []
    for eachClass in sorted_classes:
        MaleCounter=0
        FemaleCounter=0
        for student in eachClass:
            if student[4] == 'Male':
                MaleCounter+=1
            elif student[4] == 'Female':
                FemaleCounter+=1
        GenderList.append([MaleCounter/10,FemaleCounter/10])
    print(GenderList) #first ele per nested list is for Male

    # Allocate groups
    final_groups = []
    for eachClass in sorted_classes:
        TenGrp = []  # Initialize a list for 10 groups

        while len(TenGrp) < 10:  # We need 10 groups
            Grp = []  # Current group

            first_member = eachClass[0]
            Grp.append(first_member)
            eachClass.pop(0)  # Remove the first member from the class list

            # Start checking for the next member from RHS
            checkDir = 'right'

            while len(Grp) < 5:  # We need 5 members in each group
                found_member = False  # Flag to track if a valid member is found

                if checkDir == 'right':
                    # Check from the right to left
                    for student in range(len(eachClass) - 1, -1, -1):
                        # Different school and gender
                        if eachClass[student][2] != Grp[-1][2] and eachClass[student][4] != Grp[-1][4]:
                            studentToAdd = eachClass.pop(student)
                            Grp.append(studentToAdd)
                            found_member = True  # Valid member found
                            checkDir = 'left'  # Switch direction for the next member
                            break

                    # If not found, check for different school
                    if not found_member:
                        for student in range(len(eachClass) - 1, -1, -1):
                            if eachClass[student][2] != Grp[-1][2]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'left'
                                break

                    # If still not found, check for different gender
                    if not found_member:
                        for student in range(len(eachClass) - 1, -1, -1):
                            if eachClass[student][4] != Grp[-1][4]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'left'
                                break

                    # If still not found, take the rightmost element cuz we wan the biggest gpa diff
                    if not found_member and len(eachClass) > 0:
                        studentToAdd = eachClass.pop(-1)
                        Grp.append(studentToAdd)
                        found_member = True
                        checkDir = 'right'

                elif checkDir == 'left':
                    # Check from the left to right
                    for student in range(len(eachClass)):
                        if eachClass[student][2] != Grp[-1][2] and eachClass[student][4] != Grp[-1][4]:
                            # Different school and gender
                            studentToAdd = eachClass.pop(student)
                            Grp.append(studentToAdd)
                            found_member = True
                            checkDir = 'right'
                            break

                    # If not found, check for different school
                    if not found_member:
                        for student in range(len(eachClass)):
                            if eachClass[student][2] != Grp[-1][2]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'right'
                                break

                    # If still not found, check for different gender
                    if not found_member:
                        for student in range(len(eachClass)):
                            if eachClass[student][4] != Grp[-1][4]:
                                studentToAdd = eachClass.pop(student)
                                Grp.append(studentToAdd)
                                found_member = True
                                checkDir = 'right'
                                break

                    # If still not found, take the leftmost element
                    if not found_member and len(eachClass) > 0:
                        studentToAdd = eachClass.pop(0)
                        Grp.append(studentToAdd)
                        found_member = True
                        checkDir = 'right'

            #shd have 5 members in grp now           
            TenGrp.append(Grp)

        # Add the 10 groups formed for this class to final_groups, which has groups for all classes
        final_groups.append(TenGrp)

    # Print each grouping for each class
    for eachClass in final_groups:
        print('Tutorial Grp: {}'.format(eachClass[0][0][0]))
        GroupName = 1
        for group in eachClass:
            print('Group Number {}'.format(GroupName))
            GroupName+=1
            print(group)
            print()


# Specify the output file path
output_file_path = 'final_team_formation.csv'

# Open the output file in write mode
with open(output_file_path, mode='w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    
    # Write the header row
    csv_writer.writerow(["Tutorial Group", "Student ID", "School", "Name", "Gender", "CGPA", "Team Assigned"])

    # Iterate through each class and its groups
    for class_index, class_groups in enumerate(final_groups):
        for group_index, group in enumerate(class_groups):
            # Iterate through each student in the group and write their details
            for student in group:
                # student is a list of details: [Tutorial Group, Student ID, School, Name, Gender, CGPA]
                # Add the "Team Assigned" value
                team_assigned = f"Team {group_index + 1}"
                csv_writer.writerow([student[0], student[1], student[2], student[3], student[4], student[5], team_assigned])

print(f"Final team formation saved to {output_file_path}")


                    
                    
                    
                
                
    
            
            
        
    
    
    
        

