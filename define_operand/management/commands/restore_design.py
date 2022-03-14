from django.core.management import BaseCommand
import json

from datetime import timedelta
import re

from define.models import *
from define_operand.models import Instruction, Event, Event_instructions, BuessinessForm, ServicePackage, ServicesSetting, Service, OperationsSetting, Operation, SystemOperand, Role
from define_icpc.models import Icpc
from define_rule_dict.models import EventRule, EventExpression, FrequencyRule, IntervalRule


class Command(BaseCommand):
    help = 'Import design from json file'

    def handle(self, *args, **options):

        # 如果是在生产系统上运行，请确认设计数据backup_design是最新版本的备份
        make_sure = input('''如果当前是在生产系统上操作，请确认设计数据backup_design是最新版本的备份！\n是否要开始恢复设计数据操作？(y/n)''')
        if make_sure == 'y':
            print('start restore design data...')

            # 读取备份数据文件
            with open('design_data_backup.json', encoding="utf8") as f:
                design_data = json.loads(f.read())

            RelateFieldModel.objects.all().delete()
            # 导入DicList表，自动插入RelateFieldModel表内容
            DicDetail.objects.all().delete()
            DicList.objects.all().delete()
            for item in design_data['diclists']:
                print('DicList:', item)
                DicList.objects.create(**item)

            # 导入DicDetail表
            for item in design_data['dicdetails']:
                # print('DicDetail:', item)
                diclist = DicList.objects.get(hssc_id=item['diclist'])
                if item['icpc']:
                    icpc = Icpc.objects.get(icpc_code=item['icpc'])
                else:
                    icpc = None

                DicDetail.objects.create(
                    diclist=diclist,
                    item=item['item'],
                    icpc=icpc,
                    hssc_id=item['hssc_id'],
                )

            print('导入字典表完成')


            # ******************************************************
            # 导入管理实体表和字典表时自动插入RelateFieldModel表内容
            # ******************************************************
            # 导入管理实体表，自动插入RelateFieldModel表内容
            ManagedEntity.objects.all().delete()

            for item in design_data['managedentities']:
                entity=ManagedEntity.objects.create(**item)

                # 修正管理实体表中ICPC实体的app_name
                # if entity.app_name=='define_icpc':
                #     entity.app_name='icpc'
                #     entity.save()

            print('导入管理实体表完成')

            # ******************************************************
            # 导入字段表、表单表、组合表、操作表、服务表、指令表、事件表
            # ******************************************************
            ComponentsGroup.objects.all().delete()
            Component.objects.all().delete()
            BoolField.objects.all().delete()
            CharacterField.objects.all().delete()
            NumberField.objects.all().delete()
            DTField.objects.all().delete()
            RelatedField.objects.all().delete()
            # 导入字段表
            for item in design_data['boolfields']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                BoolField.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    type=item['type'],
                    required=item['required'],
                    default=item['default'],
                    hssc_id=item['hssc_id'],
                )
            print('导入布尔型字段表完成')

            for item in design_data['characterfields']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                CharacterField.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    type=item['type'],
                    length=item['length'],
                    required=item['required'],
                    default=item['default'],
                    hssc_id=item['hssc_id'],
                )
            print('导入字符型字段表完成')

            for item in design_data['numberfields']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                NumberField.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    type=item['type'],
                    max_digits=item['max_digits'],
                    decimal_places=item['decimal_places'],
                    standard_value=item['standard_value'],
                    up_limit=item['up_limit'],
                    down_limit=item['down_limit'],
                    unit=item['unit'],
                    default=item['default'],
                    required=item['required'],
                    hssc_id=item['hssc_id'],
                )
            print('导入数值型字段表完成')

            for item in design_data['dtfields']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                DTField.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    type=item['type'],
                    default_now=item['default_now'],
                    required=item['required'],
                    hssc_id=item['hssc_id'],
                )
            print('导入日期型字段表完成')


            for item in design_data['relatedfields']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None
                related_content=RelateFieldModel.objects.get(hssc_id=item['related_content'])
                RelatedField.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    type=item['type'],
                    related_content=related_content,
                    hssc_id=item['hssc_id'],
                )
            print('导入关联型字段表完成')


            for item in design_data['componentsgroups']:
                if item['components']:
                    components = []
                    for component in item['components']:
                        components.append(Component.objects.get(hssc_id=component))
                else:
                    components=None

                components_group = ComponentsGroup.objects.create(
                    name=item['name'],
                    label=item['label'],
                    hssc_id=item['hssc_id'],
                )
                components_group.components.set(components)


            # 倒入旧表单
            from define_form.models import BaseModel, BaseForm, CombineForm
            BaseModel.objects.all().delete()
            BaseForm.objects.all().delete()
            CombineForm.objects.all().delete()
            # 导入模型表
            for item in design_data['basemodels']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None
                    
                basemodel = BaseModel.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    description=item['description'],
                    is_base_infomation=item['is_base_infomation'],
                    basemodel_id=item['basemodel_id'],
                )

                # 导入多对多字段
                _components=[]
                for index, component in enumerate(item['components']):
                    _components.append(component['hssc_id'])
                components=Component.objects.filter(hssc_id__in=_components)
                basemodel.components.set(components)

                # 导入多对多字段
                managedentities=ManagedEntity.objects.filter(hssc_id__in=item['managed_entity'])
                basemodel.managed_entity.set(managedentities)
            
            print('导入基础模型表完成')

            # 导入表单表
            for item in design_data['baseforms']:
                baseform = BaseForm.objects.create(
                    name=item['name'],
                    label=item['label'],
                    basemodel=BaseModel.objects.get(basemodel_id=item['basemodel']),
                    is_inquiry=item['is_inquiry'],
                    style=item['style'],
                    baseform_id=item['baseform_id'],
                )

                # 导入多对多字段
                _components=[]
                for index, component in enumerate(item['components']):
                    _components.append(component['hssc_id'])
                components=Component.objects.filter(hssc_id__in=_components)
                baseform.components.set(components)

            print('导入基础表单表完成')

            #  导入组合表单表
            for item in design_data['combineforms']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None
                if item['managed_entity']:
                    managed_entity=ManagedEntity.objects.get(hssc_id=item['managed_entity'])
                else:
                    managed_entity=None
                combineform = CombineForm.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    is_base=item['is_base'],
                    managed_entity=managed_entity,
                    combineform_id=item['combineform_id'],
                )
                # 导入多对多字段forms
                baseforms=BaseForm.objects.filter(baseform_id__in=item['forms'])
                combineform.forms.set(baseforms)

            # 初始化生成所有组合表单（自动生成+导入）的meta_data
            for item in CombineForm.objects.all():
                meta_data = []
                for form in item.forms.all():
                    meta_data.append(json.loads(form.meta_data))
                item.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
                item.save()

            print('导入组合表单表完成')

            # 导入BuessinessForm
            BuessinessForm.objects.all().delete()
            for item in design_data['buessinessforms']:
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                buessiness_form = BuessinessForm.objects.create(
                    name = item['name'],
                    name_icpc = name_icpc,
                    label = item['label'],
                    description = item['description'],
                    meta_data = item['meta_data'],
                    hssc_id = item['hssc_id'],
                )

                # 创建表单内容的多对多字段
                if item['components']:
                    components = []
                    for component in item['components']:
                        components.append(Component.objects.get(hssc_id=component))
                    buessiness_form.components.set(components)
                else:
                    components=None

                if item['components_groups']:
                    components_groups = []
                    for components_group in item['components_groups']:
                        components_groups.append(ComponentsGroup.objects.get(hssc_id=components_group))
                    buessiness_form.components_groups.set(components_groups)
                else:
                    components_groups=None

                if item['managed_entity']:
                    managed_entities = []
                    for managed_entity in item['managed_entity']:
                        managed_entities.append(ManagedEntity.objects.get(hssc_id=managed_entity))
                    buessiness_form.managed_entities.set(managed_entities)
                else:
                    managed_entities=None


            # # 导入业务规则表
            # EventRule.objects.all().delete()
            # for item in design_data['eventrules']:
            #     EventRule.objects.create(**item)
            # print('导入业务规则表完成')

            # # 导入频率规则表
            # FrequencyRule.objects.all().delete()
            # for item in design_data['frequencyrules']:
            #     FrequencyRule.objects.create(**item)
            # print('导入频率规则表完成')

            # 导入作业间隔规则表
            IntervalRule.objects.all().delete()
            for item in design_data['operandintervalrules']:
                interval = parse_timedelta(item['interval'])
                IntervalRule.objects.create(
                    name=item['name'],
                    label=item['label'],
                    rule=item['rule'],
                    interval=interval,
                    description=item['description'],
                    hssc_id=item['hssc_id'],
                )
            print('导入作业间隔规则表完成')


            Instruction.objects.all().delete()
            # 导入指令表
            for item in design_data['instructions']:
                # print('Instruction:', item)
                Instruction.objects.create(**item)
            
            print('导入指令表完成')

            # 导入系统作业表
            # SystemOperand.objects.all().delete()
            # for item in design_data['systemoperands']:
            #     SystemOperand.objects.create(**item)
            # print('导入系统作业表完成')


            # 导入角色表
            Role.objects.all().delete()
            for item in design_data['roles']:
                # print('Role:', item)
                Role.objects.create(**item)
            print('导入角色表完成')


            ServicesSetting.objects.all().delete()
            ServicePackage.objects.all().delete()
            OperationsSetting.objects.all().delete()
            Service.objects.all().delete()
            Operation.objects.all().delete()
            Event_instructions.objects.all().delete()
            Event.objects.all().delete()

            # 导入作业表
            for item in design_data['operations']:
                # print('Operation:', item)
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                if item['forms']:
                    combineform = CombineForm.objects.get(combineform_id=item['forms'])
                    forms = BuessinessForm.objects.get(name=combineform.name)
                else:
                    forms = None

                operation = Operation.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    forms=forms,
                    enable_queue_counter=item['enable_queue_counter'],
                    priority=item['priority'],
                    suppliers=item['suppliers'],
                    not_suitable=item['not_suitable'],
                    time_limits=item['time_limits'],
                    working_hours=item['working_hours'],
                    frequency=item['frequency'],
                    cost=item['cost'],
                    load_feedback=item['load_feedback'],
                    resource_materials=item['resource_materials'],
                    resource_devices=item['resource_devices'],
                    resource_knowledge=item['resource_knowledge'],
                    hssc_id=item['hssc_id'],
                )

                # 写入Operation.group 多对多字段
                if item['group']:
                    groups=Role.objects.filter(hssc_id__in=item['group'])
                    operation.group.set(groups)


                # 临时处理
                # 导入单元服务表
                unit_service = Service.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    first_operation=operation,
                    last_operation=None,   
                    enable_queue_counter=item['enable_queue_counter'],
                    priority=item['priority'],
                    suppliers=item['suppliers'],
                    not_suitable=item['not_suitable'],
                    time_limits=item['time_limits'],
                    working_hours=item['working_hours'],
                    frequency=item['frequency'],
                    cost=item['cost'],
                    load_feedback=item['load_feedback'],
                    resource_materials=item['resource_materials'],
                    resource_devices=item['resource_devices'],
                    resource_knowledge=item['resource_knowledge'],
                )
                # 写入Service.operations 多对多字段
                # unit_service.operations.set([operation])
                # 写入Service.group 多对多字段
                if item['group']:
                    groups=Role.objects.filter(hssc_id__in=item['group'])
                    unit_service.group.set(groups)

            print('导入作业表完成')


            # # 导入单元服务表
            # for item in design_data['services']:
            #     # print('Service:', item)
            #     if item['name_icpc']:
            #         name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
            #     else:
            #         name_icpc = None

            #     if item['first_operation']:
            #         first_operation = Operation.objects.get(operand_id=item['first_operation'])
            #     else:
            #         first_operation = None
                
            #     service = Service.objects.create(
            #         name=item['name'],
            #         name_icpc=name_icpc,
            #         label=item['label'],
            #         first_operation=first_operation,
            #         priority=item['priority'],
            #         suppliers=item['suppliers'],
            #         not_suitable=item['not_suitable'],
            #         time_limits=item['time_limits'],
            #         working_hours=item['working_hours'],
            #         frequency=item['frequency'],
            #         cost=item['cost'],
            #         load_feedback=item['load_feedback'],
            #         resource_materials=item['resource_materials'],
            #         resource_devices=item['resource_devices'],
            #         resource_knowledge=item['resource_knowledge'],
            #         service_id=item['service_id'],
            #     )

            #     # 写入Service.operations 多对多字段
            #     if item['operations']:
            #         operations = Operation.objects.filter(operand_id__in=item['operations'])
            #         service.operations.set(operations)

            #     # 写入Service.group 多对多字段
            #     if item['group']:
            #         groups=Role.objects.filter(role_id__in=item['group'])
            #         service.group.set(groups)
            
            # print('导入单元服务表完成')
            
            # 导入服务包表
            for item in design_data['service_packages']:
                # print('ServicePackage:', item)
                if item['name_icpc']:
                    name_icpc = Icpc.objects.get(icpc_code=item['name_icpc'])
                else:
                    name_icpc = None

                if item['first_service']:
                    first_service = Service.objects.get(service_id=item['first_service'])
                else:
                    first_service = None

                service_package = ServicePackage.objects.create(
                    name=item['name'],
                    name_icpc=name_icpc,
                    label=item['label'],
                    first_service=first_service,
                    service_package_id=item['service_package_id'],
                )

                # 写入ServicePackage.services 多对多字段
                if item['services']:
                    services = Service.objects.filter(service_id__in=item['services'])
                    service_package.services.set(services)
            
            print('导入服务包表完成')


            # 导入事件表
            for item in design_data['events']:
                Event.objects.create(
                    name=item['name'],
                    label=item['label'],
                    operation=Operation.objects.get(hssc_id=item['operation']),
                    description=item['description'],
                    expression=item['expression'],
                    parameters=item['parameters'],
                    fields=item['fields'],
                    event_id=item['event_id'],
                )

                # 临时处理
                # 导入服务作业关系表
                _operation = Operation.objects.get(hssc_id=item['operation'])
                _service = Service.objects.get(name=_operation.name)
                next_operations = item['next_operations']
                if item['expression'] == 'completed':
                    _event_rule = EventRule.objects.get(name='completed')
                else:
                    _event_rule = None
                for next_operation in next_operations:
                    _next_operation = Operation.objects.get(hssc_id=next_operation)
                    OperationsSetting.objects.create(
                        service=_service,
                        operation=_operation,
                        system_operand = SystemOperand.objects.get(id=1),  # 推荐后续作业
                        next_operation=_next_operation,
                        event_rule=_event_rule,
                    )
                
            print('导入事件表完成')


        else:
            print('Cancel restore design data...')


# 转换string to timedelta
def parse_timedelta(stamp):
    if 'day' in stamp:
        m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
    else:
        m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', stamp)
    if not m:
        return ''

    time_dict = {key: float(val) for key, val in m.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])