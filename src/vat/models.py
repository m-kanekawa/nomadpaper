from django.db import models


class VatReport(models.Model):
  year    = models.IntegerField(verbose_name='year')
  q       = models.IntegerField(verbose_name='Q')
  net_1_a = models.FloatField(verbose_name='1a net', default=0)
  btw_1_a = models.FloatField(verbose_name='1a btw', default=0)
  net_1_b = models.FloatField(verbose_name='1b net', default=0)
  btw_1_b = models.FloatField(verbose_name='1b btw', default=0)
  net_1_e = models.FloatField(verbose_name='1e net', default=0)
  net_3_a = models.FloatField(verbose_name='3a net', default=0)
  net_3_b = models.FloatField(verbose_name='3b net', default=0)
  net_4_a = models.FloatField(verbose_name='4a net', default=0)
  btw_4_a = models.FloatField(verbose_name='4a btw', default=0)
  net_4_b = models.FloatField(verbose_name='4b net', default=0)
  btw_4_b = models.FloatField(verbose_name='4b btw', default=0)
  btw_5_a  = models.FloatField(verbose_name='5a btw', default=0)
  btw_5_b  = models.FloatField(verbose_name='5b btw', default=0)
  btw_5_c  = models.FloatField(verbose_name='5c btw', default=0)
  btw_5_g  = models.FloatField(verbose_name='5g btw', default=0)
  objects = models.Manager()

  def __str__(self):
    return "%d/%d" % (self.year, self.q)
