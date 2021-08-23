from django.shortcuts import render, redirect
from .models import User, Product, Review, UserImage, Subscription
from .forms import *
import bcrypt


# Create your views here.
def disp_home(request):

    if 'user_id' in request.session:

        user_obj = User.objects.get(id=request.session['user_id'])
        subscript_objs = Subscription.objects.all()

        context = {
            'user' : user_obj,
            'subscriptions' : subscript_objs,
        }

        return render(request, "home.html",context)

    else:
        context = {
            "login_msg": "Please log in first."
        }

        return render(request, "login.html", context) 



def disp_cart(request):

    print("Displaying Cart page")  

    if 'user_id' in request.session:
        if request.method == "POST":
            print("Displaying Cart page for logged in user")  

            user_obj = User.objects.get(id=request.session['user_id'])
            subscript_obj = Subscription.objects.get(id=request.post['sel_subscription'])

            context = {
                'user' : user_obj,
                'subscriptions' : subscript_obj,
            }

            return render(request, "cart.html",context)
        else:
            redirect("home")
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context) 


def submit_order(request):
    print("Order placed!")

    return redirect("cart")


def  disp_option(request,optionNum):  

    print("Displaying Option page")  

    if 'user_id' in request.session:

        print("Displaying Option page for logged in user")  

        user_obj = User.objects.get(id=request.session['user_id'])
        subscript_obj = Subscription.objects.get(option_id = optionNum)
        review_objs = Review.objects.filter(review_of = subscript_obj)
        userimage_objs = UserImage.objects.filter(image_for_review = review_objs)

        context = {
            'user' : user_obj,
            'subscriptions' : subscript_obj,
            'reviews' : review_objs,
            'user_images' : userimage_objs,
        }

        return render(request, "option.html", context)


    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context) 


def add_review(request):

    print("Displaying Option page")  

    if 'user_id' in request.session:
        if request.method == "POST":
            print("Displaying Option page for logged in user") 

            optionNum = request.POST['optionNum']

            user_obj = User.objects.get(id=request.session['user_id'])
            subscript_obj = Subscription.objects.get(option_id = optionNum)

            Review.objects.create(
                comment = request.POST['comment'],
                submited_by = user_obj,
                review_of = subscript_obj,
                score = request.POST['score']
            )

        return redirect("option" + str(optionNum))


    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context) 



def add_user_image(request):

    print("Adding user image to option page")  

    if 'user_id' in request.session:

        if request.method == "POST":
            print("Adding user image to option page for logged in user")  

            optionNum = request.POST['optionNum']
            user_obj = User.objects.get(id=request.session['user_id'])
            subscript_obj = Subscription.objects.get(option_id = optionNum)
            review_objs = Review.objects.filter(review_of = subscript_obj)

            UserImage.objects.create(
                user_image_path = "",
                user_image_alt = "Uploaded image for Option " + str(optionNum),
                image_for_review = review_objs.last(),
                image_from_user = user_obj,
            )

        return redirect("option" + str(optionNum))


    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context) 

def registration(request):
    # creates a form
    form = RegistrationForm()
    context = {
        "RegForm": form,
    }
    return render(request, "register.html", context)

def create_user(request):
    if request.method == 'POST':
        # sends form data to backend for validation
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            # creates object but allows for further editing of object attributes
            new_user = reg_form.save(commit=False)
            hash_pw = bcrypt.hashpw(reg_form.cleaned_data['password'].encode(), bcrypt.gensalt()).decode()
            new_user.password = hash_pw
            new_user.save()
            # stores the logged in user's id for usage elsewhere in app
            request.session['logged_user_id'] = new_user.id
            return redirect(f'/user/{new_user.id}')
        else:
            # if data does not pass validations, render form along with errors
            return render(request, 'register.html', context={'RegForm': reg_form})