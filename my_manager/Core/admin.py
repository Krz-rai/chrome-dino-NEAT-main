
from django.contrib import admin
from .models import Question, Answer, Category, Passage


# Inline for Answer
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Default number of answer options displayed
    min_num = 1  # Minimum number of answers required
    max_num = 10  # Maximum number of answers allowed
    fields = ['text', 'is_correct']  # Fields to display in the inline
    fk_name = 'question'  # Foreign key name

# Inline for Question (it needs to inherit from InlineModelAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'category', 'passage']
    model = Question
    extra = 1  # Number of blank extra forms to display
    inlines = [AnswerInline]  # Include the AnswerInline for each question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True  
    
# Admin for Passage
class PassageAdmin(admin.ModelAdmin):

    list_display = ['title', 'category']
    inlines = [QuestionInline]  # Use QuestionInline here

# Register the models and the inlines
admin.site.register(Question, QuestionAdmin)
admin.site.register(Passage)
admin.site.register(Answer)
admin.site.register(Category)
