from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *

User = get_user_model()
# Create your views here.
class LoginView(View):
    @method_decorator(never_cache)
    def get(self,request):
        return render(request, 'index.html')

    @method_decorator(never_cache)
    def post(self, request):
        username = request.POST['username']
        password =request.POST['password']
        user = authenticate(username=username, password= password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.role == 'admin':
                return redirect('admin/')
            elif user.role == 'seller':
                return redirect('seller-dashboard')
            elif user.role == 'buyer':
                return redirect('buyer-dashboard')

        else:
            messages.error(request, 'invalid username or password')  
            return render(request, 'index.html')
        
class SignupView(View):
    @method_decorator(never_cache)
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        role = request.POST['role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        image = request.FILES.get('image')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, phone=phone, role=role, password=password, image=image, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'User registered successfully. Please login.')
        return redirect('login')
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        response = redirect('login')
       
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    

class BuyerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('query', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        min_rooms = request.GET.get('min_rooms', '')
        location = request.GET.get('location', '')

        properties = Property.objects.filter(status="Approved")

        if query:
            properties = properties.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if location:
            properties = properties.filter(location__icontains=location)

        if min_price:
            try:
                properties = properties.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                properties = properties.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if min_rooms:
            try:
                properties = properties.filter(room__gte=int(min_rooms))
            except ValueError:
                pass

        context = {
            'properties': properties,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'min_rooms': min_rooms,
            'location': location
        }
        return render(request, 'dashboard.html', context)
    
class PropertyView(LoginRequiredMixin, View):
    def get(self, request, pk=None, **kwargs):
        if pk is None:
            pk = kwargs.get('pk')
        propert = Property.objects.get(id=pk)
        return render(request, 'property.html', {'propert': propert })
    
class SellerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'seller_dash.html')
    
    
class AddPropertyView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_property.html')
    def post(self, request):
        User = get_user_model()
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        location = request.POST['location']
        room = request.POST['room']
        bathroom = request.POST['bathroom']
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        user = request.user

        property = Property.objects.create(
            title=title,
            description=description,
            price=price,
            location=location,
            room=room,
            bathroom=bathroom,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            seller=user
        )
        property.save()
        messages.success(request, 'Property added successfully and is pending approval.')
        return redirect('add-property')
    
class PaymentView(LoginRequiredMixin,View):
    def get(self, request, pk=None, **kwargs):
        if pk is None:
            pk = kwargs.get('pk')
        property = Property.objects.get(id=pk)
        return render(request, "payment.html", {'property': property})
    
    def post(self, request,pk=None,**kwargs):
        property_id = request.POST['property_id']
        amount = request.POST['amount']
        if pk is None:
            pk = kwargs.get('pk')
        property = Property.objects.get(id=property_id)
        buyer = request.user

        payment = Payment.objects.create(
            property=property,
            buyer=buyer,
            amount=amount
        )
        payment.save()

        property.status = 'Sold'
        property.save()

        messages.success(request, 'Payment successful and property marked as sold.')
        return redirect('buyer-dashboard')
    
class ViewPropertyView(LoginRequiredMixin, View):
    def get(self, request):
        property = Property.objects.filter(seller=request.user).filter(Q(status="Approved")|Q(status="Pending"))
        return render(request, 'add_property.html', {'property': property })
    
class EditPropertyView(LoginRequiredMixin, View):
    def get(self, request, pk=None, **kwargs):
        return redirect('viewproperty')
    
    def post(self, request, pk=None, **kwargs):
        if pk is None:
            pk = kwargs.get('pk')
        property = Property.objects.get(id=pk)

        property.title = request.POST['title']
        property.description = request.POST['description']
        property.price = request.POST['price']
        property.location = request.POST['location']
        property.room = request.POST['room']
        property.bathroom = request.POST['bathroom']

        if 'image1' in request.FILES:
            property.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            property.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            property.image3 = request.FILES['image3']
        if 'image4' in request.FILES:
            property.image4 = request.FILES['image4']

        property.status = 'Pending'  
        property.save()

        messages.success(request, 'Property updated successfully and is pending approval.')
        return redirect('viewproperty')
    
class DeletePropertyView(LoginRequiredMixin, View):
    def post(self, request, pk=None, **kwargs):
        if pk is None:
            pk = kwargs.get('pk')
        property = Property.objects.get(id=pk)
        property.delete()

        messages.success(request, 'Property deleted successfully.')
        return redirect('viewproperty')
    
class ViewPaymentsView(LoginRequiredMixin, View):
    def get(self, request):
        payments = Payment.objects.filter(buyer=request.user)
        return render(request, 'my_payments.html', {'payments': payments })
    
class SellerPaymentsView(LoginRequiredMixin, View):
    def get(self, request):
        payments = Payment.objects.filter(property__seller=request.user)
        return render(request, 'view-payment.html', {'payments': payments })
    
class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('query', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        min_rooms = request.GET.get('min_rooms', '')
        location = request.GET.get('location', '')

        properties = Property.objects.filter(status='Approved')

        if query:
            properties = properties.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if location:
            properties = properties.filter(location__icontains=location)

        if min_price:
            try:
                properties = properties.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                properties = properties.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if min_rooms:
            try:
                properties = properties.filter(room__gte=int(min_rooms))
            except ValueError:
                pass

        context = {
            'properties': properties,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'min_rooms': min_rooms,
            'location': location
        }
        return render(request, 'dashboard.html', context)