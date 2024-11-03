# api/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Article)
def send_article_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"New article added: {instance.title}",
                "article_name": instance.title,
                "article_date": instance.created_at.strftime('%Y-%m-%d'),
                "article_author": instance.get_author(),
                "article_link": instance.get_absolute_url()
            }
        )