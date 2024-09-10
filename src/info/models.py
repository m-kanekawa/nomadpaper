from django.db import models


class Info(models.Model):
  company_name = models.CharField(verbose_name='Company Name', max_length=60, default='')
  address1     = models.CharField(verbose_name='Address 1', max_length=30, default='', null=True, blank=True)
  address2     = models.CharField(verbose_name='Address 2', max_length=30, default='', null=True, blank=True)
  address3     = models.CharField(verbose_name='Address 3', max_length=30, default='', null=True, blank=True)
  tel          = models.CharField(verbose_name='Tel', max_length=20, default='', null=True, blank=True)
  bank         = models.CharField(verbose_name='Bank', max_length=100, default='', null=True, blank=True)
  btw          = models.CharField(verbose_name='BTW', max_length=100, default='', null=True, blank=True)
  kvk          = models.CharField(verbose_name='KVK', max_length=100, default='', null=True, blank=True)
  objects      = models.Manager()

  def __str__(self):
    return "%s" % (self.company_name)
