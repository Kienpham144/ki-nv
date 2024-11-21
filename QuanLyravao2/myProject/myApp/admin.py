from django.contrib import admin
from .models import DS_DangKy, DS_Lop, DS_NhatKy, news

class DS_Dangky_admin(admin.ModelAdmin):
    list_display = ['Ten', 'Don_vi', 'Sdt_nguoi_than', 'Ly_do', 'Dia_diem',
                    'Ngay_dang_ky', 'Thoigian_ra', 'Thoigian_vao', 'Phe_duyet']

class Ds_Lop_admin(admin.ModelAdmin):
    list_display = ['Ma_hv', 'Ten', 'Don_vi', 'Ngay_sinh', 'Que_quan']

class Ds_NhatKy_admin(admin.ModelAdmin):
    list_display = ['Ngay_dang_ky', 'Ma_hv_id', 'Ten', 'Noi_dung', 'is_vipham', 'is_thanhtich', 'Diem']

class newsAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_date', 'link')  # Hiển thị các trường trong danh sách
    search_fields = ('title', 'content')  # Các trường có thể tìm kiếm
    list_filter = ('post_date',)  # Bộ lọc cho trường post_date
    ordering = ('-post_date',)  # Sắp xếp theo ngày đăng mới nhất
    readonly_fields = ('post_date',)  # Chỉ đọc với trường post_date

admin.site.register(DS_NhatKy, Ds_NhatKy_admin)
admin.site.register(DS_Lop, Ds_Lop_admin)
admin.site.register(DS_DangKy, DS_Dangky_admin)
admin.site.register(news, newsAdmin)
