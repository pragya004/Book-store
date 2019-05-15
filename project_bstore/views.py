from django.shortcuts import render,redirect
from .models import book_table
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required 
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    book_details = book_table.objects.order_by('id')
    context = {'book_details' : book_details}
    return render(request,'project_bstore/index.html',context)

def searching(request):
    query_string = ''
    found_entries = None
    if ('q' in request.POST) and request.POST['q'].strip():
    	query_string = request.POST['q']
    	title = book_table.objects.filter(title=query_string)
    	authors = book_table.objects.filter(authors=query_string)
    	context = {"book_details": list(title) + list(authors)}
    	return render(request,"project_bstore/index.html",context)

def booksdetail(request):
    query_string = ''
    found_entries = None
    if ('q' in request.POST) and request.POST['q'].strip():
        query_string = request.POST['q']
        title = book_table.objects.filter(title=query_string)
        authors = book_table.objects.filter(authors=query_string)
        context = {"book_details": list(title) + list(authors)}
        return render(request,"project_bstore/bookdetail.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created! You can now LogIn ')
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'project_bstore/register.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f' your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
 

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'project_bstore/profile.html',context)

@login_required
def sellbookpage(request):
    context = {
    'posts':post.objects.all()
    }
    return render(request,'project_bstore/sellbookpage.html',context)

class PostListView(ListView):
    model = post
    template_name = 'project_bstore/sellbookpage.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['picture','title','content']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['picture','title','content']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.seller:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/sellbookpage/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.seller:
            return True
        return False

