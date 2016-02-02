import { combineReducers } from 'redux'
import {
  REQUEST_NAMES, RECEIVE_NAMES, RESET_NAMES, RECEIVE_CATEGORIES, TOGGLE_MODAL
} from '../actions'

function modalInfo(state = {
  open: false
}, action) {
  switch (action.type) {
    case TOGGLE_MODAL:
      return Object.assign({}, state, {
        open: !state.open
      })
    default:
      return state
  }
}

function listNames(state = {
  isFetching: false,
  filter: {},
  total: null,
  items: [],
  page: 1
}, action) {

  switch (action.type) {
    case REQUEST_NAMES:
      return Object.assign({}, state, {
        isFetching: true
      })
    case RECEIVE_NAMES:
      let items = state.items.concat(action.names);
      return Object.assign({}, state, {
        isFetching: false,
        filter: action.filter,
        total: action.total,
        items: items,
        page: action.page
      })
    case RESET_NAMES:
      return Object.assign({}, state, {
        items: []
      })
    default:
      return state
  }
}

function listCategories(state = {
  items: []
}, action) {

  switch (action.type) {
    case RECEIVE_CATEGORIES:
      return Object.assign({}, state, {
        items: action.categories
      })
    default:
      return state
  }
}

const rootReducer = combineReducers({
  modalInfo,
  listNames,
  listCategories
})

export default rootReducer
