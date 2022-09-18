from fileinput import filename
from math import prod
import re
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.urls import reverse,reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView, View
from .models import Categories,SubCategories,CustomUser,MerchantUser,Products,ProductMedia,ProductAbout,ProductDetails,ProductTags,ProductTransactions,StaffUser
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

from DjangoEcommerce.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url=reverse_lazy('admin_login'))
def demoPage(request):
    return render(request, 'admin/home.html')

class AdminLoginView(View):
    template_name = 'admin/signin.html'
    context={}
    def get(self, request):
        self.context.update({
            'title':'Login',
            'url':reverse('admin_login')
        })
        return render(request, self.template_name,self.context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request=request, user=user)
            return HttpResponseRedirect(reverse('admin_home'))
        else:
            messages.error(request,'Login Failed, Invalid Input')
            return HttpResponseRedirect(reverse('admin_login'))
    
def AdminLogoutView(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return HttpResponseRedirect(reverse('admin_login'))


class CategoryListView(ListView):
    model=Categories
    template_name="admin/category/category_list.html"
    paginate_by=1

    def get_queryset(self):
        filter_value=self.request.GET.get('filter','')
        order_by=self.request.GET.get('orderby','id')
        if filter_value !='':
            cat=Categories.objects.filter(Q(title__contains=filter_value) | Q(description__contains=filter_value)).order_by(order_by)
        else:
            cat=Categories.objects.all().order_by(order_by)
        return cat


    def get_context_data(self,**kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get('filter','')
        context["orderby"]=self.request.GET.get('orderby','id')
        context["all_table_fields"]=Categories._meta.get_fields()
        return context

class CategoryCreateView(SuccessMessageMixin,CreateView):
    model=Categories
    fields= "__all__"
    success_message="Category created successfully"
    template_name="admin/category/category_create.html"
    success_url=reverse_lazy("category_list")

class CategoryUpdateView(SuccessMessageMixin,UpdateView):
    model=Categories
    fields= "__all__"
    success_message="Category updated successfully"
    template_name="admin/category/category_update.html"
    success_url=reverse_lazy("category_list")


class SubCategoryListView(ListView):
    model=SubCategories
    template_name="admin/category/sub_category_list.html"
    paginate_by=1

    def get_queryset(self):
        filter_value=self.request.GET.get('filter','')
        order_by=self.request.GET.get('orderby','id')
        if filter_value !='':
            cat=SubCategories.objects.filter(Q(title__contains=filter_value) | Q(description__contains=filter_value)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)
        return cat


    def get_context_data(self,**kwargs):
        context=super(SubCategoryListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get('filter','')
        context["orderby"]=self.request.GET.get('orderby','id')
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

class SubCategoryCreateView(SuccessMessageMixin,CreateView):
    model=SubCategories
    fields= "__all__"
    success_message="SubCategory created successfully"
    template_name="admin/category/sub_category_create.html"
    success_url=reverse_lazy("sub_category_list")

class SubCategoryUpdateView(SuccessMessageMixin,UpdateView):
    model=SubCategories
    fields= "__all__"
    success_message="SubCategory updated successfully"
    template_name="admin/category/sub_category_update.html"
    success_url=reverse_lazy("sub_category_list")

class MerchantUserCreateView(SuccessMessageMixin,CreateView):
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]
    template_name="admin/merchant/merchant_create.html"

    def form_valid(self, form):
        # saving custom user object for merchant 
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant User
        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.merchantuser.profile_pic=profile_pic_url
        user.merchantuser.company_name=self.request.POST.get("company_name")
        user.merchantuser.gst_details=self.request.POST.get("gst_details")
        user.merchantuser.address=self.request.POST.get("address")
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        user.merchantuser.is_added_by_admin=is_added_by_admin

        user.save()
        messages.success(self.request,"Merchant User Created")
        return HttpResponseRedirect(reverse('merchant_list'))



class MerchantUserListView(ListView):
    model=MerchantUser
    template_name="admin/merchant/merchant_list.html"

class MerchantUserUpdateView(SuccessMessageMixin,UpdateView):
    model=CustomUser
    fields= ["first_name","last_name","email","username"]
    success_message="Merchant updated successfully"
    template_name="admin/merchant/merchant_update.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        merchantuser=MerchantUser.objects.get(auth_user_id=self.object.pk)
        context['merchantuser']=merchantuser
        return context


    def form_valid(self, form):
        # saving custom user object for merchant 
        user=form.save(commit=False)
        user.save()

        merchantuser=MerchantUser.objects.get(auth_user_id=user.id)

        #Saving Merchant User
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            merchantuser.profile_pic=profile_pic_url


        merchantuser.company_name=self.request.POST.get("company_name")
        merchantuser.gst_details=self.request.POST.get("gst_details")
        merchantuser.address=self.request.POST.get("address")
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        merchantuser.is_added_by_admin=is_added_by_admin

        merchantuser.save()
        messages.success(self.request,"Merchant User Updated Successfully")
        return HttpResponseRedirect(reverse('merchant_list'))



class ProductCreateView(View):
    def get(self, request):
        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category, "sub_category":sub_category})

        merchant_users=MerchantUser.objects.filter(auth_user_id__is_active=True)

        return render(self.request,"admin/product/product_create.html",{"categories":categories_list,"merchant_users":merchant_users})

    def post(self, request):
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        added_by_merchant=request.POST.get("added_by_merchant")
        in_stock_total=request.POST.get("in_stock_total")
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")

        subcat_obj=SubCategories.objects.get(id=sub_category)
        merchant_user_obj=MerchantUser.objects.get(id=added_by_merchant)
        product=Products(product_name=product_name,in_stock_total=in_stock_total,url_slug=url_slug,brand=brand,subcategories_id=subcat_obj,product_description=product_description,product_max_price=product_max_price,product_discount_price=product_discount_price,product_long_description=long_desc,added_by_merchant=merchant_user_obj)
        product.save()

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i+=1

        j=0
        for title_title in title_title_list:
            product_details=ProductDetails(product_id=product,title=title_title[j],title_details=title_details_list[j])
            product_details.save()
            j+=1


        for about in about_title_list:
            product_about=ProductAbout(product_id=product,title=about)
            product_about.save()

        product_tags_list=product_tags.split(',')
        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()


        product_transaction=ProductTransactions(product_id=product,transaction_type=1,transaction_product_count=in_stock_total,transaction_description="Intially Item Added in Stocks")
        product_transaction.save()
        return HttpResponse("OK")

