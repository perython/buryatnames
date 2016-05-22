import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import Modal from 'react-modal'
import { fetchNames, fetchCategories, toggleModal } from '../actions'
import Filter from '../components/Filter'
import Names from '../components/Names'

const modalStyles = {
  content : {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)'
  }
};

const modalText = `

`

class App extends Component {
  constructor(props) {
    super(props)
    this.handleFilterChange = this.handleFilterChange.bind(this)
    this.handleLoadMore = this.handleLoadMore.bind(this)
    this.toggleModal = this.toggleModal.bind(this)
  }

  componentDidMount() {
    const { dispatch, filter, page } = this.props
    dispatch(fetchCategories())
    dispatch(fetchNames(filter, page))
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.filter !== this.props.filter) {
      const { dispatch, filter, page } = nextProps
      dispatch(fetchNames(filter, page))
    }
  }

  handleFilterChange(filter) {
    const { dispatch } = this.props
    dispatch(fetchNames(filter, 1))
  }

  handleLoadMore(e) {
    e.preventDefault()
    const { dispatch, filter, page } = this.props
    dispatch(fetchNames(filter, page))
  }

  toggleModal(e) {
    e.preventDefault()
    const { dispatch } = this.props
    dispatch(toggleModal())
  }

  render() {
    const { filter, total, names, page, isFetching, categories, modalIsOpen } = this.props
    const isMore = !!page
    return (
      <div className="wrapper">
        <header>
          <h1>Имена в Бурятии</h1>
          <div className="about">
            <a href="" onClick={this.toggleModal}>О сайте</a>
            <Modal
              isOpen={modalIsOpen}
              onRequestClose={this.toggleModal}
              className="modal modal-about"
              overlayClassName="modal-overlay"
              style={modalStyles} >
              <h2>О сайте</h2>
              <div className="modal-content">
                <p>Небольшой каталог имен и их значений. Большинство из них в основном популярны в республике Бурятия. Основу для каталога составили данные из группы Буддийские имена (http://vk.com/burnames).</p>
                <p>Бурятские имена - понятие довольно растяжимое. Прежде всего потому, что много имен пришли из других регионов и даже стран. Тибетские (санскритские), монгольские, казахские и др. имена составили костяк того множества, которое весьма популярно в Бурятии.</p>
              </div>
              <button onClick={this.toggleModal} className="modal-close">Закрыть</button>
            </Modal>
          </div>
        </header>
        <Filter categories={categories}
                filter={filter}
                onChange={this.handleFilterChange} />
        {isFetching ? <h2>Загрузка ...</h2>
          : <div className="names" style={{ opacity: isFetching ? 0.5 : 1 }}>
              <div className="names-counter">
                <span class="total-items">{total}</span> имен найдено
              </div>
              <Names names={names} />
            </div>
        }
        <div className="more">
          {!isFetching ?
            <button onClick={this.handleLoadMore} disabled={!isMore}>{isMore ? 'Больше' : 'Больше нет'}</button> : ''
          }
        </div>
      </div>
    )
  }
}

App.propTypes = {
  filter: PropTypes.object.isRequired,
  total: PropTypes.number,
  names: PropTypes.array.isRequired,
  isFetching: PropTypes.bool.isRequired,
  dispatch: PropTypes.func.isRequired,
  page: PropTypes.number,
  categories: PropTypes.array,
  modalIsOpen: PropTypes.bool
}

function mapStateToProps(state) {
  const { listNames, listCategories, modalInfo } = state

  const { isFetching, filter, total, items:names, page } = listNames
  const { items:categories } = listCategories
  const { open:modalIsOpen } = modalInfo

  return {
    filter,
    total,
    names,
    isFetching,
    page,
    categories,
    modalIsOpen
  }
}

export default connect(mapStateToProps)(App)
