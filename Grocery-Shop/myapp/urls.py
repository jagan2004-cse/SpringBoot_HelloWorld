from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('products/',views.products, name='products'),
    path('products/<uuid:id>',views.product,name='product'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<uuid:id>/',views.add_to_cart,name='add_to_cart'),
    path('add_item/<uuid:id>/',views.add_item,name='add_item'),
    path('remove_item/<uuid:id>/',views.remove_item,name='remove_item'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
]