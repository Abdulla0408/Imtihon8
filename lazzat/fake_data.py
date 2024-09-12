from . import models

def fake_datas():
    staff_1 = models.Staff.objects.create(first_name='Xurmatillo', last_name='Ganiyev', phone='998901234567', age=17, address='Vodil')
    staff_2 = models.Staff.objects.create(first_name='Behruz', last_name='Mirzadavlatov', phone='998997654321', age=18, address='Chinortagi')
    staff_3 = models.Staff.objects.create(first_name='Abdulaziz', last_name='Karimov', phone='998911234567', age=16, address='Novkent')
    staff_4 = models.Staff.objects.create(first_name='Muhammadyusuf', last_name='Ibrohimjonov', phone='998977651234', age=19, address='Vodil')
    staff_5 = models.Staff.objects.create(first_name='Bobur', last_name='Gulomov', phone='998947654578', age=25, address='Yangichek')

    
    print(f"Created: {staff_1}, {staff_2}, {staff_3}, {staff_4, {staff_5}}")