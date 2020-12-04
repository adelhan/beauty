from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import CategoryListView, CategoryCreateView, CategoryDetailView, PlaceListView, PlaceCreateView, \
    PlaceDetailView, ApplicationListView, ApplicationDetailView, ApplicationCreateView, MasterCreateView, \
    MasterListView, CommentViewSet

router = DefaultRouter()
# router.register('applications', CategoryListView)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('category/', CategoryListView.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('category/<slug:slug>/', CategoryDetailView.as_view()),
    path('accounts/', include('account.urls')),
    path('place/', PlaceListView.as_view()),
    path('place/create/', PlaceCreateView.as_view()),
    path('category/place/<slug:slug>/', PlaceDetailView.as_view()),
    path('applications/', ApplicationListView.as_view()),
    path('category/place/master/applications/<slug:slug>/', ApplicationDetailView.as_view()),
    path('application/create/', ApplicationCreateView.as_view()),
    path('masters/', MasterListView.as_view()),
    path('master/create/', MasterCreateView.as_view())
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)