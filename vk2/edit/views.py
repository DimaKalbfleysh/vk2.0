from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from edit.forms import EditUserForm, PhotoForm
from account.models import Account, Photo


class EditUser(View):
    def get(self, request):
        main_user = Account.objects.get(username=request.user)
        form = EditUserForm(instance=main_user)
        photo_form = PhotoForm(instance=main_user)
        return render(request, 'edit/edit_user.html', context={'main_user': main_user,
                                                               'form': form,
                                                               'photo_form': photo_form})

    def post(self, request):
        user = Account.objects.get(username=request.user)
        form = EditUserForm(request.POST, instance=user)
        all_photo_user = list(Photo.objects.all())
        new_id_photo = all_photo_user[0].id_photo + 1
        new_photo = Photo.objects.create(id_photo=new_id_photo)
        if form.is_valid():
            try:
                form.save()
            except:
                user.date_of_birth = None
                form.save()
            new_photo.photo = request.FILES['photo']
            new_photo.account = user
            new_photo.save()
            user.images.add(new_photo)
        return redirect('account', pk=user.pk)
