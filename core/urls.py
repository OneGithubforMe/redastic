from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('ajax/', include('ajax.urls')),        # for all AJAX requests
    path('cart/', include('cart.urls')),
    path('category/', include('category.urls')),
    path('comment/', include('comment.urls')),
    path('product/', include('product.urls')),
    path('search/', include('search.urls')),
    path('rating/', include('rating.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)