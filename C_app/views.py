from django.shortcuts import render,redirect
from . import models
from django.db.models import Q
import os
# Create your views here.
def home(request):
    if request.method == "GET":
        src = request.GET.get('src')
        if src:
            profile = models.profile.objects.filter(name__icontains = src)
        elif src == None:
            profile = models.profile.objects.all()
        else:
            profile = models.profile.objects.all()
    return render(request,'home.html',locals())
def create(request):
    if request.method == 'POST':
        Name = request.POST.get('Name')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        religion = request.POST.get('religion')
        blood_group = request.POST.get('blood_group')
        date_of_birth = request.POST.get('date_of_birth')
        is_alive = request.POST.get('is_alive')
        if models.profile.objects.filter(Q(email=email)).exists():
            return redirect('create')
        elif models.del_profile.objects.filter(Q(email=email)).exists():
            return redirect('create')
        else:

            if image:
                if is_alive == "1":
                    profile = models.profile.objects.create(
                        name=Name,image=image,email=email,gender=gender,address=address,religion=religion,blood_group=blood_group,date_of_birth=date_of_birth,is_alive=True
                    )
                    profile.save()
                    return redirect('home')
                else:
                    profile = models.profile.objects.create(
                        name=Name,image=image,email=email,gender=gender,address=address,religion=religion,blood_group=blood_group,date_of_birth=date_of_birth
                    )
                    profile.save()
                    return redirect('home')
            else:
                if is_alive == "1":
                    profile = models.profile.objects.create(
                        name=Name,email=email,gender=gender,address=address,religion=religion,blood_group=blood_group,date_of_birth=date_of_birth,is_alive=True
                    )
                    profile.save()
                    return redirect('home')
                else:
                    profile = models.profile.objects.create(
                        Name=Name,email=email,gender=gender,address=address,religion=religion,blood_group=blood_group,date_of_birth=date_of_birth
                    )
                    profile.save()
                    return redirect('home')
    return render(request,'create.html')

def profile(request,id):
    profile =models.profile.objects.get(id=id)
    return render(request,'profile.html',locals())

def update(request,id):
    profile =models.profile.objects.get(id=id)
    if request.method == 'POST':
        Name = request.POST.get('Name')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        religion = request.POST.get('religion')
        blood_group = request.POST.get('blood_group')
        date_of_birth = request.POST.get('date_of_birth')
        is_alive = request.POST.get('is_alive')
        if image == None:
            pass
        elif  profile.image !='def.png':
            os.remove(profile.image.path)
            profile.image = image
        else:
            profile.image = image
        profile.name=Name
        profile.email=email
        profile.gender=gender
        profile.address=address
        profile.religion=religion
        profile.date_of_birth=date_of_birth
        profile.blood_group=blood_group
        profile.is_alive=is_alive
        profile.save()
        return redirect('home')
    return render(request,'update.html',locals())

def delete(request,id):
    profile = models.profile.objects.get(id=id)
    del_pro = models.del_profile.objects.create(
        name = profile.name,
        image = profile.image,
        email = profile.email,
        gender = profile.gender,
        address = profile.address,
        religion = profile.religion,
        blood_group = profile.blood_group,
        date_of_birth = profile.date_of_birth,
        is_alive = profile.is_alive,
        previous_id = profile.id,
    )
    profile.delete()
    return redirect('home')

def delete_profiles(request):
    profile = models.del_profile.objects.all()
    if request.method == "GET":
        src = request.GET.get('src')
        if src:
            profile = models.del_profile.objects.filter(name__icontains = src)
        elif src == None:
            profile = models.del_profile.objects.all()
        else:
            profile = models.del_profile.objects.all()
    return render(request,'delete.html',locals())

def delete_permanent(request,id):
    profile = models.del_profile.objects.get(id=id)
    if profile.image!='def.png':
        os.remove(profile.image.path)
    profile.delete()
    return redirect('home')

def restore_profiles(request,id):
    profile = models.del_profile.objects.get(id=id)
    restore = models.profile.objects.create(
        name = profile.name,
        image = profile.image,
        email = profile.email,
        gender = profile.gender,
        address = profile.address,
        religion = profile.religion,
        blood_group = profile.blood_group,
        date_of_birth = profile.date_of_birth,
        is_alive = profile.is_alive,
        id = profile.id,
    )
    return redirect('home')
