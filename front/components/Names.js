import React, { PropTypes, Component } from 'react'

export default class Names extends Component {
  render() {
    return (
      <div className="names-container">
        {this.props.names.map((name, i) =>
          <div className="name" key={i}>
            <h3>{name.title}</h3>
            <p>{name.desc}</p>
          </div>
        )}
      </div>
    )
  }
}

Names.propTypes = {
  names: PropTypes.array.isRequired
}
