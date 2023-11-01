from django import forms
from django.core.exceptions import ValidationError

from catalog.models import TaskType


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
    # task_type = forms.ChoiceField(
    #     label="Task Type",
    #     required=False,
    #     choices=TaskType.objects.values_list()
    # )
