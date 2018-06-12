let API_PREFIX = '/api';

class Service {

  constructor($http) {
    this.$http = $http;
  }

  url(endponint){
    return `${API_PREFIX}${endponint}`;
  }

  all(){
    let url = this.url('/organizations');
    return this.$http.get(url).then(response => response.data);
  }

  search(search){
    let url = this.url(`/organizations?search=${search}`);
    return this.$http.get(url).then(response => response.data);
  }

  fields(){
    let url = this.url('/organizations-fields');
    return this.$http.get(url).then(response => response.data);
  }

  create(data){
    let url = this.url('/organizations');
    return this.$http.post(url, data).then(response => response.data);
  }

  detail(organization_id){
    let url = this.url(`/organizations/${organization_id}`);
    return this.$http.get(url).then(response => response.data);
  }
}

export default Service;
