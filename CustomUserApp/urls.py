from django.urls import path 
from CustomUserApp.views import*
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('Register/',Signup,name='Signup'),
    path('login/',Signin,name="Signin"),
    path('activate/<uidb64>/<str:token>/',activate, name='activate'),
    path('reset_password/',forgot_password,name="forgot_password"),
    path('forgot_password_done/<uidb64>/<str:token>/',forgot_password_done,name='forgot_password_done'),
    path('logout/',signout,name='signout'),
    path('Change_password/',change_password,name='change_password_request'),
    path("dashboard/",dashboard,name="dashboard"),
    path('',Home,name='Home'),
    path('AddToCart/<int:id>',AddToCart,name='AddToCart'),
    path('AboutUs/',AboutUs,name='AboutUs'),
    path('UpdateProfile/',UpdateProfile,name='UpdateProfile'),
    path('UpdateUserData/<int:id>',UpdateUserData,name='UpdateUserData'),
    path('DeleteUserData/<int:id>',DeleteUserData,name='DeleteUserData'),
    path('CheckOut/',CheckOut,name='CheckOut'),
    path('RemoveItem/<int:id>',RemoveItem,name='RemoveItem'),
    path('BuyNow/<int:id>',BuyNow,name='BuyNow'),
    path('BuyAll/',BuyAll,name='BuyAll'),
    path('Payment/',create_checkout_session_for_all,name='create_checkout_session_for_all'),
    path('Payment/<int:id>',create_checkout_session_for_one,name='create_checkout_session_for_one'),
    path('success/',success,name='success'),
    path('cancel/',cancel,name="cancel"),
    path('get_invoice/<id>',get_invoice,name='get_invoice'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)