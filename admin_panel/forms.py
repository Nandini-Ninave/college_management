from django import forms
from .models import admin_model, teacher, students, Branches, CustomUser, Subject, StudentResult
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class AdminForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)  
    
    class Meta:
        model = admin_model
        fields = ['name', 'email', 'title', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
         # Create a new user for CustomUser and set the password using set_password
        password = self.cleaned_data.get('password')
        if password:
            # Create a new CustomUser instance
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['email'],  # Or any unique username field
                user_type='admin_model',  # Or assign the appropriate user type
            )
            user.set_password(password)  # This automatically hashes the password
            user.save()
            # Now create the admin model instance, linked to the CustomUser
            admin_instance = super().save(commit=False)
            admin_instance.user = user  # Link the CustomUser to the admin model
            admin_instance.name = self.cleaned_data['name']  # Set the name field in admin_model
            if commit:
                admin_instance.save()
            return admin_instance
        return super().save(commit=commit)

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    # password = forms.CharField(widget=forms.PasswordInput)

class add_branch_form(forms.ModelForm):
    class Meta:
        model = Branches
        fields = ['branch_name']
        widgets = {
            'branch_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter branch name'}),
        }
class update_branch_form(forms.ModelForm):
    class Meta:
        model = Branches
        fields = ['branch_name']
        widgets = {
            'branch_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter branch name'}),
        }

class add_subject_form(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=teacher.objects.all(), label="Select Teacher", widget=forms.Select(attrs={'class': 'form-control'}))
    branch = forms.ModelChoiceField(queryset=Branches.objects.all(), label="Select Branch", widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Subject        
        fields = ['subject_code', 'name', 'teacher', 'branch']
        widgets = {
            'subject_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Name'}),
        }

class update_subject_form(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=teacher.objects.all(), label="Select Teacher", widget=forms.Select(attrs={'class': 'form-control'}))
    branch = forms.ModelChoiceField(queryset=Branches.objects.all(), label="Select Branch", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Subject
        fields = ['subject_code', 'name', 'teacher', 'branch']
        widgets = {
            'subject_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Name'}),
        }

class add_teacher_form(forms.ModelForm):
    class Meta:
        model = CustomUser  
        fields = ["username", "email"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }
    first_name = forms.CharField(label="first_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first_name'}))
    last_name = forms.CharField(label="last_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last_name'}))
    subject = forms.CharField(label="subject", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}))
    email = forms.EmailField(label="email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    assigned_branch = forms.CharField(label="assigned_branch", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Branch'}))
    assigned_section = forms.CharField(label="assigned_section", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Assigned Section'}))
    phone = forms.CharField(label="phone", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    hire_date = forms.CharField(label="hire_date" ,max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Hiring Date'}))
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    def save(self, commit=True):
         # Create a new user for CustomUser and set the password using set_password
        password = self.cleaned_data.get('password')
        if password:
            # Create a new CustomUser instance
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['email'],  # Or any unique username field
                user_type='teacher',  # Or assign the appropriate user type
            )
            user.set_password(password)  # This automatically hashes the password
            user.save()

            # Now create the admin model instance, linked to the CustomUser
            admin_instance = super().save(commit=False)
            admin_instance.user = user  # Link the CustomUser to the admin model
            admin_instance.first_name = self.cleaned_data['first_name']  # Set the name field in admin_model
            if commit:
                admin_instance.save()

            return admin_instance

        return super().save(commit=commit)

class update_teacher_form(forms.ModelForm):
    assigned_branch = forms.ModelChoiceField(queryset=Branches.objects.all(), label="branch", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = teacher
        fields = ['first_name', 'last_name', 'subject', 'email', 'assigned_branch', 'assigned_section', 'phone', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'assigned_section': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Assigned Section'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
        }

class add_students_form(forms.ModelForm):
    enrolled_subject = forms.ModelMultipleChoiceField(
            queryset=Subject.objects.all(),
            widget=forms.CheckboxSelectMultiple,  # ✅ Allows selecting multiple subjects
    )
    tg = forms.ModelChoiceField(queryset=teacher.objects.all(), label="Select Teacher", widget=forms.Select(attrs={'class': 'form-control'}))
    branch = forms.ModelChoiceField(queryset=Branches.objects.all(), label="branch", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser  
        fields = ["username", "email"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }      
    student_id = forms.CharField(label="student_id", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student id'}))
    first_name = forms.CharField(label="first_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="last_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    email = forms.CharField(label="email", max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    gender = forms.CharField(label="gender", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter gender'}))
    father_name = forms.CharField(label="father_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father name'}))
    date_of_birth = forms.CharField(label="date_of_birth", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter date of birth'}))
    course = forms.CharField(label="course", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course'}))
    section = forms.CharField(label="section", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter section'}))
    phone = forms.CharField(label="phone", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    
    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        if password:
            # Create a new CustomUser instance
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['email'],  # Or any unique username field
                user_type='students',  # Or assign the appropriate user type
            )
            user.set_password(password)  # This automatically hashes the password
            user.save()

            # Now create the admin model instance, linked to the CustomUser
            admin_instance = super().save(commit=False)
            admin_instance.user = user  # Link the CustomUser to the admin model
            admin_instance.first_name = self.cleaned_data['first_name']  # Set the name field in admin_model
            if commit:
                admin_instance.save()

            return admin_instance

        return super().save(commit=commit)

class update_student_form(forms.ModelForm):
    enrolled_subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple, required=True) 
    tg = forms.ModelChoiceField(queryset=teacher.objects.all(), label="Select Teacher")
    branch = forms.ModelChoiceField(queryset=Branches.objects.all(), label="branch", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = students
        fields = ['student_id', 'first_name', 'last_name', 'email', 'gender', 'father_name', 'date_of_birth', 'branch', 'course', 'section', 'phone', 'password', 'tg'] 
        widgets = {
            'student_id':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student id'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Gender'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father Name'}),
            'date_of_birth':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date of birth'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course'}),
            'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Section'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'password':forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        }  

class StudentResultForm(forms.ModelForm):
    class Meta:
        model = StudentResult
        fields = ['student', 'subject', 'marks_obtained', 'total_marks']