export function changeType (newType) {
    return function (dispatch) {
      dispatch({
        type: 'GET_TYPE',
        payload: { type: newType }
      });
    };
  }
