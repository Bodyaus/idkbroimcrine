from django.shortcuts import render
from .models import Hotel, Booking

from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from .forms import BookingForm
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Hotel, Booking
from .forms import BookingForm


def home(request):
    hotels = Hotel.objects.all().order_by('-date_posted')
    return render(request, 'mysite/home.html', {'hotels': hotels})


def home2(request):
    # тут ваша головна сторінка готелю
    return render(request, 'mysite/home-2.html')


@login_required
def create_booking(request, room_id=None):
    # якщо хочете бронювати конкретний номер з головної сторінки — передавайте room_id
    initial = {}
    if room_id:
        room = get_object_or_404(Hotel, pk=room_id)
        initial['room'] = room

    if request.method == "POST":
        form = BookingForm(request.POST, initial=initial)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.full_clean()          # викликає clean() з моделі
                booking.save()

                # відправка листа
                send_mail(
                    subject="Підтвердження бронювання",
                    message=(
                        f"Добрий день, {request.user.username}!\n\n"
                        f"Ви успішно забронювали:\n"
                        f"Номер: {booking.room.title}\n"
                        f"Період: {booking.start_date} – {booking.end_date}\n\n"
                        f"Дякуємо за вибір!"
                    ),
                    from_email='andrijlogika@gmail.com',
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

                return redirect('home')  # або створіть окрему сторінку "успішно заброньовано"

            except ValidationError as e:
                form.add_error(None, e.messages)

    else:
        form = BookingForm(initial=initial)

    return render(request, 'mysite/home-3.html', {'form': form})