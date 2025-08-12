from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import EquipmentNameForm, EquipmentPosFormSet, EquipmentPosForm
from .models import EquipmentPos, EquipmentName, LegalEntity, EquipClass, EquipSubClass, Department, Shop

def equipment_list(
    request,
    entity_id=None,
    class_id=None,
    subclass_id=None,
    department_id=None,
    shop_id=None
):
    """
    Представление для отображения списка оборудования с фильтрацией по юридическому лицу, классу, подклассу, отделу и цеху.
    Все параметры являются необязательными и могут быть равны None или 0 (означает "все").
    """
    # Получаем все юридические лица
    legal_entities = LegalEntity.objects.order_by('name')

    # Инициализация выбранных объектов
    selected_entity = None
    selected_class = None
    selected_subclass = None
    equip_subclasses = None
    selected_department = None
    selected_shop = None

    departments = Department.objects.none()
    shops = Shop.objects.none()

    # Фильтрация по юридическому лицу
    if entity_id:
        selected_entity = get_object_or_404(LegalEntity, id=entity_id)
        departments = Department.objects.filter(legal_entity=selected_entity).order_by('name')
        # Filter equipment classes by the selected legal entity
        equip_classes = EquipClass.objects.filter(
            equipmentname__positions__legal_entity=selected_entity
        ).distinct().order_by('name')
    else:
        equip_classes = EquipClass.objects.order_by('name')

    # Фильтрация по классу оборудования
    if class_id:
        selected_class = get_object_or_404(EquipClass, id=class_id)
        equip_subclasses = EquipSubClass.objects.filter(equip_class=selected_class).order_by('name')

    # Фильтрация по подклассу оборудования
    if subclass_id:
        selected_subclass = get_object_or_404(EquipSubClass, id=subclass_id)

    # Фильтрация по отделу
    if department_id:
        if department_id != 0:
            selected_department = get_object_or_404(Department, id=department_id)
            shops = Shop.objects.filter(department=selected_department).order_by('name')

    # Фильтрация по цеху
    if shop_id:
        if shop_id != 0:
            selected_shop = get_object_or_404(Shop, id=shop_id)

    # Формируем queryset для позиций оборудования с учетом выбранных фильтров
    equipment_pos_qs = EquipmentPos.objects.all()
    if selected_entity:
        equipment_pos_qs = equipment_pos_qs.filter(legal_entity=selected_entity)
    if selected_department:
        equipment_pos_qs = equipment_pos_qs.filter(department=selected_department)
    if selected_shop:
        equipment_pos_qs = equipment_pos_qs.filter(shop=selected_shop)
    if selected_class:
        equipment_pos_qs = equipment_pos_qs.filter(equipment_name__equip_class=selected_class)
    if selected_subclass:
        equipment_pos_qs = equipment_pos_qs.filter(equipment_name__equip_subclass=selected_subclass)

    # Получаем уникальные имена оборудования для отображения
    equipment_names = EquipmentName.objects.filter(positions__in=equipment_pos_qs).distinct()

    # Передаем все необходимые переменные в шаблон
    return render(request, 'equipment/equipment_list.html', {
        'legal_entities': legal_entities,
        'selected_entity': selected_entity,
        'equip_classes': equip_classes,
        'selected_class': selected_class,
        'equip_subclasses': equip_subclasses,
        'selected_subclass': selected_subclass,
        'departments': departments,
        'selected_department': selected_department,
        'shops': shops,
        'selected_shop': selected_shop,
        'equipment_names': equipment_names,
    })

def equipment_create(request):
    """
    Представление для создания новой позиции оборудования.
    """
    # Если форма отправлена, сохраняем данные
    if request.method == 'POST':
        form = EquipmentPosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment:equipment_list')
    else:
        # Иначе отображаем пустую форму
        form = EquipmentPosForm()
    return render(request, 'equipment/equipment_form.html', {'form': form})

def equipment_detail(request, pk):
    """
    Представление для отображения подробной информации об оборудовании.
    """
    equipment_name = EquipmentName.objects.get(pk=pk)
    equipment_class = equipment_name.equip_class
    equipment_subclass = equipment_name.equip_subclass
    positions = EquipmentPos.objects.filter(equipment_name=equipment_name).select_related('shop', 'department', 'legal_entity')

    return render(request, 'equipment/equipment_detail.html', {
        'equipment_name': equipment_name,
        'equipment_class': equipment_class,
        'equipment_subclass': equipment_subclass,
        'positions': positions,
    })

def equipment_edit(request, name_id):
    """
    Представление для редактирования информации об оборудовании.
    """
    # Получаем объект EquipmentName
    equipment_name = get_object_or_404(EquipmentName, id=name_id)
    # Если форма отправлена, сохраняем изменения
    if request.method == 'POST':
        form = EquipmentNameForm(request.POST, instance=equipment_name)
        formset = EquipmentPosFormSet(request.POST, instance=equipment_name)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('equipment:equipment_detail', name_id=equipment_name.id)
    else:
        # Иначе отображаем форму с текущими данными
        form = EquipmentNameForm(instance=equipment_name)
        formset = EquipmentPosFormSet(instance=equipment_name)
    return render(request, 'equipment/equipment_edit.html', {
        'form': form,
        'formset': formset,
        'equipment_name': equipment_name,
    })

def get_classes_by_entity(request, entity_id):
    """
    AJAX view to fetch equipment classes based on the selected legal entity.
    """
    if entity_id:
        departments = Department.objects.filter(legal_entity_id=entity_id)
        equip_classes = EquipClass.objects.filter(
            equipmentname__positions__department__in=departments
        ).distinct()
    else:
        equip_classes = EquipClass.objects.all()

    classes_data = [{'id': eqclass.id, 'name': eqclass.name} for eqclass in equip_classes]
    return JsonResponse({'classes': classes_data})

def get_subclasses_by_class(request, class_id):
    """
    AJAX view to fetch equipment subclasses based on the selected class.
    """
    if class_id:
        equip_subclasses = EquipSubClass.objects.filter(equip_class_id=class_id).order_by('name')
    else:
        equip_subclasses = EquipSubClass.objects.none()

    subclasses_data = [{'id': subclass.id, 'name': subclass.name} for subclass in equip_subclasses]
    return JsonResponse({'subclasses': subclasses_data})