import React, { Component, PropTypes } from 'react'
import ReactDOM from 'react-dom'

export default class Filter extends Component {
  constructor(props) {
    super(props)
    this.onChangeLocal = this.onChangeLocal.bind(this)
  }

  onChangeLocal() {
    let filter = {
      category_id: ReactDOM.findDOMNode(this.refs.categorySelect).value,
      gender: ReactDOM.findDOMNode(this.refs.genderSelect).value,
      q: ReactDOM.findDOMNode(this.refs.queryInput).value
    }
    const { onChange } = this.props
    onChange(filter);
  }

  render() {
    return (
      <div className="filters">
        <div className="filter">
          <input onChange={this.onChangeLocal} ref="queryInput"/>
        </div>
        <div className="filter">
          <select onChange={this.onChangeLocal} ref="categorySelect">
            <option value="" key="">-----------</option>
            {this.props.categories.map(category => {
              return (
                <option value={category.id} key={category.id}>{category.name}</option>
              )
            })}
          </select>
        </div>
        <div className="filter">
          <select onChange={this.onChangeLocal} ref="genderSelect">
            <option value="">-----------</option>
            <option value="male">Мужские</option>
            <option value="female">Женские</option>
          </select>
        </div>
      </div>
    )
  }
}

Filter.propTypes = {
  onChange: PropTypes.func.isRequired
}
