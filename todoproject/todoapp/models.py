from django.db import models

# Create your models here.
class TodoModel(models.Model):

    title = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.FileField(upload_to="todo_images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    complete_status = models.BooleanField(default=False)
    due_date_and_time = models.DateTimeField()


    def __str__(self):
        return self.title
    
