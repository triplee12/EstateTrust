// Asset type definition
export type Asset = {
  id: string; // Unique identifier for the asset
  name: string; // Name of the asset
  quantity: number; // Quantity of the asset
  yearAcquired: number; // Year the asset was acquired
  beneficiaries: string[]; // List of beneficiaries (assuming their names as strings)
};

// Define action types
export const ADD_ASSET = 'ADD_ASSET';
export const DELETE_ASSET = 'DELETE_ASSET';

// Define action interfaces
interface AddAssetAction {
  type: typeof ADD_ASSET;
  payload: Asset; // Asset is assumed to be a type representing your asset data structure
}

interface DeleteAssetAction {
  type: typeof DELETE_ASSET;
  payload: string; // Assuming you identify assets by some unique identifier (e.g., asset ID)
}

// Define action creators
export const addAsset = (asset: Asset): AddAssetAction => ({
  type: ADD_ASSET,
  payload: asset,
});

export const deleteAsset = (assetId: string): DeleteAssetAction => ({
  type: DELETE_ASSET,
  payload: assetId,
});

// Union type for all asset actions
export type AssetActionTypes = AddAssetAction | DeleteAssetAction;
