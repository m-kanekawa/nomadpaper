from django.db import models
from django.core.validators import FileExtensionValidator
from costtype.models import CostType
import logging

logger = logging.getLogger(__name__)


TAX_CHOICES = (
  (0, '0'),
  (9, '9%'),
  (21, '21%'),
)
CURRENCY_CHOICES = (
  (1, '€'),
  (2, '￥'),
  (3, '＄'),
)
REGION_CHOICES = (
  (1, 'Nederland'),
  (2, 'inside EU'),
  (3, 'outside EU'),
)

def get_image_path(instance, filename):
  y = instance.date_paid.year
  filepath = "%s/reciept/%s" % (y, filename)
  logger.debug("filepath = " + filepath)
  return filepath
  # https://banatech.net/blog/view/9


class Out(models.Model):
  title       = models.CharField(verbose_name='Title', max_length=100, default='', null=True, blank=True)
  cost_type   = models.ForeignKey(CostType, verbose_name='Cost Type', null=True, blank=True, on_delete=models.SET_NULL)
  region      = models.IntegerField(verbose_name='Region', choices=REGION_CHOICES, default=0)
  date_paid   = models.DateField(verbose_name='Date Paid', null=True, blank=True)
  tax_rate    = models.IntegerField(verbose_name='Tax Rate', choices=TAX_CHOICES, default=21)
  # currency    = models.IntegerField(verbose_name='Currency', choices=CURRENCY_CHOICES, default=0)
  # local_total = models.IntegerField(verbose_name='Total in Local Currency', default=0)
  # rate        = models.FloatField(verbose_name='Rate', default=0)
  net         = models.FloatField(verbose_name='Net (€)', default=0)
  vat         = models.FloatField(verbose_name='VAT (€)', default=0)     # only region=1
  vat21       = models.FloatField(verbose_name='VAT 21% (€)', default=0) # only region=1
  vat9        = models.FloatField(verbose_name='VAT 9% (€)', default=0)  # only region=1
  total       = models.FloatField(verbose_name='Total (€)', default=0)
  reciept     = models.FileField(
      verbose_name='Reciept',
      upload_to=get_image_path,
      # upload_to='%Y/reciept/',
      validators=[FileExtensionValidator(['jpg', 'png', 'pdf'])],
      null=True, blank=True
  )
  memo = models.TextField(verbose_name='Memo', max_length=300, default='', null=True, blank=True)
  objects = models.Manager()

  class Meta:
    ordering = ('pk',)

  def __str__(self):
    return "%s:%s" % (self.id, self.title)
