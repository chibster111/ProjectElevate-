from django.db import models
from django import forms

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Creating Models Here

class UserManager(BaseUserManager):
    def create_user(self, user_email, user_username, user_password, user_phone_number):
        if not user_email:
            raise ValueError('Users must have an email address')

        #TODO:: refactor
        user = self.model(
            email=self.normalize_email(user_email),
            username=user_username,
            phone_number=user_phone_number,
        )

        user.set_password(user_password)
        user.save(using=self._db)
        return user

    def create_business(self, email, username, password, phone_number, business_name=None, api_key=None,
                        expiration_date=None, street_branch_address=None, apt_branch_address=None,
                        city_branch_address=None, state_branch_address=None, country_branch_address=None,
                        zip_branch_address=None, street_hq_address=None, apt_hq_address=None, city_hq_address=None,
                        state_hq_address=None,country_hq_address=None, zip_hq_address=None,):

        user_obj = self.create_user(email, username, password, phone_number)

        user_obj.business = True

        # details about business
        user_obj.business_name = business_name
        user_obj.api_key = api_key
        user_obj.expiration_date = expiration_date

        # active
        user_obj.active = True

        # branch address
        user_obj.street_branch_address = street_branch_address
        user_obj.apt_branch_address = apt_branch_address
        user_obj.city_branch_address = city_branch_address
        user_obj.state_branch_address = state_branch_address
        user_obj.country_branch_address = country_branch_address
        user_obj.zip_branch_address = zip_branch_address

        # hq address
        user_obj.street_hq_address = street_hq_address
        user_obj.apt_hq_address = apt_hq_address
        user_obj.city_hq_address = city_hq_address
        user_obj.state_hq_address = state_hq_address
        user_obj.country_hq_address = country_hq_address
        user_obj.zip_hq_address = zip_hq_address



    def create_customer(self, email, username, password, phone_number, customer_name=None, customer_last_name=None,api_key=None,
                        street_home_address=None, apt_home_address=None, city_home_address=None, state_home_address=None,
                        country_home_address=None, zip_home_address=None):

        user_obj = self.create_user(email, username, password, phone_number)


        # details about customer
        user_obj.customer = True
        user_obj.name = customer_name
        user_obj.last_name = customer_last_name

        # active
        user_obj.active = True

        # api key


        # home address
        user_obj.street_home_address = street_home_address
        user_obj.apt_home_address = apt_home_address
        user_obj.city_home_address = city_home_address
        user_obj.state_home_address = state_home_address
        user_obj.country_home_address = country_home_address
        user_obj.zip_home_address = zip_home_address



    def deactivate_account(self):
        # TODO:
        pass

    def create_superuser(self, username, password):
        phone_number = 1
        email = "test1@gmail.com"
        user_obj = self.create_user(email, username, password, phone_number)
        user_obj.admin = True
        user_obj.staff = True
        return user_obj



    def get_all_businesses(self):
        return User.objects.filter(business=True)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True, blank=False)  # REQUIRED
    username = models.CharField(max_length=30, blank=False, unique=True)  # REQUIRED
  #  password = models.CharField(max_length=30)
    active = models.BooleanField(default=False)  # can login
    admin = models.BooleanField(default=False)  # superuser
    staff = models.BooleanField(default=False)  # staff
    customer = models.BooleanField(default=False)  # customer
    business = models.BooleanField(default=False)  # core
    business_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)  # REQUIRED
    api_key = models.CharField(max_length=1000, blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    # Branch Address
    street_branch_address = models.CharField(max_length=100, blank=True, null=True)
    apt_branch_address = models.CharField(max_length=100, blank=True, null=True)
    city_branch_address = models.CharField(max_length=100, blank=True, null=True)
    state_branch_address = models.CharField(max_length=100, blank=True, null=True)
    country_branch_address = models.CharField(max_length=100, blank=True, null=True)
    zip_branch_address = models.CharField(max_length=15, blank=True, null=True)

    # HQ Address
    street_hq_address = models.CharField(max_length=100, blank=True, null=True)
    apt_hq_address = models.CharField(max_length=100, blank=True, null=True)
    city_hq_address = models.CharField(max_length=100, blank=True, null=True)
    state_hq_address = models.CharField(max_length=100, blank=True, null=True)
    country_hq_address = models.CharField(max_length=100, blank=True, null=True)
    zip_hq_address = models.CharField(max_length=15, blank=True, null=True)

    # Home Address
    street_home_address = models.CharField(max_length=100, blank=True, null=True)
    apt_home_address = models.CharField(max_length=100, blank=True, null=True)
    city_home_address = models.CharField(max_length=100, blank=True, null=True)
    state_home_address = models.CharField(max_length=100, blank=True, null=True)
    country_home_address = models.CharField(max_length=100, blank=True, null=True)
    zip_home_address = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):

        if self.business:
            return self.business_name + " " + str(self.id)

        if self.customer:
            return self.name + " " + self.last_name + " " + str(self.id)

        else:
            return self.username + " " + str(self.id)

    def is_admin(self):
        return self.admin

    def is_staff(self):
        return self.staff

    def is_business(self):
        return self.business

    def is_customer(self):
        return self.customer

    def is_active(self):
        return self.active

    def is_superuser(self):
        return self.admin

    def get_customer_fullname(self):
        pass

    def get_email(self):
        return self.email




