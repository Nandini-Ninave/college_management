from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
            
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (('students', 'students'), ('admin_model', 'admin_model'), ('teacher', 'teacher'))
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True)  # Use email for authentication
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='admin_model')

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return f"{self.email}"

class admin_model(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=255)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.email} (Admin)"

class teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher", null=True)  
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    assigned_branch = models.CharField(max_length=100, null=True)
    assigned_section = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    hire_date = models.DateField(null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (teacher)"

class Branches(models.Model):
    branch_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.branch_name}"
    
class Subject(models.Model):
    name = models.CharField(max_length=120)
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE, related_name='subjects')
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, null=True)    
    subject_code = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return f"{self.name} - {self.subject_code}" 

class students(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True) 
    branch = models.CharField(max_length=50, null=True)
    course = models.CharField(max_length=50, null=True)
    section = models.CharField(max_length=15, null=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    tg = models.ForeignKey(teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    enrolled_subject = models.ManyToManyField(Subject, related_name="students")
    def __str__(self):
        return f"{self.user.email} - {self.student_id}"

class Attendance(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(auto_now_add=True)  # Automatically sets to current date
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE, null = True)
    class meta:
        unique_student = ('students', 'date')
    def __str__(self):
        return f"{self.student.first_name} - {self.date} - {self.status}"
    
class StudentResult(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    
    def result_status(self):
       return "Pass" if self.marks_obtained >= (self.total_marks * Decimal("0.4")) else "Fail"

    def __str__(self):
        return f"{self.student.first_name} - {self.subject.name}: {self.marks_obtained}/{self.total_marks} ({self.result_status()})"