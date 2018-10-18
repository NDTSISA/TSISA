import React, { Component } from 'react';
import './styles.scss';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { constants } from './constants.json';

class Lines extends Component {

  getPercentHeight (paragraphs, index) {
    let maxHeight = this.props.cursor.maxPosition;
    let height = (paragraphs[index].height) / (maxHeight / 100) * 5;
    return height;
  }

  render () {
    const { cursor, type } = this.props;

    console.log(constants);

    return (
      <div className="lines">
        <div className="cursor" style={{ top: ((cursor.position / ((cursor.maxPosition) / 100)) * 5) || undefined }} />
          {cursor.paragraphs.map((paragraph, i) => (<div key={i} className="block"
          style={{
            height: this.getPercentHeight(cursor.paragraphs, i),
            backgroundColor: 'rgba(' + (i * 50) + ', 123, 89, 0.2)'
          }}>
            {constants[type][i]}
          </div>))}
      </div>
    );
  }
}

Lines.propTypes = {
  type: PropTypes.any,
  cursor: PropTypes.any,
  maxPosition: PropTypes.any
};

function mapStateToProps (state) {
  return {
    type: state.type.type,
    cursor: state.cursor
  };
}

export default connect(mapStateToProps)(Lines);
