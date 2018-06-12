import 'bootstrap/dist/css/bootstrap.min.css';
import Vue from 'vue';
import VueResource from 'vue-resource';
import VueRouter from 'vue-router';
import OrganizationService from '../../services/organization';

import { ScaleLoader } from 'vue-spinner/dist/vue-spinner.min.js';
import debounce from 'debounce';

Vue.use(VueResource);
Vue.use(VueRouter);

var router = new VueRouter({
  mode: 'history',
  routes: []
});

var app = new Vue({
  router,
  el: '#search',
  components: {
    ScaleLoader,
  },
  filters: {
  },
  created() {
    this.service = new OrganizationService(this.$http);
    this.searchInput = debounce(this.searchInput, 500);
    this.searchString = this.$route.query.search;
    this.search();
  },
  data: {
    loading: false,
    error: null,
    service: null,
    organizations: [],
    searchString: '',
    organization_page: '/dist/build/organization'
  },
  methods: {
    searchInput(element) {
      this.searchString = element.target.value;
      this.search();
    },

    search(){
      this.$router.push({ query: { search: this.searchString }});
      this.error = null;
      this.loading = true;
      this.service.search(this.searchString || '').then(
        response => {
          this.organizations = response.data;
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
    }

  },
});

export default app;
