from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout # setting up login step 1
from django.contrib import messages #flashes
from . models import Record
from . forms import AddRecordForm

def home(request):
    records = Record.objects.all()



    #check to see if person is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In ...")
            return redirect('home')
        else:
            messages.success(request, "There was an Error Logging in ...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})    

def logout_user(request):
    logout(request)
    messages.success(request,"You have been Logged Out...")
    return redirect('home')

def customer_record(request,pk):
    if request.user.is_authenticated:
        # Look Up Record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record}) 

    else: 
        messages.success(request,"You Must be Logged In...") 
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else: 
        messages.success(request, "You Must be Logged in to do that...")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
            if request.method == "POST":
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Record Added...")
                    return redirect()
            return render(request, 'home.html', {'form':form})     
    else:
        messages.success(request,"You need to be logged In...")
        return redirect('home')  
    


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form}) 
    else:
        messages.success(request, "Must be authenticated...")


