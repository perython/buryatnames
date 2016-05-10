import fetch from 'isomorphic-fetch'

const HOST_API = process.env.NODE_ENV === 'production' ? 'http://buryatnames.com' : 'http://localhost:5000'

export const REQUEST_NAMES = 'REQUEST_NAMES'
export const RECEIVE_NAMES = 'RECEIVE_NAMES'
export const RESET_NAMES = 'RESET_NAMES'
export const RECEIVE_CATEGORIES = 'RECEIVE_CATEGORIES'
export const NOTHING_HAPPENS = 'NOTHING_HAPPENS'
export const TOGGLE_MODAL = 'TOGGLE_MODAL'

export function toggleModal() {
  return {
    type: TOGGLE_MODAL
  }
}

function nothingHappens() {
  return {
    type: NOTHING_HAPPENS
  }
}

function resetNames() {
  return {
    type: RESET_NAMES
  }
}

function requestNames() {
  return {
    type: REQUEST_NAMES
  }
}

function receiveNames(filter, json) {
  return {
    type: RECEIVE_NAMES,
    filter: filter,
    total: json.total,
    names: json.items,
    page: json.page
  }
}

export function fetchNames(filter, page) {
  if (!page) {
    return dispatch(nothingHappens())
  }
  return dispatch => {
    if (page === 1) {
      dispatch(resetNames())
      dispatch(requestNames())
    }

    let options = Object.assign({}, {page: page}, filter);
    let optionsStr = '';
    for (var key in options) {
      if (optionsStr != '') {
          optionsStr += '&';
      }
      optionsStr += `${key}=${encodeURIComponent(options[key])}`;
    }

    return fetch(`${HOST_API}/api/names?${optionsStr}`)
      .then(response => response.json())
      .then(json => dispatch(receiveNames(filter, json)))
  }
}

function receiveCategories(json) {
  return {
    type: RECEIVE_CATEGORIES,
    categories: json
  }
}

export function fetchCategories() {
  return dispatch => {
    return fetch(`${HOST_API}/api/names/categories`)
      .then(response => response.json())
      .then(json => dispatch(receiveCategories(json)))
  }
}