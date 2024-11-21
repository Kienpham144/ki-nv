from django import forms
from .models import DS_DangKy, news, DS_Lop
class Dangki(forms.Form):
    Ma_hv = forms.IntegerField(label = 'Mã số học viên', required=True)
    Ten = forms.CharField (label = 'Họ và tên', max_length = 100, required=True)
    Don_vi = forms.CharField (label = 'Đơn vị', max_length = 100, required=True)
    Sdt_nguoi_than = forms.CharField (label = 'Số điện thoại người thân', max_length = 100, required=True)
    Ly_do = forms.CharField (label = 'Lý do', max_length = 100, required=True)
    Dia_diem = forms.CharField (label = 'Địa điểm', max_length = 100, required=True)
    Thoigian_ra = forms.TimeField (label = 'Thời gian ra', required=True)
    Thoigian_vao = forms.TimeField (label = 'Thời gian vào', required=True)
class Nhatki(forms.Form):
    Ma_hv = forms.CharField (label = 'Mã số học viên', max_length = 100, required=True)
    Ten = forms.CharField (label = 'Họ và tên', max_length = 100, required=True)
    Noi_dung = forms.CharField (label = 'Nội dung', max_length = 100, required=True)
    Diem = forms.IntegerField(label='Điểm',required=True)
    CHOICES = [
        ('is_thanhtich', 'Là thành tích'),
        ('is_vipham', 'Là lỗi vi phạm'),
    ]
    selection = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Là thành tích hay vi phạm",
        required=True,
        initial='is_thanhtich'
    )

class NewsForm(forms.ModelForm):
    class Meta:
        model = news
        fields = ['title', 'content', 'image_url', 'link']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 50}),  # Giới hạn chiều cao cho textarea
        }



class DS_LopForm(forms.ModelForm):
    class Meta:
        model = DS_Lop
        fields = ['Ma_hv', 'Ten', 'Don_vi', 'Ngay_sinh', 'Que_quan']