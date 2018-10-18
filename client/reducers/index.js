import { combineReducers } from 'redux';
import cursor from './cursor';
import type from './type';


export default combineReducers({
  cursor,
  type
});
