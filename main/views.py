from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Stock
import bcrypt
import requests

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "CEBT02OMR2LTI43Q"



# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    else:
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
                first_name = f_name,
                last_name = l_name,
                email = email,
                password = new_password
            )
        request.session['userid'] = user.id
        return redirect('/overview')

def login(request):
    user_email = User.objects.filter(email = request.POST['email'])
    if user_email:
        logged_user = user_email[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/overview')
    else:
        messages.error(request, "Incorrect email or password")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def overview(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to access this page")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userid']),
        }
        return render(request, 'overview.html', context)

def add_fund(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to access this page")
        return redirect('/')
    else:
        if request.method == "POST":
            this_user = User.objects.get(id=request.session['userid'])
            this_user.ballance += int(request.POST['money'])
            this_user.save()
            return redirect('/overview')
        else:
            return render(request, 'add_money.html')

def activity(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to access this page")
        return redirect('/')
    else:
        return render(request, 'activity.html')

def stock(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to access this page")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userid'])
        }
        return render(request, 'stock.html', context)

def add_stock(request):
    stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": request.POST['stock_name'],
    "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    before_yesterday = data_list[1]
    yesterday_closing_price = yesterday_data["4. close"]
    before_yesterday_closing_price = before_yesterday["4. close"]
    difference = float(yesterday_closing_price) - float(before_yesterday_closing_price)
    x = round(difference, 2)
    print(difference)
    
    this_user = User.objects.get(id=request.session['userid'])
    Stock.objects.create(
        stock=request.POST['stock_name'],
        price=yesterday_closing_price,
        difference = x,
        user=this_user
    )
    this_user.ballance -= float(yesterday_closing_price)
    this_user.save()
    return redirect('/stock')

def sell_stock(request, id):
    if 'userid' not in request.session:
        messages.error(request, "Please login to sell a stock")
        return redirect('/')
    else:
        stock1 = Stock.objects.get(id=id)
        this_user = User.objects.get(id=request.session['userid'])
        this_user.ballance += int(stock1.price)
        this_user.save()
        stock1.delete()
        return redirect('/stock')



def benefit(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to access this page")
        return redirect('/')
    else:
        return render(request, 'benefit.html')