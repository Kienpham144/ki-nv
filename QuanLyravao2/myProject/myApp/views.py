from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import DS_DangKy, DS_NhatKy, DS_Lop
from .form import Dangki, Nhatki, NewsForm, DS_LopForm
from datetime import date
from .models import news
from django.db.models import Case, When, IntegerField
import requests
import os


# Decorator kiểm tra quyền admin
def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse('Bạn không phải là admin')
        return view_func(request, *args, **kwargs)
    return wrapped_view

#----------------------------------------------------------------------

# View đăng nhập
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác")
    return render(request, 'login.html')



# Hiển thị danh sách nhật ký cho admin
@login_required(login_url='login')
@admin_required
def diary_list(request):
    diary_list = DS_NhatKy.objects.all()
    context = {'diary_list': diary_list}
    html_template = loader.get_template('diary_list.html')
    return HttpResponse(html_template.render(context, request))

# View form nhật ký cho admin
@login_required(login_url='login')
@admin_required
def diary_form(request):
    if request.method == 'POST':
        form = Nhatki(request.POST)
        if form.is_valid():
            ma_hv = form.cleaned_data['Ma_hv']
            ten = form.cleaned_data['Ten']
            if DS_Lop.objects.filter(pk=ma_hv, Ten=ten).exists():
                noi_dung = form.cleaned_data['Noi_dung']
                diem = form.cleaned_data['Diem']
                selection = form.cleaned_data['selection']
                is_vipham = selection == 'is_vipham'
                is_thanhtich = not is_vipham
                DS_NhatKy.objects.create(
                    Ma_hv_id=ma_hv,
                    Ten=ten,
                    Noi_dung=noi_dung,
                    is_vipham=is_vipham,
                    is_thanhtich=is_thanhtich,
                    Diem=diem,
                    Ngay_dang_ky=date.today()
                )
                messages.success(request, "Nhật ký đã được thêm thành công")
                return redirect('diary_form')
            else:
                messages.error(request, "Mã học viên hoặc Tên không tồn tại")
    else:  
        form = Nhatki()
    return render(request, 'diary_form.html', {'form': form})

#----------------------------------------------------------------------

# View cho User

# Hiển thị danh sách chờ
@login_required(login_url='login')
def waiting_list(request):
    # Annotate sort_order và tính toán total_sum
    Waiting_list = DS_DangKy.objects.annotate(
        sort_order=Case(
            When(Thoigian_ra__gte='07:00:00', Thoigian_ra__lte='11:00:00', then=0),  # 7 AM - 11 AM
            When(Thoigian_ra__gte='14:00:00', Thoigian_ra__lte='17:00:00', then=2),  # 2 PM - 5 PM
            default=1,  # Các thời gian khác
            output_field=IntegerField()
        )
    ).order_by('sort_order', 'Thoigian_ra')  # Sắp xếp theo sort_order trước

    # Tính toán Phe_duyet dựa trên tổng điểm
    for item in Waiting_list:
        Pre = DS_NhatKy.objects.filter(Ten=item.Ten).aggregate(total_sum=Sum('Diem'))
        total_sum = Pre['total_sum']
        item.Phe_duyet = total_sum is None or total_sum >= 0

    # Chuẩn bị context cho template
    context = {'Waiting_list': Waiting_list}
    return render(request, 'waiting_list.html', context)


# Trang home
@login_required(login_url='login')
def home_view(request):
    if request.user.is_staff:
        # Nếu là admin, hiển thị trang Home dành cho Admin
        return render(request, 'home.html')
    else:
        # Nếu là người dùng thông thường, hiển thị trang Home dành cho User
        return render(request, 'home3.html')
    

# View cho thông báo kết quả (đang trống)
@login_required(login_url='login')
def notification(request):
    pass

# View form đăng ký ra vào doanh trại
@login_required(login_url='login')
def register_view(request):
    if request.method == 'POST':
        form = Dangki(request.POST)
        if form.is_valid():
            ma_hv = form.cleaned_data['Ma_hv']
            ten = form.cleaned_data['Ten']
            
            # Kiểm tra mã học viên và tên có tồn tại trong DS_Lop
            if DS_Lop.objects.filter(pk=ma_hv, Ten=ten).exists():
                try:
                    # Tạo bản ghi đăng ký mới
                    DS_DangKy.objects.create(
                        Ma_hv_id=ma_hv,
                        Ten=ten,
                        Don_vi=form.cleaned_data['Don_vi'],
                        Sdt_nguoi_than=form.cleaned_data['Sdt_nguoi_than'],
                        Ly_do=form.cleaned_data['Ly_do'],
                        Dia_diem=form.cleaned_data['Dia_diem'],
                        Ngay_dang_ky=date.today(),
                        Thoigian_ra=form.cleaned_data['Thoigian_ra'],
                        Thoigian_vao=form.cleaned_data['Thoigian_vao']
                    )
                    # Gửi thông báo thành công
                    messages.success(request, "Đăng ký thành công! Đồng chí vui lòng đợi hệ thống phê duyệt và xem kết quả tại danh sách lịch sử đăng ký. Cảm ơn!!!")
                    return redirect('home')  # Chuyển hướng về trang chủ
                except Exception as e:
                    messages.error(request, f"Đã xảy ra lỗi: {str(e)}")
            else:
                messages.error(request, "Mã học viên hoặc Tên không tồn tại trong hệ thống.")
    else:
        form = Dangki()
    
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def register_guide(request):
    return render(request, 'register_guide.html')



