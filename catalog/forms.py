from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from catalog.models import TaskType, Employee


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search task type"}
        )
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search task by name"}
        )
    )


class EmployeeSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by username"}
        )
    )


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )


class EmployeePositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["position"]


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search task type"}
        )
    )