@csrf_exempt
def File_Upload(request):
    file=request.FILES["file"]
    fs=FileSystemStorage()
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location":"'+BASE_URL+''+file_url+'"}')

class ProductListView(ListView):
    model=Products
    template_name="admin/product/product_list.html"
    paginate_by=1

    def get_queryset(self):
        filter_value=self.request.GET.get('filter','')
        order_by=self.request.GET.get('orderby','id')
        if filter_value !='':
            products=Products.objects.filter(Q(product_name__contains=filter_value) | Q(product_description__contains=filter_value)).order_by(order_by)
        else:
            products=Products.objects.all().order_by(order_by)

        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1,is_active=1).first()
            product_list.append({"product":product,'media':product_media})
        
        return product_list


    def get_context_data(self,**kwargs):
        context=super(ProductListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get('filter','')
        context["orderby"]=self.request.GET.get('orderby','id')
        context["all_table_fields"]=Products._meta.get_fields()
        return context



class ProductUpdateView(View):
    def get(self, request,*args,**kwargs):
        product_id=kwargs.get('product_id')
        product=Products.objects.get(id=product_id)
        product_details=ProductDetails.objects.filter(product_id=product_id)
        product_about=ProductAbout.objects.filter(product_id=product_id)
        product_tags=ProductTags.objects.filter(product_id=product_id)

        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category)
            categories_list.append({"category":category,"sub_category":sub_category})

        context={
            "categories": categories_list,
            "product":product,
            "product_details":product_details,
            "product_about":product_about,
            "product_tags":product_tags
        }

        return render(self.request, 'admin/product/product_update.html',context)

    def post(self, request,*args,**kwargs):

        product_id=kwargs.get('product_id')
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        details_ids=request.POST.getlist("details_id[]")
        about_title_list=request.POST.getlist("about_title[]")
        about_ids=request.POST.getlist("about_id[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")

        subcat_obj=SubCategories.objects.get(id=sub_category)
        
        product=Products.objects.get(id=product_id)
            
        product.product_name=product_name
        product.url_slug=url_slug
        product.brand=brand
        product.subcategories_id=subcat_obj
        product.product_description=product_description
        product.product_max_price=product_max_price
        product.product_discount_price=product_discount_price
        product.product_long_description=long_desc
        product.save()

        
        j=0
        for title_title in title_title_list:
            detail_id=details_ids[j]
            if detail_id == "blank" and title_title != "":
                product_details=ProductDetails(product_id=product,title=title_title[j],title_details=title_details_list[j])
                product_details.save()
                
            else:
                if title_title != "":
                    product_details=ProductDetails.objects.get(id=detail_id)
                    product_details.product_id=product
                    product_details.title=title_title
                    product_details.title_details=title_details_list[j]
                    product_details.save()
        j+=1     

        k=0
        for about in about_title_list:
            about_id=about_ids[k]
            if about_id == "blank" and about!='':
                product_about=ProductAbout(product_id=product,title=about)
                product_about.save()
            else:
                if about!='':
                    product_about=ProductAbout.objects.get(id=about_id)
                    product_about.product_id=product
                    product_about.title=about
                    product_about.save()
        k+=1

        ProductTags.objects.filter(product_id=product_id).delete()
        product_tags_list=product_tags.split(',')
        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()


        return HttpResponse("ok")


