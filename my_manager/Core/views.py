# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Task, Category, Question, Answer, Task, Passage  # Import necessary models
from django.http.response import JsonResponse, HttpResponse
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UpdateProfileForm
from django.db.models import Sum, F
from django.http import JsonResponse
import json
from collections import defaultdict
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from collections import defaultdict
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import QuizAttempt, QuestionResult


def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'register.html')

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
            
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Assuming you're updating the User model
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()

        # Add a success message or redirect
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile.html')


@login_required
def results(request):
    # Fetch quiz attempts
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('date_taken').prefetch_related(
        'question_results__question__passage',
        'question_results__selected_answer',
        'question_results__question__answers',
    )

    quiz_attempts_desc = quiz_attempts[::-1]  # Reverse the QuerySet

    # Prepare data for Pie Charts per Category and Topic
    category_stats = defaultdict(lambda: {
        'total_correct': 0,
        'total_incorrect': 0,
        'correct_to_incorrect': 0,
        'incorrect_to_correct': 0,
        # 'incorrect_to_incorrect': 0,  # Removed as per request
    })

    topic_stats = defaultdict(lambda: {
        'total_correct': 0,
        'total_incorrect': 0,
        'correct_to_incorrect': 0,
        'incorrect_to_correct': 0,
        # 'incorrect_to_incorrect': 0,  # Removed as per request
    })

    # Dictionaries to keep track of previous attempts for answer changes
    previous_category_answers = defaultdict(dict)  # {category: {question_id: {'is_correct': bool}}}
    previous_topic_answers = defaultdict(dict)     # {topic: {question_id: {'is_correct': bool}}}

    for attempt in quiz_attempts:
        question_results = attempt.question_results.select_related('question__category', 'question__passage')

        for qr in question_results:
            # Handle Category Stats
            category_name = qr.question.category.name
            category_question_id = qr.question.id
            category_stats_entry = category_stats[category_name]

            # Update total correct and incorrect
            if qr.is_correct:
                category_stats_entry['total_correct'] += 1
            else:
                category_stats_entry['total_incorrect'] += 1

            prev_attempt_category = previous_category_answers[category_name].get(category_question_id)
            if prev_attempt_category is not None:
                # Check for answer changes
                if prev_attempt_category['is_correct'] and not qr.is_correct:
                    category_stats_entry['correct_to_incorrect'] += 1
                elif not prev_attempt_category['is_correct'] and qr.is_correct:
                    category_stats_entry['incorrect_to_correct'] += 1
                # No need to track incorrect_to_incorrect as per request

            # Update previous answer
            previous_category_answers[category_name][category_question_id] = {'is_correct': qr.is_correct}

            # Handle Topic Stats
            topic_name = qr.question.passage.title if qr.question.passage else 'No Topic'
            topic_question_id = qr.question.id
            topic_stats_entry = topic_stats[topic_name]

            # Update total correct and incorrect
            if qr.is_correct:
                topic_stats_entry['total_correct'] += 1
            else:
                topic_stats_entry['total_incorrect'] += 1

            prev_attempt_topic = previous_topic_answers[topic_name].get(topic_question_id)
            if prev_attempt_topic is not None:
                # Check for answer changes
                if prev_attempt_topic['is_correct'] and not qr.is_correct:
                    topic_stats_entry['correct_to_incorrect'] += 1
                elif not prev_attempt_topic['is_correct'] and qr.is_correct:
                    topic_stats_entry['incorrect_to_correct'] += 1
                # No need to track incorrect_to_incorrect as per request

            # Update previous answer
            previous_topic_answers[topic_name][topic_question_id] = {'is_correct': qr.is_correct}

    # Prepare data for the template
    category_stats_list = list(category_stats.items())  # Convert to list of tuples
    category_stats_json = json.dumps(category_stats)

    topic_stats_list = list(topic_stats.items())
    topic_stats_json = json.dumps(topic_stats)

    context = {
        'quiz_attempts': quiz_attempts,
        'quiz_attempts_desc': quiz_attempts_desc,
        'category_stats': category_stats_list,
        'category_stats_json': category_stats_json,
        'topic_stats': topic_stats_list,
        'topic_stats_json': topic_stats_json,
    }
    return render(request, 'results.html', context)


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = Task(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password',  # email subject
                email_body,
                settings.EMAIL_HOST_USER,  # email sender
                [email]  # email receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):
    if Task.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):
    try:
        password_reset_id = Task.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    except Task.DoesNotExist:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')

