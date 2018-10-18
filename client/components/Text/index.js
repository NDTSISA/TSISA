import React, { Component } from 'react';
import './styles.scss';
import data from './text.json';
import $ from "jquery";
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as cursorActions from '../../actions/CursorActions';
import * as typeActions from '../../actions/TypeActions';
import PropTypes from 'prop-types';

class Text extends Component {
  constructor (props) {
    super(props);
    this.state = { scrollPosition: 0 };
  }

  componentDidMount () {
    $('.text').on('scroll', () => { this.handleScroll(); });

    $('.text').children('p').each((index, element) => {
      this.addParagraph(index, element);
    });

    $('.text').click((e) => { 
      this.handleClick((e.pageY - $('.text').position().top - 50));
    });
  }

  addParagraph (index, element) {
    this.props.cursorActions.addParagraphHeight({ index: index, height: ($(element).height() + 10) });
  }

  handleScroll () {
    this.setState({
      scrollPosition: $('.text').scrollTop()
    });
  }

  handleClick (position) {
    this.props.cursorActions.changeCursor(position + this.state.scrollPosition);
  }

  buttonClick (type) {
    this.props.typeActions.changeType(type);
  }

  render () {
    return (
      <div>
      <div className="text">
        { data.text.map((paragraph, i) => (<p key={i} style={{ marginTop: 10, marginBottom: 10 }}>{paragraph}</p>))}
      </div>
      <div>
        <button onClick={() => this.buttonClick(1)} >LSA</button>
        <button onClick={() => this.buttonClick(2)}>TextTiling</button>
        <button onClick={() => this.buttonClick(3)}>ARTM+TT</button>
      </div>
    </div>
    );
  }
}

Text.propTypes = {
  cursorActions: PropTypes.any,
};

function mapStateToProps (state) {
  return {
    cursor: state.cursor,
  };
}

function mapDispatchToProps (dispatch) {
  return {
    cursorActions: bindActionCreators(cursorActions, dispatch),
    typeActions: bindActionCreators(typeActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Text);
