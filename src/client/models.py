from django.db import models


class Client(models.Model):
  name     = models.CharField(verbose_name='Client Name', max_length=60, default='', blank=True)
  nickname = models.CharField(verbose_name='Nickname', max_length=60, default='', null=True, blank=True)
  address1 = models.CharField(verbose_name='Address 1', max_length=50, default='', null=True, blank=True)
  address2 = models.CharField(verbose_name='Address 2', max_length=50, default='', null=True, blank=True)
  address3 = models.CharField(verbose_name='Address 3', max_length=50, default='', null=True, blank=True)
  country  = models.CharField(verbose_name='country', max_length=50, default='', null=True, blank=True)
  objects  = models.Manager()

  def __str__(self):
    return "%s" % (self.name)
