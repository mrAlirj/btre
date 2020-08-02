from django.shortcuts import render ,redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(user_id=user_id , listing_id=listing_id)
            if has_contacted:
                messages.error(request , 'you have already make an inquryy for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing , listing_id=listing_id , name=name , phone=phone , email = email
                           , message=message , user_id=user_id )

        contact.save()

        send_mail(
            'property listing inqury',
            'there has been an inqury for' + listing + 'sign into the admin panel for more info',
            'aranjbar1372@gmail.com',
            [realtor_email , 'techguysinfo@gmail.com'],
            fail_silently=False
        )

        messages.success(request , 'your request has been submitted, a realtor will get back to you soon')

        return redirect('/listings/'+listing_id)


