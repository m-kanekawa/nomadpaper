from django.db import models
from django.utils import timezone
from client.models import Client

TAX_CHOICES = (
  (0, '0'),
  (9, '9%'),
  (21, '21%'),
)
STATUS_CHOICES = (
  (0, 'Draft'),
  (1, 'Invalid'),
  (2, 'Sent'),
  (3, 'Paid'),
)
CURRENCY_CHOICES = (
  (1, '€'),
  (2, '￥'),
  (3, '＄'),
)
CURRENCY_DIGIT = {
  1: 2,
  2: 0,
  3: 2,
}
REGION_CHOICES = (
  (1, 'Nederland'),
  (2, 'inside EU'),
  (3, 'outside EU'),
)


class Line(models.Model):
  in_id       = models.IntegerField(default=0)
  line_no     = models.IntegerField(default=0)
  title       = models.TextField(verbose_name='項目', max_length=1000, null=True, default='', blank=True)
  quantity    = models.FloatField(verbose_name='個数', null=True, blank=True)
  unit_price  = models.FloatField(verbose_name='単価', null=True, blank=True)
  total_price = models.FloatField(verbose_name='合計金額', null=True, blank=True)
  tax_rate    = models.IntegerField(verbose_name='消費税％', choices=TAX_CHOICES, default=0)
  objects     = models.Manager()

  class Meta:
    ordering = ('in_id', 'line_no')

  def __str__(self):
    return "%d:%d" % (self.in_id, self.line_no)

  def save(self, *args, **kwargs):
    return super(Line, self).save(*args, **kwargs)


class Income(models.Model):
  number      = models.CharField(verbose_name='Number', max_length=100, default='', null=True, blank=True)
  client      = models.ForeignKey(Client, verbose_name='Client', null=True, blank=True, on_delete=models.SET_NULL)
  region      = models.IntegerField(verbose_name='Region', choices=REGION_CHOICES, default=0)
  status      = models.IntegerField(verbose_name='Status', choices=STATUS_CHOICES, default=0)
  date        = models.DateField(verbose_name='Date', null=True, blank=True)
  paydue      = models.DateField(verbose_name='Paydue', null=True, blank=True)
  date_paid   = models.DateField(verbose_name='Date Paid', null=True, blank=True)
  currency    = models.IntegerField(verbose_name='Currency', choices=CURRENCY_CHOICES, default=0)
  local_total = models.FloatField(verbose_name='Total in Local Currency', default=0)      # only currency!=1
  rate        = models.FloatField(verbose_name='Rate', default=0)
  net         = models.FloatField(verbose_name='Net (€)', default=0)     # only region=1(=net21+net9+net0)
  net21       = models.FloatField(verbose_name='Net 21% (€)', default=0) # only region=1
  net9        = models.FloatField(verbose_name='Net 9% (€)', default=0)  # only region=1
  net0        = models.FloatField(verbose_name='Net 0% (€)', default=0)  # only region=1
  vat         = models.FloatField(verbose_name='VAT (€)', default=0)     # only region=1(=vat9+vat21)
  vat21       = models.FloatField(verbose_name='VAT 21% (€)', default=0)  # only region=1
  vat9        = models.FloatField(verbose_name='VAT 9% (€)', default=0)   # only region=1
  total       = models.FloatField(verbose_name='Total (€)', default=0)   # when currency!=1 local_total*rate、when currency==1, =net+vat
  memo        = models.TextField(verbose_name='Memo', max_length=300, default='', null=True, blank=True)
  objects     = models.Manager()

  class Meta:
    ordering = ('pk',)

  def __str__(self):
    return "%s:%s" % (self.id, self.number)

  @property
  def digit(self):
    return "%d" % CURRENCY_DIGIT[self.currency]