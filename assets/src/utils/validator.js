import Validate from 'validate.js';
import { isNumeric } from './numbers';

const isValidLatLng = (value) => {
  if(!isNumeric(value)){
    return false;
  }
  value = parseFloat(value);
  if(value < -90 || value > 90){
    return false;
  }
  return true;
};

Validate.validators.customLatLng = (value, options, key, attributes) => {
  let {lat, lng} = value;
  let required = options.required === true;
  if(lat === '' && lng === '' && !required){
    return;
  }

  if(lat === ''){
    return `fill: Latitude`;
  }
  if(lng === ''){
    return `fill: Longitude`;
  }

  if(!isValidLatLng(lat)){
    return `Latitude is invalid`;
  }
  if(!isValidLatLng(lng)){
    return `Longitude is invalid`;
  }
};

export default Validate;