class ProductAddMediaView(View):
    def get(self, request, *args, **kwargs):
        product_id=kwargs['product_id']
        product=Products.objects.get(id=product_id)
        return render(self.request,'admin/product/product_add_media.html',{"product":product})

    def post(self, request,*args,**kwargs):
        product_id=kwargs['product_id']
        product=Products.objects.get(id=product_id)
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i+=1

        return HttpResponse("ok")

    
class ProductEditMediaView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_media=ProductMedia.objects.filter(product_id=product_id)
        print(product_media.count())
        return render(request,"admin/product/product_edit_media.html",{"product":product,"product_medias":product_media})


class ProductDeleteMediaView(View):

    def get(self, request, *args, **kwargs):
        media_id=kwargs["id"]
        product_media=ProductMedia.objects.get(id=media_id)
        import os
        from DjangoEcommerce import settings

        #It will work too Sometimes
        # product_media.media_content.delete()
        # print("media----",os.path.join(settings.MEDIA_ROOT,str(product_media.media_content)))
        # print("path-=-------------",settings.BASE_DIR.joinpath('media').joinpath(product_media.media_content))
        os.remove(str(settings.MEDIA_ROOT).replace("\media","")+str(product_media.media_content).replace('/media',''))
        # return HttpResponse("ok :"+str(settings.MEDIA_ROOT).replace("/media","")+str(product_media.media_content).replace('/','\\'))
        product_id=product_media.product_id.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media",kwargs={"product_id":product_id}))


class ProductAddStockView(View):
    def get(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request,"admin/product/product_add_stocks.html",{"product":product})

    def post(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        new_instock=request.POST.get("add_stocks")
        product=Products.objects.get(id=product_id)
        old_stocks=product.in_stock_total
        new_stocks=int(new_instock) +int(old_stocks)
        product.in_stock_total=new_stocks
        product.save()

        product_obj=Products.objects.get(id=product_id)
        product_transaction=ProductTransactions(product_id=product_obj,transaction_product_count=new_instock,transaction_description="New Product Added",transaction_type=1)
        product_transaction.save()
        return HttpResponseRedirect(reverse("product_add_stock",kwargs={"product_id":product_id}))



class StaffUserCreateView(SuccessMessageMixin,CreateView):
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]
    template_name="admin/staff/staff_create.html"

    def form_valid(self, form):
        # saving custom user object for merchant 
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=2
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant User
        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.staffuser.profile_pic=profile_pic_url

        user.save()
        messages.success(self.request,"Staff User Created")
        return HttpResponseRedirect(reverse('staff_list'))



class StaffUserListView(ListView):
    model=StaffUser
    template_name="admin/staff/staff_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            staff=StaffUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            staff=StaffUser.objects.all().order_by(order_by)

        return staff

    def get_context_data(self,**kwargs):
        context=super(StaffUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=StaffUser._meta.get_fields()
        return context



class StaffUserUpdateView(SuccessMessageMixin,UpdateView):
    model=CustomUser
    fields= ["first_name","last_name","email","username"]
    template_name="admin/staff/staff_update.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        staffuser=StaffUser.objects.get(auth_user_id=self.object.pk)
        context['staffuser']=staffuser
        return context


    def form_valid(self, form):
        # saving custom user object for merchant 
        user=form.save(commit=False)
        user.save()

        staffuser=StaffUser.objects.get(auth_user_id=user.id)

        #Saving Merchant User
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            staffuser.profile_pic=profile_pic_url


        staffuser.save()
        messages.success(self.request,"Staff User Updated Successfully")
        return HttpResponseRedirect(reverse('staff_list'))

