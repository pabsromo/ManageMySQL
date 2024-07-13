from django import forms
from .models import Users
from .models import Servers


class UsersForm(forms.ModelForm):
    # due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Users
        fields = ["name", "email"]


class ServersForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = ["name", "user", "dbms"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the user field queryset to show user names
        self.fields["user"].queryset = Users.objects.all()
        self.fields["user"].label_from_instance = lambda obj: f"{obj.name}"