@login_required(login_url='login')  # Yêu cầu đăng nhập
def noiquy_ra_ngoai_view(request):
    return render(request, 'rules.html')  # Render template "noiquy_ra_ngoai.html"



login_required  # Yêu cầu người dùng đăng nhập
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()  # Lưu tin tức vào cơ sở dữ liệu
            return redirect('create_news')  # Chuyển hướng tới trang danh sách tin tức
    else:
        form = NewsForm()

    return render(request, 'create_news.html', {'form': form})

@login_required(login_url='login')  # Yêu cầu đăng nhập
def news_list   (request):
    news_items = news.objects.all().order_by('-post_date')  # Lấy tất cả bài viết, sắp xếp theo ngày đăng
    return render(request, 'news.html', {'news_items': news_items})

# Sửa lỗi ở đây
@login_required(login_url='login')
def game(request):
    return render(request, 'game.html')



@login_required
def home3_view(request):
    # Danh sách biểu tượng Font Awesome để chọn ngẫu nhiên
    icons = [
        "fas fa-user-circle", "fas fa-user-alt", "fas fa-user-tie", "fas fa-users", "fas fa-user-shield",
        "fas fa-user-secret", "fas fa-id-badge", "fas fa-user-ninja", "fas fa-user-astronaut", "fas fa-user-doctor",
        "fas fa-user-cog", "fas fa-user-edit", "fas fa-user-injured", "fas fa-user-lock", "fas fa-user-md",
        "fas fa-user-minus", "fas fa-user-plus", "fas fa-user-times", "fas fa-users-cog", "fas fa-user-graduate",
        "fas fa-user-hacker", "fas fa-user-headset", "fas fa-user-helmet-safety", "fas fa-user-hospital", 
        "fas fa-user-md-chat", "fas fa-user-priest", "fas fa-user-robot", "fas fa-user-sailboat", "fas fa-user-slash",
        "fas fa-user-video", "fas fa-user-alt-slash", "fas fa-user-chart", "fas fa-user-clock", "fas fa-user-cog",
        "fas fa-user-graduate", "fas fa-user-plus", "fas fa-user-gear", "fas fa-user-lock", "fas fa-user-location",
        "fas fa-user-md", "fas fa-user-suitcase", "fas fa-user-astronaut", "fas fa-user-business", "fas fa-user-friends",
        "fas fa-user-home", "fas fa-user-music", "fas fa-user-nurse", "fas fa-user-pilot", "fas fa-user-school",
        "fas fa-user-trophy"
    ]
    
    # Chọn ngẫu nhiên một biểu tượng
    random_icon = random.choice(icons)
    
    # Truyền dữ liệu vào context
    context = {
        'username': request.user.username,
        'icon': random_icon
    }
    
    return render(request, 'home3.html', context)




def ds_lop_list(request):
    # Lấy tất cả các bản ghi DS_Lop
    ds_lop = DS_Lop.objects.all()
    return render(request, 'ds_lop_list.html', {'ds_lop': ds_lop})


def add_ds_lop(request):
    if request.method == 'POST':
        form = DS_LopForm(request.POST)
        if form.is_valid():
            # Lưu đối tượng học viên
            ds_lop = form.save()

            # Thêm thông báo
            messages.success(request, f'Đã thêm học viên {ds_lop.Ten} vào danh sách lớp.')

            # Điều hướng về trang danh sách lớp
            return redirect('ds_lop_list')  # Chuyển về trang danh sách lớp
    else:
        form = DS_LopForm()

    return render(request, 'add_ds_lop.html', {'form': form})


def delete_ds_lop(request, pk):
    # Lấy đối tượng theo mã học viên (pk)
    ds_lop = get_object_or_404(DS_Lop, Ma_hv=pk)

    # Xóa đối tượng
    ds_lop.delete()

    # Hiển thị thông báo thành công
    messages.success(request, f'Đã xóa học viên {ds_lop.Ten} khỏi danh sách lớp.')

    # Chuyển hướng về danh sách lớp
    return redirect('ds_lop_list')






