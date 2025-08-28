from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Repairs, Job, Reason, RepairType
from .forms import RepairsForm
from equipment.models import EquipmentPos, Shop, LegalEntity, EquipmentName, Department

def repairs_list(request):
    legal_entity_id = request.GET.get('legalentity')
    department_id = request.GET.get('department')
    shop_id = request.GET.get('shop')
    equipment_pos_id = request.GET.get('pos')
    job_id = request.GET.get('job')
    reason_id = request.GET.get('reason')
    repair_type_id = request.GET.get('repair_type')
    start_date_from = request.GET.get('start_date_from')
    start_date_to = request.GET.get('start_date_to')

    repairs = Repairs.objects.select_related(
        'equipment_name', 'shop', 'legalentity', 'job', 'reason', 'repair_type', 'pos'
    ).all().order_by('-start')

    if legal_entity_id:
        repairs = repairs.filter(legalentity_id=legal_entity_id)
    if department_id:
        repairs = repairs.filter(pos__department_id=department_id)
    if shop_id:
        repairs = repairs.filter(shop_id=shop_id)
    if equipment_pos_id:
        repairs = repairs.filter(pos_id=equipment_pos_id)
    if job_id:
        repairs = repairs.filter(job_id=job_id)
    if reason_id:
        repairs = repairs.filter(reason_id=reason_id)
    if repair_type_id:
        repairs = repairs.filter(repair_type_id=repair_type_id)
    if start_date_from:
        repairs = repairs.filter(start__date__gte=start_date_from)
    if start_date_to:
        repairs = repairs.filter(start__date__lte=start_date_to)

    paginator = Paginator(repairs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    legal_entities = LegalEntity.objects.order_by('name')
    departments = Department.objects.filter(legal_entity_id=legal_entity_id).order_by('name') if legal_entity_id else Department.objects.none()
    shops = Shop.objects.filter(department_id=department_id).order_by('name') if department_id else Shop.objects.none()
    positions = EquipmentPos.objects.filter(shop_id=shop_id).order_by('pos') if shop_id else EquipmentPos.objects.none()

    jobs = Job.objects.all()
    reasons = Reason.objects.all()
    repair_types = RepairType.objects.all()

    return render(request, 'repairs/repairs_list.html', {
        'page_obj': page_obj,
        'legal_entities': legal_entities,
        'departments': departments,
        'shops': shops,
        'positions': positions,
        'jobs': jobs,
        'reasons': reasons,
        'repair_types': repair_types,
        'start_date_from': start_date_from,
        'start_date_to': start_date_to,
        'selected_entity': LegalEntity.objects.filter(id=legal_entity_id).first() if legal_entity_id else None,
        'selected_department': Department.objects.filter(id=department_id).first() if department_id else None,
        'selected_shop': Shop.objects.filter(id=shop_id).first() if shop_id else None,
        'selected_pos': EquipmentPos.objects.filter(id=equipment_pos_id).first() if equipment_pos_id else None,
        # Pass filter values for pagination
        'legal_entity_id': legal_entity_id,
        'department_id': department_id,
        'shop_id': shop_id,
        'equipment_pos_id': equipment_pos_id,
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
    legal_entity_id = request.GET.get('legalentity')
    department_id = request.GET.get('department')
    shops = Shop.objects.all()
    if legal_entity_id:
        shops = shops.filter(department__legal_entity_id=legal_entity_id)
    if department_id:
        shops = shops.filter(department_id=department_id)
    shops = shops.values('id', 'name')
    return JsonResponse(list(shops), safe=False)

def get_equipment_positions(request):
    legal_entity_id = request.GET.get('legalentity')
    department_id = request.GET.get('department')
    shop_id = request.GET.get('shop')
    positions = EquipmentPos.objects.all()
    if legal_entity_id:
        positions = positions.filter(legal_entity_id=legal_entity_id)
    if department_id:
        positions = positions.filter(department_id=department_id)
    if shop_id:
        positions = positions.filter(shop_id=shop_id)
    positions = positions.values('id', 'pos')
    return JsonResponse(list(positions), safe=False)
