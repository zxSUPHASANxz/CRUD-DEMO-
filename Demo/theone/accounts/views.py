
# --- IMPORTS ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from mechanics.models import Mechanic
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# --- ADMIN CHECK ---
def is_admin(user):
    return user.username == "Admin_THEONE"

# --- UPDATE MECHANIC (Admin) ---
@login_required
@user_passes_test(is_admin)
@require_POST
def update_mechanic(request, mechanic_id):
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    mechanic.name = request.POST.get("name", mechanic.name)
    mechanic.expertise = request.POST.get("expertise", mechanic.expertise)
    mechanic.phone = request.POST.get("phone", mechanic.phone)
    mechanic.save()
    return JsonResponse({"success": True})

# --- REGISTER VIEWS ---
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.filter(user=user).update(birth_date=form.cleaned_data['birth_date'])
            messages.success(request, "สมัครสมาชิกสำเร็จ!")
            return redirect('register_success')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def register_success(request):
    return render(request, 'accounts/register_success.html')



# --- ADMIN VIEWS ---
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all().select_related("profile")
    mechanics = Mechanic.objects.all()
    mechanics_users = User.objects.filter(profile__role="Mechanic").select_related("profile")
    return render(request, "accounts/admin_dashboard.html", {
        "users": users,
        "mechanics": mechanics,
        "mechanics_users": mechanics_users,
    })

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.username != "Admin_THEONE":  # กันไม่ให้ลบตัวเอง
        user.delete()
    return redirect("admin_dashboard")

@login_required
@user_passes_test(is_admin)
def delete_mechanic(request, mechanic_id):
    m = get_object_or_404(Mechanic, id=mechanic_id)
    m.delete()
    return redirect("admin_dashboard")


@login_required
@user_passes_test(is_admin)
@require_POST
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_username = request.POST.get("username")
    new_role = request.POST.get("role")

    if new_username:
        user.username = new_username
    if hasattr(user, "profile") and new_role:
        old_role = user.profile.role
        user.profile.role = new_role
        user.profile.save()
        # --- Mechanic sync logic ---
        from mechanics.models import Mechanic
        if new_role == "Mechanic":
            # Create Mechanic if not exists for this user
            mechanic, created = Mechanic.objects.get_or_create(name=user.username, defaults={"expertise": "", "phone": ""})
        elif new_role == "User":
            # Remove Mechanic if exists for this user
            Mechanic.objects.filter(name=user.username).delete()
    user.save()
    return JsonResponse({"success": True})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # ถ้าเป็น Admin → ไป Dashboard
            if user.username == "Admin_THEONE":
                return redirect("admin_dashboard")
            return redirect("home")  # user ปกติไปหน้า home
        else:
            messages.error(request, "เข้าสู่ระบบไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')



