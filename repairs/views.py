from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Repairs
from .forms import RepairsForm
from equipment.models import LegalEntity, Shop, EquipmentPos

def repairs_list(request):
    repairs = Repairs.objects.select_related(
        'equipment_pos__equipment_name',
        'equipment_pos__shop',
        'legal_entity'
    ).all().order_by('-start')

    legal_entity_id = request.GET.get('legal_entity')
    shop_id = request.GET.get('shop')
    equipment_pos_id = request.GET.get('equipment_pos')
    start_date_from = request.GET.get('start_date_from')
    start_date_to = request.GET.get('start_date_to')

    if legal_entity_id:
        repairs = repairs.filter(legal_entity_id=legal_entity_id)
    if shop_id:
        repairs = repairs.filter(equipment_pos__shop_id=shop_id)
    if equipment_pos_id:
        repairs = repairs.filter(equipment_pos_id=equipment_pos_id)
    if start_date_from:
        repairs = repairs.filter(start__date__gte=start_date_from)
    if start_date_to:
        repairs = repairs.filter(start__date__lte=start_date_to)

    paginator = Paginator(repairs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    legal_entities = LegalEntity.objects.all()
    if legal_entity_id:
        shops = Shop.objects.filter(department__legal_entity_id=legal_entity_id).distinct()
    else:
        shops = Shop.objects.all()

    positions = EquipmentPos.objects.all()
    if legal_entity_id:
        positions = positions.filter(legal_entity_id=legal_entity_id)
    if shop_id:
        positions = positions.filter(shop_id=shop_id)

    return render(request, 'repairs/repairs_list.html', {
        'page_obj': page_obj,
        'legal_entities': legal_entities,
        'shops': shops,
        'positions': positions,
        'start_date_from': start_date_from,
        'start_date_to': start_date_to,
    })

def repairs_add(request):
    RepairsFormSet = modelformset_factory(Repairs, form=RepairsForm, extra=1, can_delete=False)
    if request.method == 'POST':
        formset = RepairsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('repairs:repairs_list')
    else:
        formset = RepairsFormSet(queryset=Repairs.objects.none())
    return render(request, 'repairs/repairs_add.html', {'formset': formset})

def get_shops(request):
    legal_entity_id = request.GET.get('legal_entity')
    shops = Shop.objects.filter(department__legal_entity_id=legal_entity_id).values('id', 'name')
    return JsonResponse(list(shops), safe=False)

def get_equipment_positions(request):
    legal_entity_id = request.GET.get('legal_entity')
    shop_id = request.GET.get('shop')
    positions = EquipmentPos.objects.filter(
        legal_entity_id=legal_entity_id, shop_id=shop_id
    ).values('id', 'pos')  # Use 'pos' instead of 'name'
    return JsonResponse(list(positions), safe=False)
