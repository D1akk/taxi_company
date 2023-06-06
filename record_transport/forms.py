from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Driver, Car, Task
from django.core.exceptions import ValidationError



class RegisterAdminForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя")
    middle_name = forms.CharField(label="Отчество(если имеется)")
    last_name = forms.CharField(label="Фамилия")
    birthday = forms.DateField(label="Дата рождения",widget=forms.DateInput(attrs={'type':'date'}))
    email = forms.CharField(label='Электронная почта')
    number = forms.CharField(label='Номер телефона')
    address = forms.CharField(label='Адрес проживания')

    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','middle_name','last_name','birthday','email','number', 'address']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.is_staff = True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegisterDriverForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя")
    middle_name = forms.CharField(label="Отчество(если имеется)")
    last_name = forms.CharField(label="Фамилия")
    gender = forms.CharField(label='Пол')
    birthday = forms.DateField(label="Дата рождения",widget=forms.DateInput(attrs={'type':'date'}))
    email = forms.CharField(label='Электронная почта')
    number = forms.CharField(label='Номер телефона')
    address = forms.CharField(label='Адрес проживания')
    range = forms.CharField(label='Стаж')
    license_number = forms.CharField(label='Номер лицензии')
    license_expiry = forms.CharField(label='Срок действия лицензии',widget=forms.DateInput(attrs={'type':'date'}))
    
    car_mark = forms.CharField(label='Марка')
    car_model = forms.CharField(label='Модель')
    car_year = forms.CharField(label='Год выпуска', widget=forms.DateInput(attrs={'type':'date'}))
    car_color = forms.CharField(label='Цвет')
    car_number = forms.CharField(label='Номер')
    car_mileage = forms.CharField(label='Пробег')
    car_fuel = forms.CharField(label='Тип топлива')
    car_transmission = forms.CharField(label='Коробка передач')
    car_engine = forms.DecimalField(label='Объем двигателя', max_digits=4, decimal_places=1)
    car_passangers = forms.IntegerField(label='Количество пассажирских мест')
    car_description = forms.CharField(label='Примечания',widget=forms.Textarea, required=False)
    car_pokazatel = forms.FloatField(label='Показатель расхода топлива', required=False)
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ['username','password1','password2','first_name','middle_name','last_name','gender','birthday','number','email','address','range', 'license_number','license_expiry', 'car_mark','car_model','car_year','car_color','car_number','car_mileage','car_fuel','car_transmission','car_engine','car_pokazatel','car_passangers','car_description']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        
        driver = super().save(commit=False)
        driver.is_staff = False
        driver.set_password(self.cleaned_data["password1"])
        if commit:
            driver.save()
            car = Car.objects.create(
                driver=driver,
                mark=self.cleaned_data['car_mark'],
                model=self.cleaned_data['car_model'],
                year=self.cleaned_data['car_year'],
                color=self.cleaned_data['car_color'],
                number=self.cleaned_data['car_number'],
                mileage=self.cleaned_data['car_mileage'],
                fuel_type=self.cleaned_data['car_fuel'],
                transmission=self.cleaned_data['car_transmission'],
                engine_capacity=self.cleaned_data['car_engine'],
                pokazatel=self.cleaned_data['car_pokazatel'],
                description=self.cleaned_data['car_description'],
            )
        return driver
    

class TaskForm(forms.ModelForm):
    driver = forms.ModelChoiceField(label='Выберите водителя', queryset=Driver.objects.all())
    title = forms.CharField(label='Название')
    client = forms.CharField(label='Клиент')
    price = forms.CharField(label='Стоимость')
    people = forms.CharField(label='Количество пассажиров')
    date = forms.CharField(label='Дата выполнения', widget=forms.DateTimeInput(attrs={'type':'date'}))
    time = forms.CharField(label='Время выполнения',widget=forms.DateTimeInput(attrs={'type':'time'}))
    description = forms.CharField(label='Примечание', required=False)
    complete = forms.BooleanField(label='Выполнено', widget=forms.CheckboxInput(), required=False)
    distance = forms.FloatField(label='Пройденное расстояние, км', required=False)
    fuel_before = forms.FloatField(label='Показания одометра при выезде на заказ', required=False)
    fuel_after = forms.FloatField(label='Показания одометра при возвращении с заказа', required=False)

    class Meta:
        model = Task
        fields = ['driver','title','client','price','people','date','time','description','complete','distance','fuel_before','fuel_after']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)

        if not user.is_staff:
            self.fields['driver'].disabled = True
            self.fields['title'].disabled = True
            self.fields['client'].disabled = True
            self.fields['price'].disabled = True
            self.fields['description'].disabled = True
            self.fields['people'].disabled = True
            self.fields['time'].disabled = True
            self.fields['date'].disabled = True

            self.fields['driver'].widget = forms.HiddenInput()
            self.fields['title'].widget = forms.HiddenInput()
            self.fields['driver'].widget = forms.HiddenInput()
            self.fields['client'].widget = forms.HiddenInput()
            self.fields['price'].widget = forms.HiddenInput()
            self.fields['description'].widget = forms.HiddenInput()
            self.fields['people'].widget = forms.HiddenInput()
            self.fields['time'].widget = forms.HiddenInput()
            self.fields['date'].widget = forms.HiddenInput()
            
        elif user.is_staff:
            self.fields['complete'].widget.attrs['disabled'] = True
            self.fields['complete'].widget = forms.HiddenInput()
            self.fields['distance'].disabled = True
            self.fields['distance'].widget = forms.HiddenInput()

            self.fields['fuel_before'].disabled = True
            self.fields['fuel_after'].disabled = True
            
            self.fields['fuel_before'].widget = forms.HiddenInput()
            self.fields['fuel_after'].widget = forms.HiddenInput()
