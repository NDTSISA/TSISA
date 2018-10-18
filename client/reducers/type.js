const initialState = {
  type: 1,
};

export default function type (state = initialState, action) {
    switch (action.type) {
      case 'GET_TYPE':
        return { ...state, type: action.payload.type };
      default:
        return state;
    }
  }