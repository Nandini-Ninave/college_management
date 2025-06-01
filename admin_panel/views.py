from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import AdminForm, LoginForm, add_teacher_form, update_teacher_form, add_students_form, update_student_form, add_branch_form, update_branch_form, add_subject_form, update_subject_form, StudentResultForm
from .models import admin_model, teacher, students, Branches, CustomUser, Attendance, Subject, StudentResult
from django.utils.timezone import now, localdate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def admin_signup(request):
    admin_exist = admin_model.objects.filter(title='admin').exists()
    print ("Admin Exist = ", admin_exist)
    if not admin_exist:
        if request.method == 'POST':
            print("Post method")
            form = AdminForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                return render(request, 'admin_panel/login.html', {'form': form})
            else:
                print("not valid")
                HttpResponse("form is not valid")
        else:
            form = AdminForm() 
        return render(request, 'admin_panel/admin_signup.html', {'form': form})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                print(email)
                print(password)
                try:
                    user = CustomUser.objects.get(email=email)
                    # Accessing the name field from admin_model
                    name = user.admin_model.name if user.user_type == 'admin_model' else user.username
                    if check_password(password, user.password):
                        login(request, user)
                        if user.user_type == 'admin_model':
                            print("admin login")
                            name = user.admin_model.name
                            return render(request, 'admin_panel/dashboard.html', {'name': name, 'email': user.email})
                        elif user.user_type == 'teacher':
                            print("Teacher login")
                            if hasattr(user, 'teacher'):
                                name = user.teacher.first_name 
                                return render(request, 'admin_panel/teacher_dashboard.html', {'name': name}) 
                        else:
                            print("Student login")
                            name = user.students.first_name
                            id = user.students.id
                            print(id)
                            return render(request, 'admin_panel/student_dashboard.html', {'name': name, 'student_id':id})  
                except CustomUser.DoesNotExist:
                    return HttpResponse("User does not exist")
        else:
            form = LoginForm()
        return render(request, 'admin_panel/login.html', {'form': form})

def logout_view(request):
    logout(request)
    print("logout")
    return render(request, 'admin_panel/login.html')
    
