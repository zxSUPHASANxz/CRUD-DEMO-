from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Mechanic
from django import forms

class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = '__all__'

@login_required
def mechanic_list(request):
    items = Mechanic.objects.all()
    return render(request, 'mechanics/list.html', {'items': items})

@login_required
def mechanic_create(request):
    if request.method == 'POST':
        form = MechanicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mechanic_list')
    else:
        form = MechanicForm()
    return render(request, 'mechanics/form.html', {'form': form})

@login_required
def mechanic_edit(request, pk):
    item = get_object_or_404(Mechanic, pk=pk)
    if request.method == 'POST':
        form = MechanicForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('mechanic_list')
    else:
        form = MechanicForm(instance=item)
    return render(request, 'mechanics/form.html', {'form': form})

@login_required
def mechanic_delete(request, pk):
    item = get_object_or_404(Mechanic, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('mechanic_list')
    return render(request, 'mechanics/confirm_delete.html', {'item': item})
