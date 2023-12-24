from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from users.models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "role",
            "image",
            "is_blocked",
            "balance",
            "subscriptions",
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "role",
            "image",
            "is_blocked",
            "balance",
            "subscriptions",
        )

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        "email",
        "username",
        "password",
        "role",
        "image",
        "is_blocked",
        "balance",
    )
    list_filter = ("email", "username", "role", "created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "role",
                    "image",
                    "is_blocked",
                    "balance",
                    "subscriptions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password",
                    "role",
                    "image",
                    "is_blocked",
                    "balance",
                    "subscriptions",
                ),
            },
        ),
    )

    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
