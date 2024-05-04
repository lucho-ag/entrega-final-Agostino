from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Mesa, Reserva, Mesero, Avatar
from .forms import ReservaSearchForm, MesaSearchForm, UserEditForm, AvatarCreateForm

def home_view(request):
    return render(request, "Restaurant/home.html")

def menu_view(request):
    return render(request, "Restaurant/menu.html")

# --------------------RESERVAS--------------------

class ReservaCreateView(LoginRequiredMixin,CreateView):
    model = Reserva
    template_name = 'Restaurant/reserva_form.html'
    fields = ['nombre_de_usuario', 'mesa', 'fecha', "hora_inicio"]
    success_url = reverse_lazy('reserva-lista')
    
class ReservaListView(LoginRequiredMixin,ListView):
    model = Reserva
    template_name = 'Restaurant/reserva_list.html'
    context_object_name = 'reservas'

class ReservaDetailView(LoginRequiredMixin,DetailView):
    model = Reserva
    template_name = 'Restaurant/reserva_detail.html'
    context_object_name = 'reserva'

class ReservaUpdateView(LoginRequiredMixin,UpdateView):
    model = Reserva
    template_name = 'Restaurant/reserva_form.html'
    fields = ['nombre_de_usuario', 'mesa', 'fecha', "hora_inicio"]
    context_object_name = 'reserva'
    success_url = reverse_lazy('reserva-lista')

class ReservaDeleteView(LoginRequiredMixin,DeleteView):
    model = Reserva
    template_name = 'Restaurant/reserva_delete.html'
    success_url = reverse_lazy('reserva-lista')

@login_required
def reserva_busqueda(request):
    if request.method == "GET":
        form = ReservaSearchForm
        return render(request, "Restaurant/reserva_busqueda.html", context={"search_form": form })
    elif request.method == "POST":
        form = ReservaSearchForm(request.POST)
        if form.is_valid():
            nombre_de_usuario = form.cleaned_data['nombre_de_usuario']
        reservas_del_usuario = Reserva.objects.filter(nombre_de_usuario=nombre_de_usuario).all()
        contexto_dict = {"reservas": reservas_del_usuario}
        return render(request, "Restaurant/reserva_list.html", contexto_dict)
    
# --------------------MESAS--------------------

class MesaCreateView(LoginRequiredMixin,CreateView):
    model = Mesa
    template_name = 'Restaurant/mesa_form.html'
    fields = ['numero', 'disponible', 'capacidad']
    success_url = reverse_lazy('mesa-lista')
    
class MesaListView(LoginRequiredMixin,ListView):
    model = Mesa
    template_name = 'Restaurant/mesa_list.html'
    context_object_name = 'mesas'

class MesaUpdateView(LoginRequiredMixin,UpdateView):
    model = Mesa
    template_name = 'Restaurant/mesa_form.html'
    fields = ['numero', 'disponible', 'capacidad']
    context_object_name = 'mesa'
    success_url = reverse_lazy('mesa-lista')

class MesaDeleteView(LoginRequiredMixin,DeleteView):
    model = Mesa
    template_name = 'Restaurant/mesa_delete.html'
    success_url = reverse_lazy('mesa-lista')
 
@login_required   
def mesa_busqueda(request):
    if request.method == "GET":
        form = MesaSearchForm
        return render(request, "Restaurant/mesa_busqueda.html", context={"search_form": form })
    elif request.method == "POST":
        form = MesaSearchForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            mesas = Mesa.objects.filter(numero=numero).all()
            contexto_dict = {"mesas": mesas}
            return render(request, "Restaurant/mesa_list.html", contexto_dict)
        else:
            return render(request, "Restaurant/mesa_busqueda.html", context={"search_form": form })
            
        
    
# --------------------MESEROS--------------------

class MeseroCreateView(LoginRequiredMixin,CreateView):
    model = Mesero
    template_name = 'Restaurant/mesero_form.html'
    fields = ['nombre', 'mesa_asignada']
    success_url = reverse_lazy('mesero-lista')
    
class MeseroListView(LoginRequiredMixin,ListView):
    model = Mesero
    template_name = 'Restaurant/mesero_list.html'
    context_object_name = 'meseros'

class MeseroUpdateView(LoginRequiredMixin,UpdateView):
    model = Mesero
    template_name = 'Restaurant/mesero_form.html'
    fields = ['nombre', 'mesa_asignada']
    context_object_name = 'mesero'
    success_url = reverse_lazy('mesero-lista')

class MeseroDeleteView(LoginRequiredMixin,DeleteView):
    model = Mesero
    template_name = 'Restaurant/mesero_delete.html'
    success_url = reverse_lazy('mesero-lista')

#--------------------USUARIOS--------------------

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

def user_creation_view(request):
    if request.method == "GET":
        form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)     
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    return render(request, "Restaurant/crear_usuario.html", {"form": form})

def user_login_view(request):
    if request.method == "GET":
        form = AuthenticationForm()
    elif request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None:
                login(request, user)
                return redirect("home")

    return render(request, "Restaurant/login.html", {"form": form})

def user_logout_view(request):
    logout(request)
    return redirect("login")

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "Restaurant/user_edit_form.html"
    success_url = reverse_lazy("home")
    
    def get_object(self):
        return self.request.user

def avatar_view(request):
    if request.method == "get":
        contexto = {"avatar": AvatarCreateForm()}
    else:
        form = AvatarCreateForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            avatar_existente = Avatar.objects.filter(user=request.user)
            avatar_existente.delete()
            nuevo_avatar = Avatar(image=image, user= request.user)
            nuevo_avatar.save()
            return redirect("home")
        else:
            contexto = {"avatar": form}
    
    return render(request, "restaurant/avatar_create.html", context=contexto)

def about_view(request):
    return render(request, "Restaurant/about_me.html")