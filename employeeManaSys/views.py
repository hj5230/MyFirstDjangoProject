from django.shortcuts import redirect, render
from employeeManaSys import models
from django import forms
from employeeManaSys.utils.secure import md5

def mainPage(request):
    return render(request, 'mainPage.html')

'''部门管理'''
def departList(request):
    departs = models.Department.objects.all()
    return render(request, 'departList.html', {'departs': departs})

def departAdd(request):
    if request.method == 'GET':
        return render(request, 'departAdd.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')

def departDelete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def departEdit(request, nid):
    if request.method == 'GET':
        row = models.Department.objects.filter(id=nid).first()
        return render(request, 'departEdit.html', {'nid': nid, 'title': row.title})
    id = request.POST.get('id')
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    models.Department.objects.filter(id=nid).update(id=id)
    return redirect('/depart/list/')

'''用户管理'''
def userList(request):
    persons = models.Personnel.objects.all()
    # for obj in persons:
    #     print(obj.create_time.strftime("%Y-%m-%d"), obj.depart.title)
    return render(request, 'userList.html', {"persons": persons})

def userAdd(request):
    if request.method == 'GET':
        departs = models.Department.objects.all()
        return render(request, 'userAdd.html', {'departs': departs})
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    depart_id = request.POST.get('depart_id')
    models.Personnel.objects.create(name=name, pwd=pwd, age=age,
        account=account, create_time=create_time, 
        depart_id=depart_id)
    return redirect("/user/list/")

class personModel(forms.ModelForm):
    '''验证规则
    name = forms.CharField(label='姓名', min_length=4)
    pwd = forms.CharField(label='密码', validators='正则表达式')
    '''
    class Meta:
        model = models.Personnel
        fields = ["name", "pwd", "age", "account",
           "create_time", "depart"]
        widgets = {
            'pwd': forms.PasswordInput(attrs={
                'type': 'password',
                'class': 'form-control',
                'style': 'margin-bottom: 15px',
                'placeholder': '密码'
            })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'pwd':
                continue
            field.widget.attrs = {
                'class': 'form-control',
                'style': 'margin-bottom: 15px',
                'placeholder': field.label
                }

def userAddM(request):
    if request.method == 'GET':
        form = personModel()
        return render(request, 'userAddM.html', {'form': form})
    form = personModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'userAddM.html', {'form': form})

def userEdit(request, nid):
    row = models.Personnel.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = personModel(instance=row)
        return render(request, 'userEdit.html', {'form': form})
    form = personModel(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'userEdit.html', {'form': form})

def userDelete(request, nid):
    models.Personnel.objects.filter(id=nid).delete()
    return redirect('/user/list/')

class loginForm(forms.Form):
    unm = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 15px',
            'placeholder': '用户名',
        }),
    )
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 15px',
            'placeholder': '密码',
        }),
    )
    def cleanPassword(self):
        pwd = self.cleaned_data.get('pwd')
        return md5(pwd)

def login(request):
    if request.method == 'GET':
        form = loginForm()
        return render(request, 'login.html', {'form': form})
    form = loginForm(data=request.POST)
    if form.is_valid():
        admin = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin:
            form.add_error('pwd', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        request.session['user'] = admin.unm
        return redirect('/1/')
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.clear()
    return redirect('/login/')