@login_required
def dashboard_view(request):
    user = request.user
    admin_name = user.admin_model.name
    teacher_count = teacher.objects.count()
    student_count = students.objects.count()
    branch_count = Branches.objects.count()
    subject_count = Subject.objects.count()
    context = {
        'name':admin_name,
        "student_count": student_count or 0,
        "teacher_count": teacher_count or 0,
        "branch_count": branch_count or 0,
        "subject_count": subject_count or 0,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
def branch_view(request):
    branch_detail = Branches.objects.all()
    branch_count = Branches.objects.all().count()
    context = {
        'branch_detail': branch_detail,
        'branch_count': branch_count,
    }
    return render(request, 'admin_panel/branches.html', context)

@login_required
def add_branch(request):
    if request.method=='POST':
        form = add_branch_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/branch_view/')
    else:
        form = add_branch_form()
    return render(request, 'admin_panel/add_branch.html', {'form': form}) 

@login_required
def delete_branch(request, branch_id):
    id = Branches.objects.get(id=branch_id)
    id.delete()
    return HttpResponseRedirect('/branch_view/')

@login_required
def update_branch(request, branch_id):
    id = Branches.objects.get(id=branch_id)
    fm = update_branch_form(request.POST, instance=id)
    if fm.is_valid():
        fm.save()
        return HttpResponseRedirect('/branch_view/')
    else:
        detail = Branches.objects.get(id=branch_id)
        fm = update_branch_form(instance=detail)
    return render(request, 'admin_panel/update_branch.html', {'form':fm})


@login_required
def subject_view(request):
    subject_detail = Subject.objects.all()
    subject_count = Subject.objects.all().count()
    context = {
        'subject_detail': subject_detail,
        'subject_count': subject_count,
    }
    return render(request, 'admin_panel/subjects.html', context)

@login_required
def add_subject(request):
    if request.method=='POST':
        form = add_subject_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/subject_view/')
    else:
        form = add_subject_form()
    return render(request, 'admin_panel/add_subject.html', {'form': form}) 

@login_required
def delete_subject(request, subject_id):
    id = Subject.objects.get(id=subject_id)
    id.delete()
    return HttpResponseRedirect('/subject_view/')

@login_required
def update_subject(request, subject_id):
    id = Subject.objects.get(id=subject_id)
    fm = update_subject_form(request.POST, instance=id)
    if fm.is_valid():
        fm.save()
        return HttpResponseRedirect('/subject_view/')
    else:
        detail = Subject.objects.get(id=subject_id)
        fm = update_subject_form(instance=detail)
    return render(request, 'admin_panel/update_subject.html', {'form':fm})

@login_required
def teacher_view(request):
    print("teacher__View")
    teachers = teacher.objects.all()
    teacher_count = teacher.objects.all().count()
    print("hello ---- ", teachers)
    context = {
        'teachers': teachers,
        'teacher_count': teacher_count,
    }
    return render(request, 'admin_panel/teacher.html', context)

@login_required
def add_teacher(request):
    if request.method == 'POST':
        fm = add_teacher_form(request.POST)
        if fm.is_valid():
            first_name = fm.cleaned_data.get('first_name')
            last_name = fm.cleaned_data.get('last_name')
            subject = fm.cleaned_data.get('subject')
            email = fm.cleaned_data.get('email')
            assigned_branch = fm.cleaned_data.get('assigned_branch')
            assigned_section = fm.cleaned_data.get('assigned_section')
            phone = fm.cleaned_data.get('phone')
            hire_date = fm.cleaned_data.get('hire_date')
            password = fm.cleaned_data.get('password')
            # Create a user entry in CustomUser
            user = CustomUser.objects.create(username = email, email = email, user_type='teacher', password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.subject = subject
            user.assigned_branch = assigned_branch
            user.assigned_section = fm.cleaned_data['assigned_section']
            user.phone = phone
            user.hire_date = hire_date
            user.set_password(password) 
            user.save()
            teacher_obj = teacher.objects.create(
                user=user,  # Link teacher to CustomUser
                first_name=first_name,
                last_name=last_name,
                subject=subject,
                email=email,
                assigned_branch=assigned_branch,
                assigned_section=assigned_section,
                phone=phone,
                hire_date=hire_date
            )
            teacher_obj.save()
            return HttpResponseRedirect('/teacher/')
    else:
        fm = add_teacher_form()
    teachers = teacher.objects.all()     
    return render(request, 'admin_panel/add_teacher.html', {'form': fm, 'teachers': teachers})

@login_required
def delete_teacher(request, email):
    email = teacher.objects.get(email=email)
    email.delete()
    return HttpResponseRedirect('/teacher/')

@login_required
def update_teacher(request, email):
    if request.method == 'POST':
        detail = teacher.objects.get(email=email)
        fm = update_teacher_form(request.POST, instance=detail)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/teacher/')
    else:
        detail = teacher.objects.get(email=email)
        fm = update_teacher_form(instance=detail)
    return render(request, 'admin_panel/update_teacher.html', {'form':fm})

@login_required
def student_view(request):
    print("Student__View")
    student_details = students.objects.all()
    student_count = students.objects.all().count()
    context = {
        'student_details':student_details,
        'student_count': student_count,
    }
    print("hello ---- ", student_details)
    return render(request, 'admin_panel/student.html', context)

@login_required
def add_student(request):
    if request.method == 'POST':
        fm = add_students_form(request.POST)
        if fm.is_valid():
            print("form is valid")
            student_id = fm.cleaned_data.get('student_id')
            first_name = fm.cleaned_data.get('first_name')
            last_name = fm.cleaned_data.get('last_name')
            email = fm.cleaned_data.get('email')
            gender = fm.cleaned_data.get('gender')
            father_name = fm.cleaned_data.get('father_name')
            date_of_birth = fm.cleaned_data.get('date_of_birth')
            branch = fm.cleaned_data.get('branch')
            course = fm.cleaned_data.get('course')
            section = fm.cleaned_data.get('section')
            phone = fm.cleaned_data.get('phone')
            password = fm.cleaned_data.get('password')
            tg_id = fm.cleaned_data.get('tg').id
            enrolled_subject_ids = fm.cleaned_data.get('enrolled_subject')

            # Create user in CustomUser
            user = CustomUser.objects.create(username=email, email=email, user_type='students')
            user.set_password(password)  # Hash the password
            user.save()
            print("user is saved", user.id)
            # Assign other attributes
            user.student_id = student_id
            user.first_name = first_name
            user.last_name = last_name
            user.gender = gender
            user.father_name = father_name
            user.date_of_birth = date_of_birth
            user.branch = branch
            user.course = course
            user.section = section
            user.phone = phone

            # Assign Teacher Guardian (tg)
            teacher_obj = teacher.objects.filter(id=tg_id).first()
            user.tg = teacher_obj  
            print("add student---teacher_obj:", teacher_obj)
            enrolled_subject_ids = fm.cleaned_data.get('enrolled_subject')
            # ✅ Check if enrolled_subject_ids is not None before filtering
            if enrolled_subject_ids:
                subject_objs = Subject.objects.filter(id__in=enrolled_subject_ids)
            else:
                subject_objs = []  # If no subjects selected, assign an empty list

            print("🔍 Selected Subjects:", subject_objs)  # Debugging
            # Assign Enrolled Subjects
            user.save()

            # Create Student Object
            student_obj = students.objects.create(
                user=user, student_id=student_id, first_name=first_name, last_name=last_name,
                email=email, gender=gender, father_name=father_name, date_of_birth=date_of_birth,
                branch=branch, course=course, section=section, phone=phone, tg=teacher_obj
            )
            student_obj = students.objects.create(user=user)
            student_obj.enrolled_subject.set(subject_objs)
            student_obj.save()

            return HttpResponseRedirect('/student/')
        else:
            print("form is not valid")
            print("❌ Form Errors:", fm.errors)
    else:
        fm = add_students_form()
    student_detail = students.objects.all()  
    return render(request, 'admin_panel/add_student.html', {'form':fm, 'student_detail':student_detail}) 

@login_required
def delete_student(request, email):
    email = students.objects.get(email=email)
    email.delete()
    return HttpResponseRedirect('/student/')

@login_required
def update_student(request, email):
    if request.method == 'POST':
        detail = students.objects.get(email=email)
        print(detail)
        fm = update_student_form(request.POST, instance=detail)
        if fm.is_valid():
            print("Update students", fm)
            updated_student = fm.save(commit=False)  # Save form fields except ManyToMany
            updated_student.save()  # Save the model instance
            selected_subjects = request.POST.getlist('enrolled_subject')  # Get selected subjects as a list of IDs
            updated_student.enrolled_subject.set(Subject.objects.filter(id__in=selected_subjects)) 
            return HttpResponseRedirect('/student/')
    else:
        detail = students.objects.get(email=email)
        fm = update_student_form(instance=detail)
    return render(request, 'admin_panel/update_student.html', {'form':fm})

@login_required
def teacher_dashboard(request):
    teacher_name = request.user.username 
    print("teacher email - ", teacher_name)
    teacher_obj = teacher.objects.get(email=teacher_name)  
    print("teacher object - ", teacher_obj)
    teacher_id = teacher_obj.id
    print("teacher id - ", teacher_id)
    teacher_name = teacher_obj.first_name
    print("teacher name - ", teacher_name)
    subjects = Subject.objects.filter(teacher_id=teacher_id)
    print("subjects - ", subjects)
    student_count = students.objects.filter(enrolled_subject__in=subjects).count()
    print("student count - ", student_count)
    student = students.objects.filter(enrolled_subject__in=subjects)
    print("students - ", student)
    student_id = students.objects.filter(enrolled_subject__in=subjects).values_list("id", flat=True)
    print("Student ID:", student_id)
    today_date = now().date()
    print(today_date)
    student_present = Attendance.objects.filter(student_id__in = student_id, status = "Present", date__exact = today_date).count()
    student_absent = Attendance.objects.filter(student_id__in = student_id, status = "Absent", date__exact = today_date).count()
    print(f"students present  ({today_date})- ", student_present)
    print(f"students absent ({today_date})- ", student_absent) 
    all_attendance = Attendance.objects.all()
    print("All Attendance Records:", all_attendance.values("student_id", "status", "date"))
    context = {
        'name':teacher_name,
        'student_count': student_count,
        "student_present": int(student_present) if student_present else 0,
        "student_absent": int(student_absent) if student_absent else 0,
    }
    return render(request, 'admin_panel/teacher_dashboard.html', context) 

@login_required
def students_under_teacher(request):
    teacher_name = request.user.username  
    teacher_obj = teacher.objects.get(email=teacher_name)  
    teacher_id = teacher_obj.id
    print("Teacher:", teacher_obj)
    print("Teacher ID:", teacher_id)
    subjects = Subject.objects.filter(teacher_id=teacher_id)
    print("Subjects taught by teacher:", subjects)
    # Fetch all students enrolled in any of these subjects
    students_list = students.objects.filter(enrolled_subject__in=subjects)
    print("Students under teacher:", students_list)
    context = {
        'name': teacher_name,
        'students': students_list,
    }
    return render(request, 'admin_panel/teacher_dashboard_students.html', context)
    
@login_required
def student_attendance(request):
    teacher_name = request.user.username  
    teacher_obj = teacher.objects.get(email=teacher_name)
    teacher_id = teacher_obj.id
    today_date = localdate()
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        status = request.POST.get("status")
        try:
            student = students.objects.get(student_id=student_id)
        except students.DoesNotExist:
            return HttpResponse("Student not found")
        # # Check if attendance already exists for today
        attendance, created = Attendance.objects.get_or_create(student=student, date=today_date, defaults={"status": status},)
        if not created:
            return HttpResponse("Attendance already marked for this student.")
        attendance.status = status
        attendance.save()
    subjects = Subject.objects.filter(teacher_id=teacher_id)
    student_list = students.objects.filter(enrolled_subject__in=subjects)   
    marked_students = Attendance.objects.filter(date=today_date).values_list('student_id', flat=True)
    context = {
        "name": teacher_name,
        "students": student_list,
        'marked_students':marked_students,
    }
    return render(request, 'admin_panel/student_attendance.html', context) 
     
def add_result(request):
    if request.method == 'POST':
        form = StudentResultForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'admin_panel/results.html', {'form': form})  
    else:
        form = StudentResultForm()
    return render(request, 'admin_panel/add_results.html', {'form': form})

def student_results_list(request):
    results = StudentResult.objects.all()
    return render(request, 'admin_panel/results.html', {'results': results})

@login_required
def student_dashboard(request, student_id):
    name = request.user.username
    print(name)
    # teacher_obj = students.objects.get(email=name)  
    student = students.objects.get(id=student_id)
    student_id = student.id
    print(student_id)
    student_name = student.first_name
    total_attendance = Attendance.objects.filter(student__id=student_id).count()
    print("Total attendance - ", total_attendance)
    present_attendance = Attendance.objects.filter(student_id=student_id, status = 'present').count()
    print("Present attendance - ",present_attendance) 
    if total_attendance == 0:
        attendance_percentage = 0
    else:    
        attendance_percentage = (present_attendance / total_attendance) * 100
    context = {
        'name' : student_name,
        'attendance' : attendance_percentage,
        'student_id' : student_id, 
    }
    return render(request, 'admin_panel/student_dashboard.html', context)   

def student_attendance_view(request, student_id):
    student = students.objects.get(id=student_id)
    student_id = student.id
    total_attendance = Attendance.objects.filter(student__id=student_id)
    context = {
        'total_attendance' : total_attendance,
        'student_id' : student_id,
    }
    return render(request, 'admin_panel/student_attendance_view.html', context) 

def  student_result_view(request, student_id):
    student = students.objects.get(id=student_id)
    student_id = student.id
    result = StudentResult.objects.filter(student_id=student_id)
    context = {
        'student_id' : student_id,
        'result' : result
    }
    return render(request, 'admin_panel/student_result_view.html', context)  

def student_profile_view(request, student_id):
    student = students.objects.get(id=student_id)
    student_id = student.id
    name = student.first_name
    id = student.student_id
    email_id = student.email
    gender = student.gender
    father_name = student.father_name
    branch = student.branch
    course = student.course
    section = student.section
    phone_number = student.phone
    context = {
        'student_id' : student_id,
        'name' : name,
        'id' : id,
        "email_id" : email_id,
        "gender" : gender,
        "father_name" : father_name,
        "branch" : branch,
        "course" : course,
        "section" : section,
        "phone_number" : phone_number,
    }
    return render(request, 'admin_panel/student_profile_view.html', context)   