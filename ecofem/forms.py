from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "organisation", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "organisation": forms.TextInput(
                attrs={"placeholder": "Organisation (optional)"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "How can we help?"}),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Tell us about your interest in EcoFem…",
                    "rows": 6,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError("Please provide at least 20 characters.")
        return message
