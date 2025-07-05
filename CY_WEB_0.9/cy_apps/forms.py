# cy_apps/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    # 原有注册表单代码...
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=50, required=True)  # 确保有此字段
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入的密码不匹配")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# 新增：登录表单类
class UserLoginForm(AuthenticationForm):
    """用户登录表单，继承自Django内置的AuthenticationForm"""
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ('username', 'password')


# cy_apps/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile  # 假设Profile模型已定义


class UserProfileForm(forms.ModelForm):
    nickname = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '输入你的昵称'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'nickname']  # 包含昵称字段

    # ========== 新增 __init__ 方法 ==========
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 必须先调用父类初始化

        # 判断当前用户是否是管理员（超级用户）
        if not self.instance.is_superuser:
            # 非管理员：设置用户名只读 + 灰色样式
            self.fields['username'].widget.attrs.update({
                'readonly': 'readonly',  # 核心：前端不可编辑
                'class': 'bg-gray-100 cursor-not-allowed',  # Tailwind样式：灰色背景+禁止光标
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # 保存昵称到Profile模型
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = self.cleaned_data['nickname']
            profile.save()
        return user