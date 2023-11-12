from .models import *
from datetime import datetime, timedelta, timezone

ref = datetime(1970, 1, 1, tzinfo=timezone.utc)

def secstamp(dt : datetime):
  return (dt - ref) // timedelta(seconds=1)

def upd_poi(poi : POI):
  if poi.owner is None:
    return
  now = datetime.now(tz=timezone.utc)
  if poi.lastupdated is None:
    poi.lastupdated = now
  secs = secstamp(now) - secstamp(poi.lastupdated)
  poi.lastupdated = now
  poi.save()
  pts = secs*poi.points
  own = Account.objects.filter(username=poi.owner).first()
  own.points += pts
  own.save()

def upd_all():
  for poi in POI.objects.all():
    upd_poi(poi)