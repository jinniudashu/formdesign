

{
    'name': 'que_ren_dan_baseform', 
    'label': '确认单', 
    'mutate_or_inquiry': 'mutate', 
    'style': 'detail', 
    'basemodel': 'que_ren_dan', 
    'fields': [
        {
            'name': 'boolfield_yu_yue_que_ren', 
            'label': '确认', 
            'type': 'boolean'
        }
    ]
}

[
    {
        'name': 'yu_yue_biao_baseform', 
        'label': '预约单', 
        'mutate_or_inquiry': 'mutate', 
        'style': 'detail', 
        'basemodel': 'yu_yue_biao', 
        'fields': [
            {
                'name': 'datetimefield_ri_qi_shi_jian', 
                'label': '日期时间', 
                'type': 'datetime'
            }
        ]
    }, 
    {
        'name': 'basic_personal_information_baseform_query_1642159528', 
        'label': '个人基本情况_查询视图_1642159528', 
        'mutate_or_inquiry': 'inquiry', 
        'style': 'detail', 
        'basemodel': 'basic_personal_information', 
        'fields': [
            {
                'name': 'characterfield_name', 
                'label': '姓名', 
                'type': 'string'
            }, 
            {'name': 'characterfield_contact_number', 'label': '联系电话', 'type': 'string'}, {'name': 'datetimefield_date_of_birth', 'label': '出生日期', 'type': 'datetime'}, {'name': 'relatedfield_gender', 'label': '性别', 'type': 'dict', 'dict_name': 'Gender'}]}]


{
    'name': 'basic_personal_information_baseform', 
    'label': '个人基本情况', 
    'mutate_or_inquiry': 'mutate', 
    'style': 'detail', 
    'basemodel': 'basic_personal_information', 
    'fields': [
        {
            'name': 'boolfield_contract_signatory', 
            'label': '合同签约户', 
            'type': 'boolean'
        }, {
            'name': 'characterfield_name', 
            'label': '姓名', 
            'type': 'string'
        }, {
            'name': 'characterfield_identification_number', 
            'label': '身份证号码', 
            'type': 'string'
        }, {
            'name': 'characterfield_resident_file_number', 
            'label': '居民档案号', 
            'type': 'string'
        }, {
            'name': 'characterfield_family_address', 
            'label': '家庭地址', 
            'type': 'string'
        }, {
            'name': 'characterfield_contact_number', 
            'label': '联系电话', 
            'type': 'string'
        }, {
            'name': 'characterfield_medical_ic_card_number', 
            'label': '医疗ic卡号', 
            'type': 'string'
        }, {
            'name': 'datetimefield_date_of_birth', 
            'label': '出生日期', 
            'type': 'datetime'
        }, {
            'name': 'relatedfield_family_id', 
            'label': '家庭编号', 
            'type': 'dict', 
            'dict_name': 'Icpc1_register_logins'
        }, {
            'name': 'relatedfield_gender', 
            'label': '性别', 
            'type': 'dict', 
            'dict_name': 'Gender'
        }, {
            'name': 'relatedfield_nationality', 
            'label': '民族', 
            'type': 'dict', 
            'dict_name': 'Nationality'
        }, {
            'name': 'relatedfield_marital_status', 
            'label': '婚姻状况', 
            'type': 'dict', 
            'dict_name': 'Marital_status'
        }, {
            'name': 'relatedfield_education', 
            'label': '文化程度', 
            'type': 'dict', 
            'dict_name': 'Education'
        }, {
            'name': 'relatedfield_occupational_status', 
            'label': '职业状况', 
            'type': 'dict', 
            'dict_name': 'Occupational_status'
        }, {
            'name': 'relatedfield_medical_expenses_burden', 
            'label': '医疗费用负担', 
            'type': 'dict', 
            'dict_name': 
            'Medical_expenses_burden'
        }, {
            'name': 'relatedfield_type_of_residence', 
            'label': '居住类型', 
            'type': 'dict', 
            'dict_name': 'Type_of_residence'
        }, {'name': 'relatedfield_blood_type', 'label': '血型', 'type': 'dict', 'dict_name': 'Blood_type'}, {'name': 'relatedfield_signed_family_doctor', 'label': '签约家庭医生', 'type': 'dict', 'dict_name': 'Staff'}, {'name': 'relatedfield_family_relationship', 'label': '家庭成员关系', 'type': 'dict', 'dict_name': 'Family_relationship'}]}