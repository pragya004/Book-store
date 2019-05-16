from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Book, post
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm


def index(request):
    book_details = Book.objects.order_by('id')
    context = {'book_details' : book_details}
    return render(request,'project_bstore/index.html',context)

def searching(request):

    criteria     = request.POST["criteria"]
    query_string = request.POST['query']

    if criteria == '1':
        books = Book.objects.filter(isbn=query_string)        
    elif criteria == '2':
        books = Book.objects.filter(title=query_string)
    else:
        books = Book.objects.filter(author=query_string)
        
    context = {"book_details": books}
        
    return render(request,"project_bstore/index.html",context)


def booksdetail(request):
    query_string = ''
    found_entries = None
    if ('q' in request.POST) and request.POST['q'].strip():
        query_string = request.POST['q']
        title = Book.objects.filter(title=query_string)
        authors = Book.objects.filter(author=query_string)
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

