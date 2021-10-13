from django.db.models.fields import EmailField
from scaffolding.models import StudentDatabase

def verify_student(student_name, student_email, student_university):
    student_object = StudentDatabase.objects.filter(university=student_university).filter(name=student_name).filter(email=student_email)
    return student_object.count() > 0

