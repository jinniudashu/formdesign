########################################################################################################################
# Generate JS script 
########################################################################################################################
def generate_js_script(params):
    import openai
    from formdesign.settings import OPENAI_API_KEY

    openai.api_key = OPENAI_API_KEY

    messages = None

    # prompt = {'form_events': form_events, 'computed_fields': ''}  # 提示信息清单
    # 根据prompt调用不同的提示生成脚本
    if params.get('computed_fields'):
        messages = generate_computed_fields_prompt(params.get('computed_fields'))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages
    )
    result = response['choices'][0]['message']['content']
    print('usage:\n', response['usage'])
    
    return result


def generate_computed_fields_prompt(param):
    SYSTEM_PROMPT = 'You are a seasoned Javascript developer.'

    USER_INPUT_PREFIX = '''Please write concise JS code to automatically update computed fields on a web page form. The form definition is in "form definition" section. The computation logic is in "computation logic" section. Computed field values are obtained by calculating values from other fields in the form using the computation logic.
Use the 'document.addEventListener' method to listen for the DOMContentLoaded event and execute a callback function when the page is loaded. The callback function should follow these steps:
1. Use document.getElementById to retrieve the DOM elements of all fields involved in the computation logic. Follow this naming convention: the field name prefixed with "id_" is the field ID.
2. Write calculation functions to implementing the business logic based on the computation logics description one by one.
3. Write an update function for each computed field one by one, refreshing the related DOM element of the related computed field. Retrieve the values of relevant fields, call the relative calculation function from step 2, and assign the calculation result to the relative DOM elements of the computed fields.
4. Add input event listeners to the DOM elements of related fields involved in the computation logics, so that the relative updating function from step 3 is called when the user inputs values.
5. Put the final 'document.addEventListener' method into a <script> tag.
Follow the steps above, that's all you need to do, no more words needed.
    '''
    EXAMPLE_USER_INPUT = '''- form definition: {'boolfield_ti_wen': '体温', 'boolfield_mai_bo': '脉搏', 'boolfield_hu_xi_pin_lv': '呼吸频率', 'boolfield_shen_gao': '身高', 'boolfield_ti_zhong': '体重', 'boolfield_ti_zhi_zhi_shu': '体质指数', 'boolfield_shou_suo_ya': '收缩压', 'boolfield_shu_zhang_ya': '舒张压', 'boolfield_yao_wei': '腰围', 'boolfield_yan_bu': '咽部', 'boolfield_xia_zhi_shui_zhong': '下肢水肿'}
    - computation logic: ['体质指数=体重/身高的平方']
    '''

    EXAMPLE_USER_INPUT = USER_INPUT_PREFIX + EXAMPLE_USER_INPUT

    EXAMPLE_ASSISTANT_RESPONSE = '''<script>
        document.addEventListener('DOMContentLoaded', function() {
            // Retrieve DOM elements of all fields involved in the computation logic
            const boolfield_shen_gao = document.getElementById("id_boolfield_shen_gao");
            const boolfield_ti_zhong = document.getElementById("id_boolfield_ti_zhong");
            const boolfield_ti_zhi_zhi_shu = document.getElementById("id_boolfield_ti_zhi_zhi_shu");

            // Calculation function implementing the business logic
            const calculateBmi = (shenGao, tiZhong) => {
            if (shenGao > 0 && tiZhong > 0) {
                const shenGaoInMeters = shenGao / 100;
                return (tiZhong / (shenGaoInMeters * shenGaoInMeters)).toFixed(1);
            }
            return None;
            };

            // Update the DOM element of the computed field
            const update_boolfield_ti_zhi_zhi_shu = () => {
                const shen_gao = parseFloat(boolfield_shen_gao.value);
                const ti_zhong = parseFloat(boolfield_ti_zhong.value);
                boolfield_ti_zhi_zhi_shu.value = calculateBmi(shen_gao, ti_zhong);
            };

            // Add input event listener to related fields
            boolfield_shen_gao.addEventListener("input", update_boolfield_ti_zhi_zhi_shu);
            boolfield_ti_zhong.addEventListener("input", update_boolfield_ti_zhi_zhi_shu);
        });
    </script>'''

    prompt = USER_INPUT_PREFIX + param

    messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": EXAMPLE_USER_INPUT},
            {"role": "assistant", "content": EXAMPLE_ASSISTANT_RESPONSE},
            {"role": "user", "content": prompt}
        ]

    return messages


