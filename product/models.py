from django.db import models
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from ckeditor_uploader.fields import  RichTextUploadingField
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

# Create your models here.

class Category(MPTTModel):

	STATUS = (
		('True', 'True'),
		('False', 'False')
	)
	parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
	titre = models.CharField(max_length=30)
	keywords = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	photo = models.ImageField(upload_to='images/', blank=True)
	status = models.CharField(max_length=10, choices=STATUS)
	slug = models.SlugField()

	date_add = models.DateTimeField(auto_now_add=True)
	date_upd = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Categorie"
		verbose_name_plural = "Categories"

	class MPTTMeta:
		order_insertion_by = ['titre']


	def __str__(self):
		return self.titre

	def __str__(self):
		path = [self.titre]
		k = self.parent
		while k is not None:
			path.append(k.titre)
			k = k.parent
		return ' / '.join(path[::-1])


class Produit(models.Model):
	STATUS = (
		('True','True'),
		('False', 'False'),
	)
	VARIANTS = (
		('None', 'None'),
		('Size', 'Size'),
		('Color', 'Color'),
		('Size-Color', 'Size-Color'),
	)
	categorie = models.ForeignKey(Category, on_delete=models.CASCADE)
	titre = models.CharField(max_length=150)
	keywords = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	photo = models.ImageField(upload_to='product/images', blank=True)
	price = models.FloatField()
	amount = models.IntegerField()
	reduction = models.FloatField()
	pourcentage = models.IntegerField()
	details = RichTextUploadingField()
	variant = models.CharField(max_length=10, choices=VARIANTS, default='None' )
	status = models.CharField(max_length=10, choices=STATUS)
	slug = models.SlugField()

	date_add = models.DateTimeField(auto_now_add=True)
	date_upd = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Produit"
		verbose_name_plural = "Produits"

	def __str__(self):
		return self.titre

	# def image_tag(self):
	# 	return mark_safe('<img src= "{}" height="50"/>'.format(self.photo.url))

	# image_tag.short_description = 'photo'

	def averagereview(self):
		reviews = Comment.objects.filter(produit=self, status='Red').aggregate(avarage=Avg('rate'))
		avg=0
		if reviews["avarage"] is not None:
			avg=int(reviews["avarage"])
		return avg

	def countreview(self):
		reviews = Comment.objects.filter(produit=self, status='Red').aggregate(count=Count('id'))
		cnt=0
		if reviews["count"] is not None:
			cnt = int(reviews["count"])	
		return cnt


class Image(models.Model):
	product = models.ForeignKey(Produit, on_delete=models.CASCADE)
	titre = models.CharField(max_length=50)
	photo = models.ImageField(upload_to='images', blank=True)

	def __str__(self):
		return self.titre


class Comment(models.Model):

	STATUS = (
		('New','New'),
		('Red','Red'),
		('Closed','Closed'),
	)
	produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(blank=True, max_length=100)
	comment = models.CharField(blank=True, max_length=255)
	rate = models.IntegerField(default=1)
	ip = models.CharField(blank=True, max_length=20)
	status = models.CharField(max_length=10, choices=STATUS, default='New')

	date_add = models.DateTimeField(auto_now_add=True)
	date_upd = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.subject


class Color(models.Model):
	name = models.CharField(max_length=30)
	code = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.name

	def color_tag(self):
		if self.code is not None:
			return mark_safe('<p style="background-color:{}"> Color </p>'.format(self.code))
		else:
			return ""


class Size(models.Model):
	name = models.CharField(max_length=20)
	code = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.name


class Variant(models.Model):
	titre = models.CharField(max_length=100, blank=True, null=True)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="produit")
	color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
	size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
	image_id = models.IntegerField(blank=True, null=True, default=0)
	quantity = models.IntegerField(default=1)
	price = models.FloatField(default=0)

	def __str__(self):
		return self.titre

	def image(self):
		img = Image.objects.get(id=self.image_id)
		if img.id is not None:
			varimage = img.photo.url
		else:
			varimage =""
		return varimage


	def image_tag(self):
		img = Image.objects.get(id=self.image_id)
		if img.id is not None:
			return mark_safe('<img src="{}" height="50"/>'.format(img.photo.url))
		else:
			return ""









