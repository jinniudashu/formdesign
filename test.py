

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
