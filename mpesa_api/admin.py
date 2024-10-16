from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'status', 'time', 'ip_address')
    search_fields = ('transaction_id', 'user__username')
    list_filter = ('status', 'time')
