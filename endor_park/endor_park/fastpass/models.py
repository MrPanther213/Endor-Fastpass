# fastpass/models.py
from django.db import models

class ThemeZone(models.Model):
    """Represents a themed area of Endor Adventures park.
    Examples: Forest of Endor, Ewok Village, Imperial Ruins
    """
    # Basic information about the zone
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Is this zone currently open to guests?
    is_open = models.BooleanField(default=True)
    # When was this record created?
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']  # Sort zones alphabetically

    def __str__(self):
        return self.name


class Attraction(models.Model):
    """Represents a ride, show, or experience in the park."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    theme_zone = models.ForeignKey(ThemeZone, on_delete=models.CASCADE, related_name='attractions')
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    """Represents available booking time slots for attractions."""
    start_time = models.TimeField()
    end_time = models.TimeField()
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='time_slots')
    capacity = models.PositiveIntegerField(default=100)  # Maximum guests per slot
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class Guest(models.Model):
    """Represents park visitors."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    membership_tier = models.CharField(
        max_length=20,
        choices=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold')
        ],
        default='bronze'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FastPass(models.Model):
    """Represents FastPass reservations linking guests to attractions at specific times."""
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='fast_passes')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='fast_passes')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='fast_passes')
    booking_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['guest', 'attraction', 'time_slot', 'booking_date']  # Prevent duplicate bookings

    def __str__(self):
        return f"{self.guest} - {self.attraction} at {self.time_slot} on {self.booking_date}"