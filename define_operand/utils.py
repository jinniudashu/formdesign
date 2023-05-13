########################################################################################################################
# Generate JS script 
########################################################################################################################
def generate_js_script(params):
    import openai
    from formdesign.settings import OPENAI_API_KEY

    openai.api_key = OPENAI_API_KEY

    messages=[]
    # prompt = {'form_events': form_events, 'computed_fields': ''}  # 提示信息清单
    # 根据prompt调用不同的提示生成脚本
    if params.get('form_events'):
        messages = generate_form_assistance_prompt(params.get('form_events'))
        return messages
    elif params.get('computed_fields'):
        messages = generate_computed_fields_prompt(params.get('computed_fields'))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages
    )
    result = response['choices'][0]['message']['content']
    print('usage:\n', response['usage'])
    
    return result


def generate_form_assistance_prompt(param):
    return f"hi, your script is generated here ...{param}"


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
