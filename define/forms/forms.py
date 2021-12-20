from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *

class Allergies_history_baseform_ModelForm(ModelForm):
    class Meta:
        model = Allergies_history
        fields = ['relatedfield_drug_name', ]
        widgets = {'relatedfield_drug_name': CheckboxSelectMultiple, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Out_of_hospital_self_report_survey_baseform_ModelForm(ModelForm):
    class Meta:
        model = Out_of_hospital_self_report_survey
        fields = ['relatedfield_symptom_list', 'characterfield_supplementary_description_of_the_condition', ]
        widgets = {'relatedfield_symptom_list': CheckboxSelectMultiple, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Personal_comprehensive_psychological_quality_survey_baseform_ModelForm(ModelForm):
    class Meta:
        model = Personal_comprehensive_psychological_quality_survey
        fields = ['relatedfield_personality_tendency', 'boolfield_is_life_fun', ]
        widgets = {'relatedfield_personality_tendency': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Personal_adaptability_assessment_baseform_ModelForm(ModelForm):
    class Meta:
        model = Personal_adaptability_assessment
        fields = ['boolfield_do_you_feel_pressured_at_work', 'boolfield_do_you_often_work_overtime', 'characterfield_working_hours_per_day', 'relatedfield_are_you_satisfied_with_the_job_and_life', 'relatedfield_are_you_satisfied_with_your_adaptability', 'relatedfield_can_you_get_encouragement_and_support_from_family_and_friends', ]
        widgets = {'relatedfield_are_you_satisfied_with_the_job_and_life': Select, 'relatedfield_are_you_satisfied_with_your_adaptability': Select, 'relatedfield_can_you_get_encouragement_and_support_from_family_and_friends': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Personal_health_behavior_survey_baseform_ModelForm(ModelForm):
    class Meta:
        model = Personal_health_behavior_survey
        fields = ['boolfield_is_the_diet_regular', 'boolfield_is_the_diet_proportion_healthy', 'boolfield_whether_the_bowel_movements_are_regular', 'boolfield_whether_to_drink_alcohol', 'relatedfield_drinking_frequency', 'boolfield_do_you_smoke', 'relatedfield_smoking_frequency', 'characterfield_average_sleep_duration', 'boolfield_insomnia', 'characterfield_duration_of_insomnia', ]
        widgets = {'relatedfield_drinking_frequency': RadioSelect, 'relatedfield_smoking_frequency': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Personal_health_assessment_baseform_ModelForm(ModelForm):
    class Meta:
        model = Personal_health_assessment
        fields = ['relatedfield_own_health', 'relatedfield_compared_to_last_year', 'relatedfield_sports_preference', 'relatedfield_exercise_time', 'boolfield_is_it_easy_to_get_sick', 'relatedfield_have_any_recent_symptoms_of_physical_discomfort', ]
        widgets = {'relatedfield_own_health': RadioSelect, 'relatedfield_compared_to_last_year': Select, 'relatedfield_sports_preference': Select, 'relatedfield_exercise_time': RadioSelect, 'relatedfield_have_any_recent_symptoms_of_physical_discomfort': CheckboxSelectMultiple, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Social_environment_assessment_baseform_ModelForm(ModelForm):
    class Meta:
        model = Social_environment_assessment
        fields = ['relatedfield_is_the_living_environment_satisfactory', 'relatedfield_is_the_transportation_convenient', 'boolfield_whether_the_living_environment_is_clean_and_hygienic', 'boolfield_is_drinking_water_healthy?', 'boolfield_whether_there_is_noise_pollution', 'boolfield_whether_there_is_air_pollution', 'boolfield_whether_there_is_other_pollution', ]
        widgets = {'relatedfield_is_the_living_environment_satisfactory': Select, 'relatedfield_is_the_transportation_convenient': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Vital_signs_check_baseform_ModelForm(ModelForm):
    class Meta:
        model = Vital_signs_check
        fields = ['numberfield_body_temperature', 'numberfield_pulse', 'numberfield_respiratory_rate', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Family_history_of_illness_baseform_ModelForm(ModelForm):
    class Meta:
        model = Family_history_of_illness
        fields = ['relatedfield_diseases', 'relatedfield_family_relationship', ]
        widgets = {'relatedfield_diseases': Select, 'relatedfield_family_relationship': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Physical_examination_baseform_ModelForm(ModelForm):
    class Meta:
        model = Physical_examination
        fields = ['numberfield_hight', 'numberfield_weight', 'numberfield_body_mass_index', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class History_of_blood_transfusion_baseform_ModelForm(ModelForm):
    class Meta:
        model = History_of_blood_transfusion
        fields = ['datetimefield_date', 'numberfield_blood_transfusion', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class History_of_trauma_baseform_ModelForm(ModelForm):
    class Meta:
        model = History_of_trauma
        fields = ['datetimefield_date', 'relatedfield_diseases_name', ]
        widgets = {'relatedfield_diseases_name': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Fundus_examination_baseform_ModelForm(ModelForm):
    class Meta:
        model = Fundus_examination
        fields = ['relatedfield_fundus', ]
        widgets = {'relatedfield_fundus': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Medical_history_baseform_ModelForm(ModelForm):
    class Meta:
        model = Medical_history
        fields = ['relatedfield_disease_name', 'datetimefield_time_of_diagnosis', ]
        widgets = {'relatedfield_disease_name': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Doctor_registry_baseform_ModelForm(ModelForm):
    class Meta:
        model = Doctor_registry
        fields = ['characterfield_name', 'characterfield_gender', 'characterfield_age', 'characterfield_identification_number', 'characterfield_contact_information', 'characterfield_contact_address', 'relatedfield_service_role', 'characterfield_practice_qualification', 'characterfield_password_setting', 'characterfield_confirm_password', 'characterfield_expertise', 'characterfield_practice_time', 'relatedfield_affiliation', 'datetimefield_date_of_birth', ]
        widgets = {'relatedfield_service_role': CheckboxSelectMultiple, 'relatedfield_affiliation': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class User_login_baseform_ModelForm(ModelForm):
    class Meta:
        model = User_login
        fields = ['characterfield_username', 'characterfield_password', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Doctor_login_baseform_ModelForm(ModelForm):
    class Meta:
        model = Doctor_login
        fields = ['characterfield_username', 'characterfield_password', 'characterfield_service_role', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Dorsal_artery_pulsation_examination_baseform_ModelForm(ModelForm):
    class Meta:
        model = Dorsal_artery_pulsation_examination
        fields = ['relatedfield_left_foot', 'relatedfield_right_foot', ]
        widgets = {'relatedfield_left_foot': RadioSelect, 'relatedfield_right_foot': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Physical_examination_hearing_baseform_ModelForm(ModelForm):
    class Meta:
        model = Physical_examination_hearing
        fields = ['relatedfield_left_ear_hearing', 'relatedfield_right_ear_hearing', ]
        widgets = {'relatedfield_left_ear_hearing': Select, 'relatedfield_right_ear_hearing': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class History_of_infectious_diseases_baseform_ModelForm(ModelForm):
    class Meta:
        model = History_of_infectious_diseases
        fields = ['relatedfield_diseases', 'relatedfield_family_relationship', ]
        widgets = {'relatedfield_diseases': Select, 'relatedfield_family_relationship': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class History_of_surgery_baseform_ModelForm(ModelForm):
    class Meta:
        model = History_of_surgery
        fields = ['datetimefield_date', 'relatedfield_name_of_operation', ]
        widgets = {'relatedfield_name_of_operation': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Physical_examination_oral_cavity_baseform_ModelForm(ModelForm):
    class Meta:
        model = Physical_examination_oral_cavity
        fields = ['relatedfield_lips', 'relatedfield_dentition', 'relatedfield_pharynx', ]
        widgets = {'relatedfield_lips': RadioSelect, 'relatedfield_dentition': RadioSelect, 'relatedfield_pharynx': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Blood_pressure_monitoring_baseform_ModelForm(ModelForm):
    class Meta:
        model = Blood_pressure_monitoring
        fields = ['numberfield_systolic_blood_pressure', 'numberfield_diastolic_blood_pressure', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Major_life_events_baseform_ModelForm(ModelForm):
    class Meta:
        model = Major_life_events
        fields = ['datetimefield_date', 'relatedfield_major_life', ]
        widgets = {'relatedfield_major_life': CheckboxSelectMultiple, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Physical_examination_vision_baseform_ModelForm(ModelForm):
    class Meta:
        model = Physical_examination_vision
        fields = ['characterfield_left_eye_vision', 'characterfield_right_eye_vision', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Lower_extremity_edema_examination_baseform_ModelForm(ModelForm):
    class Meta:
        model = Lower_extremity_edema_examination
        fields = ['relatedfield_lower_extremity_edema', ]
        widgets = {'relatedfield_lower_extremity_edema': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Basic_personal_information_baseform_ModelForm(ModelForm):
    class Meta:
        model = Basic_personal_information
        fields = ['relatedfield_family_relationship', 'characterfield_name', 'characterfield_identification_number', 'datetimefield_date_of_birth', 'relatedfield_family_id', 'characterfield_resident_file_number', 'relatedfield_gender', 'relatedfield_nationality', 'relatedfield_marital_status', 'relatedfield_education', 'relatedfield_occupational_status', 'characterfield_family_address', 'characterfield_contact_number', 'characterfield_medical_ic_card_number', 'relatedfield_medical_expenses_burden', 'relatedfield_type_of_residence', 'relatedfield_blood_type', 'boolfield_contract_signatory', 'relatedfield_signed_family_doctor', ]
        widgets = {'relatedfield_family_relationship': Select, 'relatedfield_family_id': Select, 'relatedfield_gender': Select, 'relatedfield_nationality': Select, 'relatedfield_marital_status': Select, 'relatedfield_education': Select, 'relatedfield_occupational_status': Select, 'relatedfield_medical_expenses_burden': CheckboxSelectMultiple, 'relatedfield_type_of_residence': Select, 'relatedfield_blood_type': Select, 'relatedfield_signed_family_doctor': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Physical_examination_athletic_ability_baseform_ModelForm(ModelForm):
    class Meta:
        model = Physical_examination_athletic_ability
        fields = ['relatedfield_athletic_ability', ]
        widgets = {'relatedfield_athletic_ability': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class User_registry_baseform_ModelForm(ModelForm):
    class Meta:
        model = User_registry
        fields = ['characterfield_name', 'characterfield_gender', 'characterfield_age', 'characterfield_identification_number', 'characterfield_contact_information', 'characterfield_contact_address', 'characterfield_password_setting', 'characterfield_confirm_password', 'datetimefield_date_of_birth', ]
        
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug
