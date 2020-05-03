from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    # 自定义字段，覆盖原模型字段
    # 一边适应前端要求两次密码验证
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:  # 定义了存储时指向的数据模型
        model = User  
        fields = ('username', 'email')  # 指定使用的字段

    def clean_password2(self):  # 密码验证函数，在视图调用is_valid()时调用
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    

class UserProfileForm(forms.ModelForm):  # 定义新家字段表单
    class Meta:
        model = UserProfile  # 指向存储数据的表单
        fields = ('birth', 'phone')