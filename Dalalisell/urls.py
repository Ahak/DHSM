
from django.urls import path
from . import views


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),   
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('buyer-dashboard/', views.BuyerDashboardView.as_view(), name='buyer-dashboard'),
    path('seller-dashboard/', views.SellerDashboardView.as_view(), name='seller-dashboard'),
    path('add-property/', views.AddPropertyView.as_view(), name='add-property'),
    path('property/<int:pk>', views.PropertyView.as_view(), name='property'),
    path('payment/<int:pk>', views.PaymentView.as_view(), name='payment'),
    path('view_property', views.ViewPropertyView.as_view(), name='viewproperty'),
    path('edit-property/<int:pk>', views.EditPropertyView.as_view(), name='edit-property'),
    path('delete-property/<int:pk>', views.DeletePropertyView.as_view(), name='delete-property'),
    path('my-payments/', views.ViewPaymentsView.as_view(), name='my-payments'),
    path('seller-payments/', views.SellerPaymentsView.as_view(), name='seller-payments'),
] 