########################################################################################################################
# keyword_search
########################################################################################################################

def keyword_search(s, keywords_list):

    next = []
    match = []

    def buildNext():
        next.append(0)
        x = 1
        now = 0
        while x < len(p):
            if p[now] == p[x]:
                now += 1
                x += 1
                next.append(now)
            elif now:
                now = next[now-1]
            else:
                next.append(0)
                x += 1

    def search():
        tar = 0
        pos = 0
        while tar < len(s):
            if s[tar] == p[pos]:
                tar += 1
                pos += 1
            elif pos:
                pos = next[pos-1]
            else:
                tar += 1
            if pos == len(p):   # 匹配成功
                match.append(p)
                pos = next[pos-1]

    for p in keywords_list:
        buildNext()
        search()
    keywords = sorted(set(match), key=match.index)
    return keywords


########################################################################################################################
def generate_form_event_js_script(rules, domain, class_name, autofill_fields, show_icpc_hint):
    import json
    from define_icpc.models import HintFields

    rules_string = json.dumps(rules, ensure_ascii=False)
    keys = list(rules[0].keys())

    template_script_header = f'''
<script src="https://cdn.jsdelivr.net/npm/js-cookie@3.0.1/dist/js.cookie.min.js"></script>    
<script>
    document.addEventListener('DOMContentLoaded', async function() {{
        const domain = '{domain}';
        
        // 根据表单检测范围，从CustomerServiceLog获取历史记录，构造{keys[0]}数组上下文
        const customerId = Cookies.get('customer_id');
        const period = 'ALL';  // 'ALL' or 'LAST_WEEK_SERVICES'
        const form_class = 0;  // 指定表单类别
        const fetchCustomerServiceLogURL = `http://${{domain}}/core/api/customer_service_log/`;
        const fetchCustomerServiceLog = async (customerId, period=null, form_class=0) => {{
            let url = fetchCustomerServiceLogURL + `?customer=${{customerId}}`
            if (period !== null) {{
                url += `&period=${{period}}`;
            }}
            if (form_class > 0) {{
                url += `&form_class=${{form_class}}`;
            }}
            try {{
                const response = await fetch(url, {{
                    headers: {{
                        'Accept': 'application/json',
                    }}
                }});
                if (!response.ok) {{
                    throw new Error('HTTP error ' + response.status);
                }}
                const result = await response.json();
                // 将获取的{keys[0]}历史记录保存在数组中返回
                const logs = JSON.parse(result);
                arrayValue = logs.filter(log => log.fields.data.hasOwnProperty('{keys[0]}'))
                    .map(log => {{
                        s = log.fields.data.{keys[0]};
                        v = s.replace("{{", "").replace("}}", "").replace(/'/g, "")
                        return {{value: v, datetime: log.fields.created_time}};
                    }});
                return arrayValue;
            }} catch (error) {{
                console.error('Error:', error);
            }}
        }}
        const context_{keys[0]} = await fetchCustomerServiceLog(customerId, period, form_class);
        console.log(context_{keys[0]});'''
    
    if show_icpc_hint:
        hint_fields = HintFields.objects.all().last().hint_fields.split(',')
        template_script_show_icpc_hint = f'''
        // ******************************************
        // 显示字段提示
        // ******************************************
        const showIcpcHint = async (node) => {{
            const fetchIcpcItemURL = `http://${{domain}}/core/api/get_icpc_item/`;
            const fetchIcpcItem = async (node_field_name, itemId) => {{
                let url = fetchIcpcItemURL + `?fieldName=${{node_field_name}}&itemId=${{itemId}}`
                try {{
                    const response = await fetch(url, {{ headers: {{'Accept': 'application/json',}} }});
                    if (!response.ok) {{
                        throw new Error('HTTP error ' + response.status);
                    }}
                    const result = await response.json();
                    return result;
                }} catch (error) {{
                    console.error('Error:', error);
                    return null;
                }}
            }}

            // 1. 从node获取字段名称、itemId
            // 当前node字段名
            let parts = node.id.split('-')
            parts.pop()
            let node_field_name = parts.pop().substr(3)
            // 获取itemId
            const itemId = node.parentElement.parentElement.parentElement.parentElement.firstElementChild.value

            // 2. fetch API获取item详细信息
            const icpcItem = await fetchIcpcItem(node_field_name, itemId)

            // 3. 显示字段提示
            const hintFields = {hint_fields}
            const parentNode = node.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
            // 构造提示div
            let hintDiv = document.createElement("div")
            hintDiv.id = "dynamic_hint"; 
            hintFields.forEach(field => {{
                console.log(field, ":", icpcItem[field])
                let textContent = icpcItem[field]
                if ((textContent === null) || (textContent === undefined))
                    textContent = ''
                let newLabel = document.createElement("div")
                newLabel.textContent = `${{field}}: ${{textContent}}`
                hintDiv.appendChild(newLabel)
                hintDiv.appendChild(document.createElement("p"))
            }})
            existingHintDiv = parentNode.parentElement.querySelector('#dynamic_hint')
            if (existingHintDiv) {{
                parentNode.parentElement.removeChild(existingHintDiv)
            }}
            parentNode.insertAdjacentElement('afterend', hintDiv);
        }}'''
        template_script_call_show_icpc_hint = '''
                    // 显示字段提示
                    showIcpcHint(node)'''
    else:
        template_script_show_icpc_hint = ''
        template_script_call_show_icpc_hint = ''

    if autofill_fields:
        template_script_autofill_fields = '''
        // ******************************************
        // 自动补全字典明细相关字段
        // ******************************************
        // 从明细表表头提取表头数组，用于获取字段名称数组
        const thElements = document.querySelector('table thead tr').querySelectorAll('th')
        // 自动补全字典字段
        const autocompleteFields = async (node) => {
            const autocompleteFieldsURL = `http://${domain}/core/api/get_medicine_item/`;
            const fetchMedicineItem = async (itemId) => {
                let url = autocompleteFieldsURL + `?itemId=${itemId}`
                try {
                    const response = await fetch(url, { headers: {'Accept': 'application/json',} });
                    if (!response.ok) {
                        throw new Error('HTTP error ' + response.status);
                    }
                    const result = await response.json();
                    return result;
                } catch (error) {
                    console.error('Error:', error);
                    return null;
                }
            }

            // 获取item纪录明细
            const itemId = node.parentElement.parentElement.parentElement.parentElement.firstElementChild.value
            const medicineItem = await fetchMedicineItem(itemId)

            // 当前node字段名
            let parts = node.id.split('-')
            parts.pop()
            let node_field_name = parts.pop()
            // 当前tr
            const tr = node.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
            console.log('id:', itemId, node.getAttribute('title').trim())
            // 查找对应的<td>元素.input/select元素，填充相关属性字段
            thElements.forEach(th => {
                if ((th.className) && (th.className !== 'original')) {
                    // 从表头类名解析出字段名
                    let fieldName = th.className.split(' ')[0].split('-')[1]  
                    if (fieldName !== node_field_name) {
                        // 获取类名，用于从tr中查找节点
                        let classStr = '.field-' + fieldName
                        // 获取表头title，用于从item字典中查找对应键值
                        let title = th.innerText
                        console.log(title, ':', medicineItem[title])
                        // 获取节点
                        let relate_node = tr.querySelector(classStr).firstElementChild
                        // 根据类型写入键值
                        if (relate_node.nodeName === 'INPUT') {
                            relate_node.value = medicineItem[title]
                        } else if (relate_node.nodeName === 'DIV') {
                            relate_node.firstElementChild.value = medicineItem[title]
                        }
                    }
                }
            })
        }'''
        template_script_call_autofill_fields = '''
                    // 填充字典相关属性字段
                    autocompleteFields(node)'''
    else:
        template_script_autofill_fields = ''
        template_script_call_autofill_fields = ''
    
    if rules:
        template_script_detect_event = f'''
        // ******************************************
        // 检测是否发生符合特定规则的表单事件
        // ******************************************
        // 表单事件规则
        const content_conflict_rules = {rules_string}
        // 接受一条来自表单事件规则列表的规则, 如果发生表单事件，执行规则配置表中指定的表单事件动作
        const detect_form_event = (rule) => {{
            // 定义表单事件动作，接受一个选项，来自表单事件规则列表
            const form_event_action = (action, conflict_items) => {{
                // 把冲突项目数组转换为字符串
                const conflict_items_string = conflict_items.join('、');
                if (action === 'WARN') {{
                    // 警告用户内容冲突
                    alert(`表单内容冲突：${{conflict_items_string}}`);
                }} else if (action === 'PROHIBIT') {{
                    alert(`表单内容冲突：${{conflict_items_string}}`);
                    // 禁止保存表单
                    document.querySelector('input[name="_save"]').disabled = true;
                }}
            }}

            if (!current_values.{keys[1]}) return;

            // 构造冲突项列表
            const conflict_items = [];

            const events_context = {{
                event_0 : context_{keys[0]}.filter(item => rule.{keys[0]}.includes(item.value)).length > 0,
                event_1 : rule.{keys[1]}.includes(current_values.{keys[1]}),
            }}
            // 检测是否发生上下文冲突
            if (Object.values(events_context).every(value => value === true)) {{
                // 对于上下文冲突，添加产生冲突的具体疾病名称
                if (events_context.event_0) {{
                    const conflictingDiseases = context_{keys[0]}.filter(item => rule.{keys[0]}.includes(item.value)).map(item => item.value);
                    if (conflictingDiseases.length > 0) {{
                        conflict_items.push(conflictingDiseases.join(', '));
                    }}
                }}
                form_event_action(rule.form_event_action, conflict_items)
            }}

            const events_input = {{
                event_0 : new Set(rule.{keys[0]}).has(current_values.{keys[0]}),
                event_1 : rule.{keys[1]}.includes(current_values.{keys[1]}),
            }}
            // 相与所有输入事件结果，如果全部为真，返回真
            if (Object.values(events_input).every(value => value === true)) {{
                for (const key in current_values) {{
                    const value = current_values[key];
                    // 如果值是数组，找出冲突项
                    if (Array.isArray(value)) {{
                        const conflictingItems = value.filter(item => rule.{keys[1]}.includes(item));
                        if (conflictingItems.length > 0) {{
                            conflict_items.push(conflictingItems.join(', '));
                        }}
                    }} else {{
                        conflict_items.push(value);
                    }}
                }}
                form_event_action(rule.form_event_action, conflict_items)
            }}
        }};'''
        template_script_call_detect_event_0 = f'''
                    // 检测是否发生符合特定规则的表单事件
                    content_conflict_rules.find(item => {{
                        if (item.{keys[0]}.includes(current_values.{keys[0]})) {{
                            detect_form_event(item);
                        }}
                    }});'''
        template_script_call_detect_event_1 = f'''
                    // 检测是否发生符合特定规则的表单事件
                    content_conflict_rules.find(item => {{
                        if (item.{keys[1]}.includes(current_values.{keys[1]})) {{
                            detect_form_event(item);
                        }}
                    }});'''
    else:
        template_script_detect_event = ''
        template_script_call_detect_event_0 = ''
        template_script_call_detect_event_1 = ''

    template_script_body = f'''
        {template_script_detect_event}
        {template_script_show_icpc_hint}
        {template_script_autofill_fields}

        // 创建观察器，接受一个回调函数为参数
        function createObserver(callback) {{
            return new MutationObserver(function(mutationsList, observer) {{
                for (let mutation of mutationsList) {{
                    if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {{
                        callback(mutation.target);
                    }}
                }}
            }});
        }}
        const mutationObserverConfig = {{ childList: true, subtree: true }}

        // 定义全局变量，用于存储被跟踪的字段当前值
        const current_values = {{
            {keys[0]}: null,
            {keys[1]}: null
        }}

        // {keys[0]}变化处理
        function {keys[0]}HandleChanges(node) {{
            if (node.hasAttribute('title')) {{
                const title = node.getAttribute('title').trim();
                if (title !== current_values.{keys[0]}) {{
                    current_values.{keys[0]} = title;
                    document.querySelector('input[name="_save"]').disabled = false;
                    {template_script_call_detect_event_0}
                    {template_script_call_show_icpc_hint}
                }}
            }}
        }}

        // 为{keys[0]} <select>元素添加事件监听器
        const {keys[0]} = document.querySelector('.form-row.field-{keys[0]} .related-widget-wrapper span.select2-selection__rendered');
        const observer_{keys[0]} = createObserver({keys[0]}HandleChanges);
        observer_{keys[0]}.observe({keys[0]}, mutationObserverConfig)

        // {keys[1]}变化处理
        function {keys[1]}HandleChanges(node) {{
            if (node.hasAttribute('title')) {{
                const title = node.getAttribute('title').trim();
                if (title !== current_values.{keys[1]}) {{
                    current_values.{keys[1]} = title;
                    document.querySelector('input[name="_save"]').disabled = false;
                    {template_script_call_detect_event_1}
                    {template_script_call_autofill_fields}
                }}
            }}
        }}

        // 先为已存在的第一个{keys[1]} <select>元素添加事件监听器
        const existingSpanElement = document.querySelector('.form-row.dynamic-{class_name}_list_set .related-widget-wrapper span.select2-selection__rendered');
        const observer_{keys[1]} = createObserver({keys[1]}HandleChanges);
        observer_{keys[1]}.observe(existingSpanElement, mutationObserverConfig);

        // 需要观察的目标节点
        const targetNode = document.querySelector('#{class_name}_form tbody');

        // 当观察到变动时执行的回调函数
        const trNodeCallback = function(mutationsList, observer) {{
            for(let mutation of mutationsList) {{
                // 检查是否有新节点被添加到DOM中
                if(mutation.type === 'childList') {{
                    // 获得新的<tr>节点
                    var addedNodes = mutation.addedNodes;
                    for(let i = 0; i < addedNodes.length; i++) {{
                        // 判断节点类型是不是元素节点，且节点名字是不是'tr'
                        if(addedNodes[i].nodeType === 1 && addedNodes[i].nodeName === 'TR') {{
                            var trNode = addedNodes[i];
                            // 找到包含{keys[1]}名称的节点
                            var yaoPinMingNode = trNode.querySelector('span.select2-selection__rendered');
                            if(yaoPinMingNode) {{
                                // 为新tr创建观察器
                                observer_{keys[1]}.observe(yaoPinMingNode, mutationObserverConfig);
                            }} else {{
                                console.log('No select node in new TR node');
                            }}
                        }}
                    }}
                }}
            }}
        }};

        // 创建一个观察器实例并传入回调函数
        const tableObserver = new MutationObserver(trNodeCallback);

        // 以上述配置开始观察目标节点
        tableObserver.observe(targetNode, mutationObserverConfig);

    }});
</script>
'''
    return template_script_header + template_script_body