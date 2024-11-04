import random
import string
from io import BytesIO

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404


from .forms import TaskForm, FeedbackForm
from .models import Task, StudentList


def projecthomepage(request):
    return render(request,'adminapp/ProjectHomePage.html')

def printpagecall(request):
    return render(request,'adminapp/printer.html')
def printpagelogic(request):
    if request.method =="POST":
        user_input=request.POST['user_input']
        print(f'User input: {user_input}')
    a1= {'user_input':user_input}
    return render(request,'adminapp/printer.html',a1)



def exceptionpagecall(request):
    return render(request, 'adminapp/ExceptionHandling.html')

def exceptionpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10 / num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/ExceptionHandling.html', {'result': result, 'error': error_message})
    return render(request, 'adminapp/ExceptionHandling.html')

def randompagecall(request):
    return render(request, 'adminapp/randomexample.html')

def randomlogic(request):
    if request.method=="POST":
        number1=int(request.POST['number1'])
        ran=''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
    a1={'ran':ran}
    return render(request,'adminapp/randomexample.html',a1)

def calculatorpagecall(request):
    return render(request, 'adminapp/calculator.html')

def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Infinity'

        return render(request, 'adminapp/calculator.html', {'result': result})
    return render(request, 'adminapp/calculator.html')

def datetimepagecall(request):
    return render(request,'adminapp/datetimepage.html')


import datetime
import calendar

def datetimepagelogic(request):
    if request.method == "POST":
        number1 = int(request.POST['date1'])
        x = datetime.datetime.now()
        from datetime import timedelta
        ran= x + timedelta(days=number1)
        ran1 = ran.year
        ran2 = calendar.isleap(ran1)
        if ran2 == False:
            ran3 = "Not leap year"
        else:
            ran3 = "leap year"
    a1 = {'ran': ran, 'ran3':ran3, 'ran1':ran1, 'number1':number1}
    return render(request, 'adminapp/datetimepage.html', a1)

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'adminapp/add_task.html',
                  {'form' : form, 'tasks': tasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render
def UserRegisterPageCall(request):
    return render(request, 'adminapp/UserRegisterPage.html')
def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/UserRegisterPage.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'adminapp/UserRegisterPage.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return render(request, 'adminapp/ProjectHomePage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/UserRegisterPage.html')
    else:
        return render(request, 'adminapp/login.html')

def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLoginPage.html')

def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if len(username) == 10:
                # Redirect to StudentHomePage
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')  # Replace with your student homepage URL name
                # return render(request, 'facultyapp/FacultyHomepage.html')
            elif len(username) == 4:
                # Redirect to FacultyHomePage
                # messages.success(request, 'Login successful as faculty!')
                return redirect('facultyapp:FacultyHomePage')  # Replace with your faculty homepage URL name
                # return render(request, 'facultyapp/FacultyHomepage.html')
            else:
                # Invalid username length
                messages.error(request, 'Username length does not match student or faculty criteria.')
                return render(request, 'adminapp/UserLoginPage.html')
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/UserLoginPage.html')
    else:
        return render(request, 'adminapp/UserLoginPage.html')

def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')


def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student_list.html', {'students': students})

from .forms import StudentForm
from .models import StudentList
#def add_student(request):
 #   if request.method == 'POST':
  #      form = StudentForm(request.POST)
   #     if form.is_valid():
    #        form.save()
     #       return redirect('student_list')
    #else:
     #   form = StudentForm()
   # return render(request, 'adminapp/add_student.html', {'form': form})

from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save feedback to the database
            return redirect('projecthomepage')  # Redirect to the same page after submission
    else:
        form = FeedbackForm()

    return render(request, 'adminapp/feedback_form.html', {'form': form})

from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True)
        total_sales = df['Sales'].sum()
        average_sales = df['Sales'].mean()

        df['Month'] = df['Date'].dt.month
        monthly_sales = df.groupby('Month')['Sales'].sum()
        month_names = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        monthly_sales.index = monthly_sales.index.map(lambda x: month_names[x-1])

        plt.pie(monthly_sales, labels=monthly_sales.index, autopct='%1.1f%%')
        plt.title('Sales Distribution per Month')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        return render(request, 'adminapp/chart.html',{
            'total_sales':total_sales,
            'average_sales':average_sales,
            'chart': image_data,
        })
    return render(request, 'adminapp/chart.html', {'form': UploadFileForm()})

from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save(commit=False)
            contact_instance.save()

            # Get the logged-in user
            user_email = request.user.email
            user_first_name = request.user.first_name

            # Prepare email details
            subject = 'New Contact Added'
            message = (
                f'Hello, {user_first_name},\n\n'
                f'A new contact has been added with the following details:\n'
                f'Name: {contact_instance.name}\n'
                f'Email: {contact_instance.email}\n'
                f'Phone Number: {contact_instance.phone_number}\n'
                f'Address: {contact_instance.address}\n\n'  # Updated to address
                f'Thank you!'
            )
            from_email = 'jahnavichevuri@gmail.com'
            recipient_list = [user_email]

            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            return redirect('add_contact')  # Redirect after saving

    else:
        form = ContactForm()

    contacts = Contact.objects.all()
    return render(request, 'adminapp/contact.html', {'form': form, 'contacts': contacts})

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from .models import Contact

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    # Ensure the user is logged in
    if request.user.is_authenticated:
        # Get the logged-in user's email and first name
        user_email = request.user.email
        user_first_name = request.user.first_name

        # Prepare email details
        subject = 'Contact Deleted'
        message = (
            f'Hello, {user_first_name},\n\n'
            f'The following contact has been deleted:\n'
            f'Name: {contact.name}\n'
            f'Email: {contact.email}\n'
            f'Phone Number: {contact.phone_number}\n'
            f'Address: {contact.address}\n\n'
            f'Thank you!'
        )
        from_email = 'jahnavichevuri@gmail.com'
        recipient_list = [user_email]

        # Send the email before deleting the contact
        send_mail(subject, message, from_email, recipient_list)

    # Delete the contact
    contact.delete()

    return redirect('add_contact')  # Redirect after deletion

# Adjust this to your desired URL after deletion
def add_contact_page_call(request):
    return render(request, 'adminapp/contact.html')
