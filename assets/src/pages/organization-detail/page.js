import 'bootstrap/dist/css/bootstrap.min.css';
import Vue from 'vue';
import VueResource from 'vue-resource';
import VueRouter from 'vue-router';

import { ScaleLoader } from 'vue-spinner/dist/vue-spinner.min.js';

import OrganizationService from '../../services/organization';

Vue.use(VueResource);
Vue.use(VueRouter);

var router = new VueRouter({
  mode: 'history',
  routes: []
});

var app = new Vue({
  router,
  el: '#organization-detail',
  components: {
    ScaleLoader,
  },
  filters: {
  },
  created() {
    this.service = new OrganizationService(this.$http);
    this.organization_id = this.$route.query.id;
    if(this.organization_id){
      this.getOrganization();
    }else{
      this.error = 'Organization ID not found';
    }
  },
  data: {
    loading: false,
    error: null,
    organization_id: null,
    fields: [],
    title: null,
  },
  methods: {
    getOrganization(){
      this.error = null;
      this.loading = true;
      this.service.detail(this.organization_id).then(
        response => {
          let organization = response.data.data;
          let fields_conf = response.data.fields;

          this.title = organization.name;
          this.fields = [];
          for(let field of fields_conf){
            this.fields.push({
              name: field.name,
              value: organization[field.key]
            });
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

  },
});

export default app;
