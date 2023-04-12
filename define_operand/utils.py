########################################################################################################################
# Generate JS script 
########################################################################################################################
def generate_js_script(prompt):
    import openai
    from formdesign.settings import OPENAI_API_KEY

    openai.api_key = OPENAI_API_KEY

    SYSTEM_PROMPT = 'You are a seasoned Javascript developer.'

    USER_INPUT_PREFIX = '''Please write concise JS code to automatically update computed fields on a web page form. The form definition and computation logic are specified in their respective sections. Computed field values are obtained by calculating values from other fields in the form using the computation logic. Follow this naming convention: the field name prefixed with "id_" is the field ID.
    Use the 'document.addEventListener' method to listen for the DOMContentLoaded event and execute a callback function when the page is loaded. The callback function should follow these steps:
    1. Use document.getElementById to retrieve the DOM elements of all fields involved in the computation logic.
    2. Write a calculation function to implementing the business logic based on the computation logic description.
    3. Implement a function to update the DOM element of the computed field. Retrieve the values of relevant fields, call the calculation function from step 2, and assign the calculation result to the DOM element of the computed field.
    4. Add an input event listener to the DOM elements of related fields involved in the computation logic, except for the computed field itself, so that the update calculation function from step 3 is called when the user inputs values.
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

    prompt = USER_INPUT_PREFIX + prompt
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": EXAMPLE_USER_INPUT},
            {"role": "assistant", "content": EXAMPLE_ASSISTANT_RESPONSE},
            {"role": "user", "content": prompt}
        ]
    )
    result = response['choices'][0]['message']['content']
    print('prompt:\n', prompt)
    print('result:\n', result)
    print('usage:\n', response['usage'])
    
    return result


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
