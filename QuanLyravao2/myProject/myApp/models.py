from django.db import models
from django.utils import timezone


class DS_Lop(models.Model):
    Ma_hv = models.IntegerField(primary_key=True, default=000) 
    Ten = models.CharField(max_length=100)
    Don_vi = models.CharField(max_length=100)
    Ngay_sinh = models.DateField()
    Que_quan = models.CharField(max_length=100)
from django.core.exceptions import ValidationError
from datetime import time

class DS_DangKy(models.Model):
    Ma_hv = models.ForeignKey(DS_Lop, on_delete=models.CASCADE, to_field='Ma_hv')
    Ten = models.CharField(max_length=100)
    Don_vi = models.CharField(max_length=100)
    Sdt_nguoi_than = models.CharField(max_length=15)
    Ly_do = models.TextField()
    Dia_diem = models.CharField(max_length=100)
    Ngay_dang_ky = models.DateField()
    Thoigian_ra = models.TimeField()
    Thoigian_vao = models.TimeField()
    Phe_duyet = models.BooleanField(default=False)

    def clean(self):
        # Validate Thoigian_ra to be either 7:00 AM or 2:00 PM
        if self.Thoigian_ra not in [time(7, 0), time(14, 0)]:
            raise ValidationError("Thời gian ra chỉ được chọn 7:00 sáng hoặc 2:00 chiều, thời gian vào là 11:00 sáng và 5:00 chiều.")

        # Validate Thoigian_vao to be either 11:00 AM or 5:00 PM
        if self.Thoigian_vao not in [time(11, 0), time(17, 0)]:
            raise ValidationError("Thời gian ra chỉ được chọn 7:00 sáng hoặc 2:00 chiều, thời gian vào là 11:00 sáng và 5:00 chiều.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call the clean method before saving
        super().save(*args, **kwargs)

class DS_NhatKy(models.Model):
    Ma_hv = models.ForeignKey(DS_Lop, on_delete=models.CASCADE, to_field='Ma_hv') 
    Ten = models.CharField(max_length=100)
    Noi_dung = models.CharField(max_length=256)
    Ngay_dang_ky = models.DateField()
    is_vipham = models.BooleanField(default=False)
    is_thanhtich = models.BooleanField(default=False)
    Diem = models.IntegerField()

     


class news(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    link = models.URLField()




    
