
from django.http import HttpResponse
from django.shortcuts import redirect, render
#import all of your models
from .models import Pokemon, Join
from django.contrib import messages
#import all your forms 
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
import requests as r


# def index(request):
#     # posts = Post.objects.all()
    
#     # context = {'posts':posts}
#     return render(request, 'pokemon/homepg.html', context={})

def homePg(request):
    return render(request, 'pokemon/homepg.html', context={})

def about(request):
    return render(request, 'pokemon/about.html', context={})

def signIn(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        
        user = authenticate(request , username=username, password=password1)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'{username} is now signed in!')
            return redirect('home')
        else:
            messages.warning(request, f'Login Information is incorrect')
    
    return render(request, 'pokemon/signin.html', context = {})

def signUp(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, f'Account Created {user}!')
            return redirect('signin')
        else:
            messages.warning(request, f'Invalid Attempt')
            print('invalid', form.errors)
    else:
        print('get req submitted', request.method)            
        
    return render(request, 'pokemon/signup.html', context = {'form':form})


def logOut(request):
    logout(request)
    return redirect('signin')


def getPokemon(request):
    pokemon = {}
    if request.method == "POST":
        name = request.POST.get('poke')
        response = r.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        data = response.json()
        if response.status_code == 200:    
             pokemon = {
                 'name': data['name'],
                 "img": data['sprites']['front_shiny'],
                 'id' : data['id']
                 }
        else:
             messages.warning(request, 'There is an issue with the pokemon search function')
            
    
    
    return render(request, 'pokemon/catch.html', context={'pokemon': pokemon})




def addTeam(request, post_id):
    try: 
        p = Pokemon.objects.get(id=post_id)
    
    except:
        p = Pokemon()
        res = r.get(f'https://pokeapi.co/api/v2/pokemon/{post_id}')
        data = res.json()
        p.name = data['name']
        p.id = data['id']
        p.img = data['sprites']['front_shiny']
        p.save()
    
    j = Join()
    j.user = request.user
    j.pokemon = p
    j.save()
    
    
    return redirect('my-team')



def myTeam(request):
    j = Join.objects.filter(user = request.user.id).all()
    
    pokemon =[Pokemon.objects.get(id = p.pokemon.id) for p in j]  
    
    return render(request, 'pokemon/myTeam.html', context = {'pokemon': pokemon})  