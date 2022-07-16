from django.db import models

SALES_CHANNEL = (
    ('trendyol', 'Trendyol'),
    ('hepsiburada', 'Hepsiburada'),
)


class ProdcutListing(models.Model):
    '''Model for storing products'''
    sales_channel = models.CharField(choices=SALES_CHANNEL, max_length=50, db_index=True)
    name = models.CharField(max_length=250)
    stock = models.PositiveIntegerField(default=0)
    stock_code = models.CharField(max_length=25)
    is_bundle = models.BooleanField(default=False)
    status = models.BooleanField(default=True, verbose_name='is active?',
                                 help_text='Active products will show in selling list')

    class Meta:
        verbose_name_plural = 'Products List'

    def save(self, *args, **kwargs):
        '''if stock equals to zero status automatically change to false'''
        if int(self.stock) == 0:
            self.status = False

        super(ProdcutListing, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.sales_channel} : {self.name}'

    @property
    def statusChange(self):
        '''to change status of objects'''
        if self.status is True:
            status = False
        else:
            status = True
        return status


class ProductGroup(models.Model):
    '''Model for keeping bundle products'''
    group_name = models.CharField(max_length=250)
    group_code = models.CharField(max_length=250)
    amount = models.IntegerField(default=0, null=True, blank=True)
    bundle_product = models.ForeignKey(ProdcutListing, related_name="group", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Product Group'

    def __str__(self):
        return f'{self.group_name}'
