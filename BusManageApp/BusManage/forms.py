from django import forms
from .models import Customer
from django.contrib.auth.hashers import check_password
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'address', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        # Kiểm tra nếu instance có hình ảnh avatar thì hiển thị
        if self.instance and self.instance.avatar:
            self.fields['avatar'].widget.attrs.update({
                'class': 'form-control',
                'style': 'margin-top: 10px;',
            })
            self.fields['avatar'].label = "Cập nhật ảnh đại diện (hình hiện tại bên dưới)"

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Mật khẩu cũ')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Mật khẩu mới')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Xác nhận mật khẩu mới')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        user = Customer.objects.get(email=self.initial['email'])  # Lấy user từ email đã lưu trong session
        if not check_password(old_password, user.password):
            raise forms.ValidationError("Mật khẩu cũ không chính xác.")

        if new_password != confirm_password:
            raise forms.ValidationError("Mật khẩu mới và xác nhận không khớp.")
