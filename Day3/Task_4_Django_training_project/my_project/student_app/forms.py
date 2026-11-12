from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
      
    class Meta:
        model = Student
        fields = "__all__"



     # Age validation
    def clean_age(self):
        age = self.cleaned_data.get("age")

        if age < 16 or age > 60:
            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )

        return age

    # Marks validation
    def clean_marks(self):
        marks = self.cleaned_data.get("marks")

        if marks < 0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks
