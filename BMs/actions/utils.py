from .models import Action
from django.contrib.contenttypes.models import ContentType

from django.utils import timezone

def create_action(user, verb, target):
    target_ct = ContentType.objects.get_for_model(target)

    new_action = Action(user=user,
                        verb=verb,
                        target_ct=target_ct,
                        target_id=target.id)

    last_minute = timezone.now() - timezone.timedelta(minutes=1)
    last_actions = Action.objects.filter(user=user,
                                         verb=verb,
                                         created__gt=last_minute,
                                         target_ct = target_ct,
                                         target_id = target.id)

    if last_actions:
        return False
    new_action.save()
    return True


