import 'bootstrap/dist/css/bootstrap.min.css';
import Vue from 'vue';
import VueResource from 'vue-resource';
import VueRouter from 'vue-router';

import Datepicker from 'vuejs-datepicker';
import { ScaleLoader } from 'vue-spinner/dist/vue-spinner.min.js';

import OrganizationService from '../../services/organization';
import Validate from '../../utils/validator';
import { ORGANIZATION_DETAIL } from '../../utils/urls';

Vue.use(VueResource);
Vue.use(VueRouter);

var router = new VueRouter({
  mode: 'history',
  routes: []
});

var app = new Vue({
  router,
  el: '#organization-create',
  components: {
    Datepicker,
    ScaleLoader
  },
  filters: {
  },
  created() {
    this.service = new OrganizationService(this.$http);
    this.loadFields();
  },
  data: {
    loading: false,
    error: null,
    formValidator: {},
    service: null,
    fields: [],
    fieldsMap: {},
    title: 'Add Organization',
    newField: { name: '', type: '-' },
    newFieldValidator: {
      name: { exclusion: { within: [''], message: 'is required.' } },
      type: { exclusion: { within: ['-'], message: 'is required.' } },
    }
  },
  methods: {
    loadFields(){
      this.error = null;
      this.loading = true;
      this.service.fields().then(
        response => {
          for (let field of response.data){
            this.addField(field);
          }
          this.loading = false;
        },
        response_error => {
          if(response_error.status === 400){
            this.error = response_error.body.error;
          } else {
            this.error = 'Something went wrong, try againg in few seconds';
          }
          this.loading = false;
        }
      );
    },
    addField(field){
      if (!field.add_visible_flag || !this.isSupportedInput(field.field_type)){
        return;
      }

      field.value = '';
      if(this.isAddressInput(field.field_type)){
        field.value = {lat: '', lng: ''};
      }
      field.errors = [];
      this.fields.push(field);
      this.fieldsMap[field.name.toLowerCase()] = field;
      this.setValidator(field);
    },

    setValidator(field){
      if(this.isAddressInput(field.field_type)){
        this.formValidator[field.key] = {
          customLatLng: true,
        };
      }
      if(field.mandatory_flag){
        this.formValidator[field.key] = {
          presence: { message: 'is required.' }
        };
      }
    },

    fieldExists(name){
      let field = this.fieldsMap[name.toLowerCase()] || {};
      return Object.keys(field).length > 0;
    },

    setErrors(errorsMap){
      for(let [name, errors] of Object.entries(errorsMap)){
        let field = this.fieldsMap[name.toLocaleLowerCase()];
        field.errors = field.errors.concat(errors);
      }
    },

    submit(){
      let data = {};
      let field_type = {};
      for (let field of this.fields){
        field.errors = [];
        if(field.value){
          data[field.key] = field.value;
          field_type[field.key] = field.field_type;
        }
      }
      let errors = Validate(data, this.formValidator);
      if(Object.keys(errors || {}).length > 0){
        this.setErrors(errors);
        window.scrollTo(0, 0);
        return;
      }

      this.loading = true;
      this.service.create({data, field_type}).then(
        response => {
          let organization_id = response.data.id;
          window.location.href = (
            `${ORGANIZATION_DETAIL}/?id=${organization_id}`
          );
        },
        response_error => {
          if(response_error.status === 400){
            this.error = response_error.body.error;
          } else {
            this.error = 'Something went wrong, try againg in few seconds';
          }
          this.loading = false;
          window.scrollTo(0, 0);
        }
      );

    },

    isSupportedInput(field_type){
      let supported_types = [
        'varchar', 'varchar_auto', 'phone', 'text', 'date', 'address'
      ];
      return supported_types.indexOf(field_type) >= 0;
    },

    isAddressInput(field_type){
      return field_type == 'address';
    },

    isTextInput(field_type){
      return [
        'varchar', 'varchar_auto', 'phone',
      ].indexOf(field_type) >= 0;
    },

    isTextAreaInput(field_type){
      return field_type == 'text';
    },

    isDatePickerInput(field_type){
      return field_type == 'date';
    },

    isNewFieldValid(){
      let errors = Validate(this.newField, this.newFieldValidator);
      if(Object.keys(errors || {}).length > 0){
        return false;
      }

      let name = this.newField.name;
      if(this.fieldExists(name)){
        return false;
      }

      return true;
    },

    addNewField(){
      if(!this.isNewFieldValid()){
        return;
      }
      let field = {
        key: this.newField.name,
        name: this.newField.name,
        field_type: this.newField.type,
        add_visible_flag: true,
      };
      this.addField(field);
      this.newField = { name: '', type: '-' };
    },

  },
});

export default app;
