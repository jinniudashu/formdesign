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
def generate_form_event_js_script(rules):
    import json

    template_script_header = '''
<script src="https://cdn.jsdelivr.net/npm/js-cookie@3.0.1/dist/js.cookie.min.js"></script>    
<script>
    document.addEventListener('DOMContentLoaded', async function() {
        // 表单事件规则配置列表
        const content_conflict_rules = '''
    
    rules_string = json.dumps(rules, ensure_ascii=False)

    template_script_get_context = '''
        // 根据表单检测范围，从CustomerServiceLog获取历史记录，构造boolfield_ji_bing_ming_cheng数组上下文
        const customerId = Cookies.get('customer_id');
        const period = 'ALL';  // 'ALL' or 'LAST_WEEK_SERVICES'
        const form_class = 0;  // 指定表单类别
        const fetchCustomerServiceLog = async (customerId, period=null, form_class=0) => {
            let url = `http://127.0.0.1:8000/core/api/customer_service_log/?customer=${customerId}`;
            if (period !== null) {
                url += `&period=${period}`;
            }
            if (form_class > 0) {
                url += `&form_class=${form_class}`;
            }    
            try {
                const response = await fetch(url, {
                    headers: {
                        'Accept': 'application/json',
                    }
                });
                if (!response.ok) {
                    throw new Error('HTTP error ' + response.status);
                }
                const result = await response.json();
                // 将获取的boolfield_ji_bing_ming_cheng历史记录保存在数组中返回
                const logs = JSON.parse(result);
                arrayValue = logs.filter(log => log.fields.data.hasOwnProperty('boolfield_ji_bing_ming_cheng'))
                    .map(log => {
                        s = log.fields.data.boolfield_ji_bing_ming_cheng;
                        v = s.replace("{", "").replace("}", "").replace(/'/g, "")
                        return {value: v, datetime: log.fields.created_time};
                    });
                return arrayValue;
            } catch (error) {
                console.error('Error:', error);
            }
        }
        const context_boolfield_ji_bing_ming_cheng = await fetchCustomerServiceLog(customerId, period, form_class);
        console.log(context_boolfield_ji_bing_ming_cheng);
    '''    

    template_script_body = '''

        // 定义全局变量，用于存储被跟踪的字段当前值
        const current_values = {
            boolfield_ji_bing_ming_cheng: null,
            boolfield_yao_pin_ming: null
        }

        // 定义表单事件动作，接受一个选项，来自表单事件规则列表
        const form_event_action = (action, conflict_items) => {
            // 把冲突项目数组转换为字符串
            const conflict_items_string = conflict_items.join('、');
            if (action === 'WARN') {
                // 警告用户内容冲突
                alert(`表单内容冲突：${conflict_items_string}`);
            } else if (action === 'PROHIBIT') {
                alert(`表单内容冲突：${conflict_items_string}`);
                // 禁止保存表单
                document.querySelector('input[name="_save"]').disabled = true;
            }
        }

        // 检测是否发生符合特定规则的表单事件. 接受一条来自表单事件规则列表的规则, 如果发生表单事件，执行规则配置表中指定的表单事件动作
        const detect_form_event = (rule) => {
            if (!current_values.boolfield_yao_pin_ming) return;

            // 构造冲突项列表
            const conflict_items = [];

            const events_context = {
                event_0 : context_boolfield_ji_bing_ming_cheng.filter(item => rule.boolfield_ji_bing_ming_cheng.includes(item.value)).length > 0,
                event_1 : current_values.boolfield_yao_pin_ming.filter(item => rule.boolfield_yao_pin_ming.includes(item)).length > 0,
            }
            // 检测是否发生上下文冲突
            if (Object.values(events_context).every(value => value === true)) {
                // 对于上下文冲突，添加产生冲突的具体疾病名称
                if (events_context.event_0) {
                    const conflictingDiseases = context_boolfield_ji_bing_ming_cheng.filter(item => rule.boolfield_ji_bing_ming_cheng.includes(item.value)).map(item => item.value);
                    if (conflictingDiseases.length > 0) {
                        conflict_items.push(conflictingDiseases.join(', '));
                    }
                }
                form_event_action(rule.form_event_action, conflict_items)
            }

            const events_input = {
                event_0 : new Set(rule.boolfield_ji_bing_ming_cheng).has(current_values.boolfield_ji_bing_ming_cheng),
                event_1 : current_values.boolfield_yao_pin_ming.filter(item => rule.boolfield_yao_pin_ming.includes(item)).length > 0,
            }
            // 相与所有输入事件结果，如果全部为真，返回真
            if (Object.values(events_input).every(value => value === true)) {
                for (const key in current_values) {
                    const value = current_values[key];
                    // 如果值是数组，找出冲突项
                    if (Array.isArray(value)) {
                        const conflictingItems = value.filter(item => rule.boolfield_yao_pin_ming.includes(item));
                        if (conflictingItems.length > 0) {
                            conflict_items.push(conflictingItems.join(', '));
                        }
                    } else {
                        conflict_items.push(value);
                    }
                }
                form_event_action(rule.form_event_action, conflict_items)
            }
        };

        // 选择字段对应的dom元素，django admin 自动补全单选下拉框，创建一个新的MutationObserver实例，监听变化。
        const boolfield_ji_bing_ming_cheng = document.querySelector('.form-row.field-boolfield_ji_bing_ming_cheng .related-widget-wrapper');
        // Create a new MutationObserver instance
        const observer_boolfield_ji_bing_ming_cheng = new MutationObserver(function(mutationsList, observer) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const spanElement = boolfield_ji_bing_ming_cheng.querySelector('span.select2-selection__rendered');
                    if (spanElement.hasAttribute('title')) {
                        const title = spanElement.getAttribute('title').trim();
                        // 检查字段内容是否发生变化
                        if (title !== current_values.boolfield_ji_bing_ming_cheng) {
                            current_values.boolfield_ji_bing_ming_cheng = title;
                            // 检查保存按钮是否被禁用，如果是，启用
                            document.querySelector('input[name="_save"]').disabled = false;
                            // 如果疾病名称在规则列表中，检查表单事件
                            content_conflict_rules.find(item => {
                                if (item.boolfield_ji_bing_ming_cheng.includes(current_values.boolfield_ji_bing_ming_cheng)) {
                                    detect_form_event(item);
                                }
                            });
                        }
                    }            
                }
            }
        });
        observer_boolfield_ji_bing_ming_cheng.observe(boolfield_ji_bing_ming_cheng, { childList: true, subtree: true });

        // 选择字段对应的dom元素，django admin 自动补全多选下拉框，创建一个新的MutationObserver实例，监听变化。
        const boolfield_yao_pin_ming = document.querySelector('.form-row.field-boolfield_yao_pin_ming .related-widget-wrapper');
        // Create a new MutationObserver instance
        const observer_boolfield_yao_pin_ming = new MutationObserver(function(mutationsList, observer) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const spanElement = boolfield_yao_pin_ming.querySelector('ul.select2-selection__rendered');
                    const liElements = spanElement.querySelectorAll('li.select2-selection__choice');
                    const titleArray = Array.from(liElements, li => li.getAttribute('title').trim());
                    // 检查字段内容是否发生变化
                    if (JSON.stringify(titleArray) !== JSON.stringify(current_values.boolfield_yao_pin_ming)) {
                        current_values.boolfield_yao_pin_ming = titleArray;
                        // 检查保存按钮是否被禁用，如果是，启用
                        document.querySelector('input[name="_save"]').disabled = false;
                        // 如果药品名称在规则列表中，检查表单事件
                        content_conflict_rules.find(item => {
                            if (item.boolfield_yao_pin_ming.filter(item => current_values.boolfield_yao_pin_ming.includes(item)).length > 0) {
                                detect_form_event(item);
                            }
                        });
                    }
                }
            }
        });
        observer_boolfield_yao_pin_ming.observe(boolfield_yao_pin_ming, { childList: true, subtree: true });
    });
</script>
'''
    return template_script_header + rules_string + template_script_get_context + template_script_body