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
        main_user = Account.objects.get(pk=request.user.pk)
        form = EditUserForm(request.POST, instance=main_user)
        new_photo = Photo.objects.create(account=main_user, photo=request.FILES['photo'])
        if form.is_valid():
            try:
                form.save()
            except:
                main_user.date_of_birth = None
                form.save()
            main_user.images.add(new_photo)
        return redirect('account', pk=main_user.pk)
