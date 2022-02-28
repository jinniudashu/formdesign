from django.core.management import BaseCommand
import json

from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component, RelateFieldModel
from define_dict.models import DicDetail, DicList, ManagedEntity
from define_form.models import BaseModel, BaseForm, CombineForm
from define_operand.models import ServicePackage, Service, Operation, Event, Instruction, Event_instructions, Role
from define_icpc.models import Icpc

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

            # 删除所有数据
            Role.objects.all().delete()
            ManagedEntity.objects.all().delete()
            DicDetail.objects.all().delete()
            DicList.objects.all().delete()
            RelateFieldModel.objects.all().delete()
            BoolField.objects.all().delete()
            CharacterField.objects.all().delete()
            NumberField.objects.all().delete()
            DTField.objects.all().delete()
            ChoiceField.objects.all().delete()
            RelatedField.objects.all().delete()
            Component.objects.all().delete()
            BaseModel.objects.all().delete()
            BaseForm.objects.all().delete()
            CombineForm.objects.all().delete()
            ServicePackage.objects.all().delete()
            Service.objects.all().delete()
            Operation.objects.all().delete()
            Instruction.objects.all().delete()
            Event.objects.all().delete()
            Event_instructions.objects.all().delete()

            # 导入角色表
            for item in design_data['roles']:
                print('Role:', item)
                Role.objects.create(**item)
            print('导入角色表完成')

            # 导入DicList表，自动插入RelateFieldModel表内容
            for item in design_data['diclists']:
                print('DicList:', item)
                DicList.objects.create(**item)
            
            # 导入DicDetail表
            for item in design_data['dicdetails']:
                print('DicDetail:', item)
                diclist = DicList.objects.get(name=item['diclist'])
                if item['icpc']:
                    icpc = Icpc.objects.get(icpc_code=item['icpc'])
                else:
                    icpc = None
                DicDetail.objects.create(
                    diclist=diclist,
                    item=item['item'],
                    icpc=icpc,
                )

            print('导入字典表完成')


            # ******************************************************
            # 导入管理实体表和字典表时自动插入RelateFieldModel表内容
            # ******************************************************
            # 导入管理实体表，自动插入RelateFieldModel表内容
            for item in design_data['managedentities']:
                ManagedEntity.objects.create(**item)

            # 初始化管理实体表，自动插入RelateFieldModel表内容
            # 创建ICPC类实体
            # for icpc in icpc_list:
            #     ManagedEntity.objects.create(
            #         name=icpc['name'].lower(),
            #         label=icpc['label'],
            #         app_name='define_icpc',
            #         model_name=icpc['name'],
            #         display_field='iname',
            #         related_field='icpc_code',
            #     )

            # 创建管理实体
            # entities_list = [
            #     {'name': 'staff', 'label': '职员', 'app_name': 'core', 'model_name': 'Staff', 'display_field': 'name', 'related_field': 'staff_code'},
            #     {'name': 'customer', 'label': '客户', 'app_name': 'core', 'model_name': 'Customer', 'display_field': 'name', 'related_field': 'customer_code'},
            #     {'name': 'supplier', 'label': '供应商', 'app_name': 'core', 'model_name': 'Supplier', 'display_field': 'name', 'related_field': 'supplier_code'},
            #     {'name': 'medicine', 'label': '药品', 'app_name': 'core', 'model_name': 'Medicine', 'display_field': 'name', 'related_field': 'medicine_code'},
            #     {'name': 'device', 'label': '设备', 'app_name': 'core', 'model_name': 'Device', 'display_field': 'name', 'related_field': 'device_code'},
            #     {'name': 'role', 'label': '角色', 'app_name': 'core', 'model_name': 'Role', 'display_field': 'name', 'related_field': 'role_code'},
            #     {'name': 'institution', 'label': '机构', 'app_name': 'core', 'model_name': 'Institution', 'display_field': 'name', 'related_field': 'institution_code'},
            # ]
            # for entity in entities_list:
            #     ManagedEntity.objects.create(**entity)

            print('导入管理实体表完成')

            # ******************************************************
            # 导入字段表、表单表、组合表、操作表、服务表、指令表、事件表
            # ******************************************************
            # 导入字段表
            for item in design_data['boolfields']:
                BoolField.objects.create(
                    name=item['name'],
                    label=item['label'],
                    type=item['type'],
                    required=item['required'],
                    default=item['default'],
                )
            print('导入布尔型字段表完成')

            for item in design_data['characterfields']:
                CharacterField.objects.create(
                    name=item['name'],
                    label=item['label'],
                    type=item['type'],
                    length=item['length'],
                    required=item['required'],
                    default=item['default'],
                )
            print('导入字符型字段表完成')

            for item in design_data['numberfields']:
                NumberField.objects.create(
                    name=item['name'],
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
                )
            print('导入数值型字段表完成')

            for item in design_data['dtfields']:
                DTField.objects.create(
                    name=item['name'],
                    label=item['label'],
                    type=item['type'],
                    default_now=item['default_now'],
                    required=item['required'],
                )
            print('导入日期型字段表完成')

            for item in design_data['choicefields']:
                ChoiceField.objects.create(
                    name=item['name'],
                    label=item['label'],
                    type=item['type'],
                    options=item['options'],
                    default_first=item['default_first'],
                    required=item['required'],
                )
            print('导入选择型字段表完成')

            for item in design_data['relatedfields']:
                related_content=RelateFieldModel.objects.get(name=item['related_content'])
                RelatedField.objects.create(
                    name=item['name'],
                    label=item['label'],
                    type=item['type'],
                    related_content=related_content,
                )
            print('导入关联型字段表完成')

            # 导入模型表
            for item in design_data['basemodels']:
                basemodel = BaseModel.objects.create(
                    name=item['name'],
                    label=item['label'],
                    description=item['description'],
                    is_base_infomation=item['is_base_infomation'],
                )

                model_components = []
                for _component in item['components']:
                    component = Component.objects.get(name=_component['name'])
                    model_components.append(component)
                basemodel.components.set(model_components)

                model_managedentities = []
                for _managedentity in item['managed_entity']:
                    managedentity = ManagedEntity.objects.get(name=_managedentity)
                    model_managedentities.append(managedentity)
                basemodel.managed_entity.set(model_managedentities)
            
            print('导入基础模型表完成')

            # 导入表单表
            for item in design_data['baseforms']:
                baseform = BaseForm.objects.create(
                    name=item['name'],
                    label=item['label'],
                    basemodel=BaseModel.objects.get(name=item['basemodel']),
                    is_inquiry=item['is_inquiry'],
                    style=item['style'],
                )

                form_components = []
                for _component in item['components']:
                    component = Component.objects.get(name=_component['name'])
                    form_components.append(component)
                baseform.components.set(form_components)
            
            print('导入基础表单表完成')

            # 导入组合表单表
            for item in design_data['combineforms']:
                if item['managed_entity']:
                    managed_entity=ManagedEntity.objects.get(name=item['managed_entity'])
                else:
                    managed_entity=None
                print(item)
                combineform = CombineForm.objects.create(
                    name=item['name'],
                    label=item['label'],
                    is_base=item['is_base'],
                    managed_entity=managed_entity,
                )

            for item in design_data['combineforms']:
                combineform = CombineForm.objects.get(name=item['name'])                
                forms = []
                for _form in item['forms']:
                    form = CombineForm.objects.get(name=_form)
                    forms.append(form)
                combineform.forms.set(forms)

            print('导入组合表单表完成')

            # 导入作业表
            for item in design_data['operations']:
                print('Operation:', item)
                if item['forms']:
                    forms = CombineForm.objects.get(name=item['forms'])
                else:
                    forms = None
                operation = Operation.objects.create(
                    name=item['name'],
                    label=item['label'],
                    forms=forms,  
                )
                # 写入Operation.group 多对多字段
                if item['group']:
                    groups = []
                    for _role in item['group']:
                        group = Role.objects.get(name=_role)  # 使用角色中文名称查询角色
                        groups.append(group)
                    operation.group.set(groups)


            print('导入作业表完成')


            # 导入服务表
            for item in design_data['services']:
                print('Service:', item)

                if item['first_operation']:
                    first_operation = Operation.objects.get(name=item['first_operation'])
                else:
                    first_operation = None
                
                service = Service.objects.create(
                    name=item['name'],
                    label=item['label'],
                    first_operation=first_operation,
                )

                # 写入Service.operations 多对多字段
                if item['operations']:
                    operations = []
                    for _operation in item['operations']:
                        operation = Operation.objects.get(name=_operation)
                        operations.append(operation)
                    service.operations.set(operations)

                # 写入Service.group 多对多字段
                if item['group']:
                    groups = []
                    for _role in item['group']:
                        group = Role.objects.get(name=_role)  # 使用角色中文名称查询角色
                        groups.append(group)
                    service.group.set(groups)
            
            print('导入服务表完成')
            
            # 导入服务包表
            for item in design_data['service_packages']:
                print('ServicePackage:', item)

                if item['first_service']:
                    first_service = Service.objects.get(name=item['first_service'])
                else:
                    first_service = None

                service_package = ServicePackage.objects.create(
                    name=item['name'],
                    label=item['label'],
                    first_service=first_service,
                )

                # 写入ServicePackage.services 多对多字段
                if item['services']:
                    services = []
                    for _service in item['services']:
                        service = Service.objects.get(name=_service)
                        services.append(service)
                    service_package.services.set(services)
            
            print('导入服务包表完成')


            # 导入指令表
            for item in design_data['instructions']:
                print('Instruction:', item)
                Instruction.objects.create(
                    name=item['name'],
                    label=item['label'],
                    code=item['code'],
                    func=item['func'],
                    description=item['description'],
                )
            
            print('导入指令表完成')
            
            # 导入事件表
            for item in design_data['events']:
                print('Event:', item)
                event = Event.objects.create(
                    name=item['name'],
                    label=item['label'],
                    operation=Operation.objects.get(name=item['operation']),
                    description=item['description'],
                    expression=item['expression'],
                    parameters=item['parameters'],
                    fields=item['fields'],
                )

                next_operations = []
                for _operation in item['next']:
                    operation = Operation.objects.get(name=_operation)
                    next_operations.append(operation)
                event.next.set(next_operations)
            
            print('导入事件表完成')

        else:
            print('Cancel restore design data...')
