from django.shortcuts import render, redirect
from .models import Student, QuizResult


def home(request):
    return render(request, 'home.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def lesson(request):
    grade = request.GET.get('grade')
    topic = request.GET.get('topic')

    explanation = ""
    quiz = []
    doubt_answer = ""

    # If POST, override from form
    if request.method == "POST":
        grade = request.POST.get("grade") or grade
        topic = request.POST.get("topic") or topic

    # SAFE CHECK
    if not grade or not topic:
        return render(request, 'lesson.html')

    try:
        grade = int(grade)
    except:
        grade = 1

    # Generate explanation
    if grade <= 2:
        explanation = f"{topic} means something simple. Imagine sharing a pizza into equal pieces."
    else:
        explanation = f"{topic} is a mathematical concept used to represent parts of a whole. For example, 1/2 means one out of two equal parts."

    quiz = [
        f"What is {topic}?",
        f"Why is {topic} important?",
        f"Give an example of {topic}.",
        f"Where do we use {topic}?",
        f"Explain {topic} briefly."
    ]

    # DOUBT HANDLING
    if request.method == "POST" and "ask_doubt" in request.POST:
        doubt = request.POST.get("doubt")

        if grade <= 2:
            doubt_answer = f"""
You asked: {doubt}

Let me explain in a simple way 😊

👉 {topic} means dividing something into equal parts.

Imagine you have 1 chocolate 🍫.
If you share it with 1 friend, each of you gets 1/2.

That is called a fraction.
"""
        else:
            doubt_answer = f"""
You asked: {doubt}

Here is a clear explanation:

👉 {topic} represents parts of a whole.

If a pizza is divided into 4 equal slices and you take 1 slice,
you have 1/4 of the pizza.

Fractions have:
• Numerator → top number  
• Denominator → bottom number  
"""

    return render(request, 'lesson.html', {
        'explanation': explanation,
        'quiz': quiz,
        'doubt_answer': doubt_answer
    })

def exam(request):
    grade = request.GET.get('grade')
    topic = request.GET.get('topic')

    try:
        grade = int(grade)
    except:
        grade = 1

    questions = [
        f"Define {topic}.",
        f"Give one real-life example of {topic}.",
        f"Why is {topic} important?",
        f"Solve a basic problem related to {topic}.",
        f"Explain {topic} in your own words."
    ]

    if request.method == "POST":
        student_name = request.POST.get("student_name")

        score = 0
        for i in range(1, 6):
            answer = request.POST.get(f"answer{i}")
            if answer and len(answer) > 5:
                score += 1

        student, created = Student.objects.get_or_create(
            name=student_name,
            grade=grade
        )

        QuizResult.objects.create(
            student=student,
            topic=topic,
            score=score
        )

        # 🔥 ADAPTIVE RESPONSE
        if score <= 2:
            feedback = f"""
You need more practice.

Let me explain {topic} again in a simpler way:

{topic} means dividing something into equal parts.
Imagine sharing chocolate with friends.

Let's try easier questions next time.
"""
        elif score <= 4:
            feedback = f"""
Good effort!

You understand {topic}, but you can improve.
Review key concepts like numerator and denominator.
"""
        else:
            feedback = f"""
Excellent work! 🎉

You have mastered {topic}.
Now try advanced problems involving real-life applications.
"""

        return render(request, "result.html", {
            "score": score,
            "total": 5,
            "feedback": feedback,
            "grade": grade,
            "topic": topic
        })

    return render(request, "exam.html", {
        "questions": questions,
        "topic": topic,
        "grade": grade
    })

def progress(request):
    results = QuizResult.objects.all()
    return render(request, 'progress.html', {'results': results})