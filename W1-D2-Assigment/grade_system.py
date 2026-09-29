def grade(score):
    
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "E"

score = int(input("Enter your score (0-100): "))
grade_letter = grade(score)
print("Mark: ",score ,"-> Grade: ", grade_letter)