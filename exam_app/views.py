from django.shortcuts import render, redirect
from login_app.models import User
from .models import Trip
from django.contrib import messages
from datetime import datetime

# Create your views here.
def exam(request):
    if 'user_id' in request.session:
        return redirect('/exam/dashboard')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')
def index(request):
    if 'user_id' in request.session:
        this_user = User.objects.get(id = request.session['user_id'])
        context = {
            'this_user' : User.objects.get(id = request.session['user_id']),
            'all_trips' : Trip.objects.all()
        }
        return render(request, 'index_exam.html', context)
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def new_trip(request):
    if 'user_id' in request.session:
        context = {
            'this_user' : User.objects.get(id = request.session['user_id'])
        }
        return render(request, 'createtrip.html', context)
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/exam/trips/new')

    else:
        if 'user_id' in request.session:
            new_trip = Trip.objects.create(destination = request.POST['destination'], start_date = request.POST['start_date'], end_date = request.POST['end_date'], creator = User.objects.get(id = request.session['user_id']), plan = request.POST['plan'])
            new_trip.attendees.add(User.objects.get(id = request.session['user_id']))
            new_trip.save()
            return redirect('/exam/dashboard')
        else: 
            messages.error(request, "You must be logged in to view that page!")
            return redirect('/')

def edit_trip(request, num):
    if 'user_id' in request.session:
        this_trip = Trip.objects.get(id = num)
        this_user = User.objects.get(id = request.session['user_id'])
        if this_user.id == this_trip.creator.id:
            print(this_trip.destination)
            context = {
                'this_trip' : Trip.objects.get(id = num),
                'this_user' : User.objects.get(id = request.session['user_id'])
            }
            return render(request, "edittrip.html", context)
        else:
            return redirect(f'/exam/trips/view/{num}')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def update_trip(request, num):
    if 'user_id' in request.session:
        this_trip = Trip.objects.get(id = num)
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect(f'/exam/trips/edit/{num}')
        this_trip.destination = request.POST['destination']
        this_trip.start_date = request.POST['start_date']
        this_trip.end_date = request.POST['end_date']
        this_trip.plan = request.POST['plan']
        this_trip.save()
        return redirect('/exam/dashboard')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def view_trip(request, num):
    if 'user_id' in request.session:
        context = {
            'this_trip' : Trip.objects.get(id = num),
            'this_user' : User.objects.get(id = request.session['user_id'])
        }
        return render(request, "viewtrip.html", context)
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def delete_trip(request, num):
    if 'user_id' in request.session:
        this_trip = Trip.objects.get(id = num)
        this_trip.delete()
        return redirect('/exam/dashboard')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def join_trip(request, num):
    if 'user_id' in request.session:
        this_trip = Trip.objects.get(id = num)
        this_trip.attendees.add(User.objects.get(id = request.session['user_id']))
        this_trip.save()
        return redirect('/exam/dashboard')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')

def cancel_trip(request, num):
    if 'user_id' in request.session:
        this_trip = Trip.objects.get(id = num)
        this_trip.attendees.remove(User.objects.get(id = request.session['user_id']))
        this_trip.save()
        return redirect('/exam/dashboard')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')