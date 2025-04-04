from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from core import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name="home"),
    path('mdv/', TemplateView.as_view(template_name='mdv/base.html'), name="mdv"),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('products/', include('products.urls', namespace="products")),
    path('orders/', include('orders.urls', namespace="orders")),
    path('store/', include('store.urls', namespace="store")),
    
    path('backoffice/', include('backoffice.urls', namespace="backoffice")),

    path('contact', TemplateView.as_view(template_name='contact.html'), name="contact"),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name="faq"),
    
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "store.views.error_404"
handler500 = "store.views.error_500"