# New Views for the Quiz Functionality
@login_required
def quiz_list_view(request):
    try:
        category_name = request.GET.get('category')
        sub_category_name = request.GET.get('sub_category')

        passages = Passage.objects.filter(category__name=category_name)
        if sub_category_name:
            passages = passages.filter(sub_category__name=sub_category_name)

        data = []
        for passage in passages:
            passage_data = {
                'title': passage.title,
                'text': passage.text,
                'questions': []
            }

            questions = passage.questions.all()
            for question in questions:
                answers = question.answers.all()
                answers_data = [{
                    'id': answer.id,
                    'text': answer.text,
                    'is_correct': answer.is_correct,
                } for answer in answers]

                passage_data['questions'].append({
                    'id': question.id,
                    'text': question.text,
                    'marks': question.marks,
                    'answers': answers_data,
                    'uid': str(question.uid),
                    'explanation': question.explanation,
                    'hints': [question.hint1, question.hint2, question.hint3] 
                })

            data.append(passage_data)

        payload = {
            'status': True,
            'data': data
        }
        return JsonResponse(payload, status=200)

    except Exception as e:
        payload = {'status': False, 'data': [], 'message': str(e)}
        return JsonResponse(payload, status=500)
    

@login_required
def quiz_results(request):
    """
    Display quiz results with a breakdown of each question.
    """
    # Get the session data from quiz completion
    score = request.session.get('quiz_score', 0)
    total_marks = request.session.get('total_marks', 0)
    questions = request.session.get('quiz_questions', [])

    # You can fetch the actual Question and Answer models here if needed
    # Otherwise, assume 'questions' in the session already contains the necessary info

    def getCorrectAnswer(question):
        for answer in question['answers']:
            if answer['is_correct']:
                return answer['text']
        return None

    context = {
        'score': score,
        'total_marks': total_marks,
        'questions': questions,
        'getCorrectAnswer': getCorrectAnswer
    }
    return render(request, 'results.html', context)

@login_required
def home(request):
    context = {"categories": Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz_main/?category={request.GET.get('category')}")
    return render(request, 'home.html', context)

@login_required
def quiz_main(request):
    context = {"category": request.GET.get('category')}
    return render(request, 'quiz_main.html', context)



@login_required
@csrf_exempt
def save_quiz_results(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_name = data.get('category')
            score = data.get('score')
            total_marks = data.get('total_marks')
            passages_data = data.get('passages')

            category = Category.objects.get(name=category_name)

            # Create a new QuizAttempt
            quiz_attempt = QuizAttempt.objects.create(
                user=request.user,
                category=category,
                score=score,
                total_marks=total_marks
            )

            # Save QuestionResults
            for passage in passages_data:
                for question_data in passage['questions']:
                    question = Question.objects.get(id=question_data['id'])
                    selected_answer_id = question_data.get('selectedAnswerId')
                    selected_answer = Answer.objects.get(id=selected_answer_id) if selected_answer_id else None
                    is_correct = question_data.get('is_correct', False)
                    hints_used = question_data.get('hints_used', 0)

                    QuestionResult.objects.create(
                        quiz_attempt=quiz_attempt,
                        question=question,
                        selected_answer=selected_answer,
                        is_correct=is_correct,
                        used_hints=hints_used
                    )

            return JsonResponse({'status': True, 'message': 'Quiz results saved successfully.'}, status=200)

        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method.'}, status=400)
