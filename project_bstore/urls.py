from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('home/',views.index, name='bstore_home'),
    path('searching/', views.searching, name="searching"),
    path('register/', views.register, name='bstore_register'),
    path('login/',auth_views.LoginView.as_view(template_name='project_bstore/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='project_bstore/logout.html'),name='logout'),
    path('profile/',views.profile,name='profile'),
    path('booksdetail/', views.booksdetail, name="booksdetail"),
    path('sellbookpage/', PostListView.as_view(), name="sellbookpage"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
