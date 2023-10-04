import { AssetActionTypes, ADD_ASSET, DELETE_ASSET, Asset } from './assetsActions';

// Define the shape of the asset state
interface AssetState {
  assets: Asset[];
}

// Define the initial state
const initialState: AssetState = {
  assets: [],
};

// Define the asset reducer
const assetReducer = (state = initialState, action: AssetActionTypes): AssetState => {
  switch (action.type) {
    case ADD_ASSET:
      return {
        ...state,
        assets: [...state.assets, action.payload],
      };
    case DELETE_ASSET:
      return {
        ...state,
        assets: state.assets.filter(asset => asset.id !== action.payload),
      };
    default:
      return state;
  }
};

export default assetReducer;