class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    business_id     = models.IntegerField(blank=False)
    title           = models.CharField(max_length=30, blank=False)
    description     = models.CharField(max_length=255, blank=False)
    cost            = models.IntegerField(blank=False)
    start_date      = models.DateTimeField(blank=True)
    end_date        = models.DateTimeField(blank=True)


    def __str__(self):
        return self.title




class Benefit:
    pass



class Customer(models.Model):

    customer_id             = models.IntegerField(blank=False)
    email                   = models.EmailField(max_length=255, unique=True, blank=False)  # REQUIRED
    username                = models.CharField(max_length=30, blank=False, unique=True)  # REQUIRED
    active                  = models.BooleanField(default=False)  # can login
    subscriptions           = models.ManyToManyField(Subscription)
    name                    = models.CharField(max_length=255, blank=True, null=True)
    last_name               = models.CharField(max_length=255, blank=True, null=True)
    phone_number            = models.CharField(max_length=15, blank=False, null=False)  # REQUIRED
    api_key                 = models.CharField(max_length=1000, blank=True, null=True)
    expiration_date         = models.DateTimeField(blank=True, null=True)
    street_home_address     = models.CharField(max_length=100, blank=True, null=True)
    apt_home_address        = models.CharField(max_length=100, blank=True, null=True)
    city_home_address       = models.CharField(max_length=100, blank=True, null=True)
    state_home_address      = models.CharField(max_length=100, blank=True, null=True)
    country_home_address    = models.CharField(max_length=100, blank=True, null=True)
    zip_home_address        = models.CharField(max_length=15, blank=True, null=True)
    credit_card_number      = models.IntegerField(blank=False)  #
    credit_card_exp_date    =  models.DateTimeField(blank=False)


    def __str__(self):
        return self.customer_id


class Business(models.Model):
    business_id         = models.IntegerField(blank=False)
    email               = models.EmailField(max_length=255, unique=True, blank=False)  # REQUIRED
    username            = models.CharField(max_length=30, blank=False, unique=True)  # REQUIRED
    phone_number        = models.CharField(max_length=15, blank=False, null=False)  # REQUIRED
    business_name       = models.CharField(max_length=255, blank=True, null=True)
    api_key             = models.CharField(max_length=1000, blank=True, null=True)

    nmi_login           = models.CharField(max_length=30, blank=False, unique=True)  # REQUIRED
    nmi_password        = models.CharField(max_length=30, blank=False, unique=True)
    expiration_date     = models.DateTimeField(blank=True, null=True)

    # Branch Address
    street_branch_address = models.CharField(max_length=100, blank=True, null=True)
    apt_branch_address = models.CharField(max_length=100, blank=True, null=True)
    city_branch_address = models.CharField(max_length=100, blank=True, null=True)
    state_branch_address = models.CharField(max_length=100, blank=True, null=True)
    country_branch_address = models.CharField(max_length=100, blank=True, null=True)
    zip_branch_address = models.CharField(max_length=15, blank=True, null=True)


    # HQ Address
    street_hq_address = models.CharField(max_length=100, blank=True, null=True)
    apt_hq_address = models.CharField(max_length=100, blank=True, null=True)
    city_hq_address = models.CharField(max_length=100, blank=True, null=True)
    state_hq_address = models.CharField(max_length=100, blank=True, null=True)
    country_hq_address = models.CharField(max_length=100, blank=True, null=True)
    zip_hq_address = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.business_id


class History_Redeemables(models.Model):
    history_redeemables_id  = models.AutoField(primary_key= True)
    benefit_id              = models.IntegerField(blank=False)
    subscription_id         = models.IntegerField(blank=False)
    customer_id             = models.IntegerField(blank=False)
    set_expiration          = models.DateTimeField(blank=True, null=True)
    method_redeemed         = models.BooleanField(default=False)

    def __str__(self):
        return self.historgy_redeemables_id

class SubscriptionPlan(models.Model):
    subscription_plan_id        = models.AutoField(primary_key=True)
    business_id                 = models.ForeignKey("Business", on_delete=models.CASCADE)
    title                       = models.CharField(blank=False)
    description                 = models.CharField(blank=False)
    amount                      = models.IntegerField(blank=False)
    recurring                   = models.BooleanField(blank=False)
    monthly_recurring           = models.BooleanField(blank=False, default=False)
    yearly_recurring            = models.BooleanField(blank=False, default=False)




class Benefit(models.Model):
    benefit_id      = models.AutoField(primary_key=True)
    business_id     = models.ForeignKey("Business", on_delete=models.CASCADE)
    title           = models.CharField(blank=False)
    description     = models.CharField(blank=False)
    quantity        = models.IntegerField(default=1)



class Benefit_Routing(models.Model):
    benefit_routing_id      = models.AutoField(primary_key=True)
    subscription_id         = models.ForeignKey("Subscription",  on_delete=models.CASCADE)
   # benefit_id              = models.
    quantity                = models.IntegerField()



class ActiveRedeemables(models.Model):
    active_redeemables_id       = models.AutoField(primary_key=True)
    benefit_id                  = models.ForeignKey("Benefit", on_delete=models.CASCADE)
    subscription_plan_id        = models.ForeignKey("SubscriptionPlan", on_delete=models.CASCADE)
    customer_id                 = models.ForeignKey("Customer", on_delete=models.CASCADE)
    expiration                  = models.DateTimeField()


