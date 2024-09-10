from django.db import models


class CostType(models.Model):
  COLOR_CHOICES = (
      ('#f79f1f', 'Radiant Yellow'),
      ('#a3cb38', 'Android Green'),
      ('#1289a7', 'Mediterranean Sea'),
      ('#d980fa', 'Lavender Tea'),
      ('#b53471', 'Very Berry'),
      ('#ea2027', 'Red Pigment'),
      ('#006266', 'Turkish Aqua'),
      ('#1b1464', '20000 Leagues Under the Sea'),
      ('#5758bb', 'Circumorbital Ring'),
      ('#6f1e51', 'Magenta Purple'),
  )

  name     = models.CharField(verbose_name='Category', max_length=60, default='', blank=True)
  nickname = models.CharField(verbose_name='Category Nickname', max_length=60, default='', null=True, blank=True)
  color    = models.CharField(verbose_name='Color', choices=COLOR_CHOICES, max_length=10, default='', null=True, blank=True)
  objects  = models.Manager()

  def __str__(self):
    return "%s" % (self.name)
