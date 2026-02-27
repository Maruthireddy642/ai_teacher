from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.IntegerField()

    def __str__(self):
        return self.name


class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.topic}"