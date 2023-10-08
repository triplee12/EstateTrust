import { get, post, put, del } from './apiHelpers';
import { AxiosResponse } from 'axios';


export const fetchData = async <T>(url: string): Promise<AxiosResponse<T>> => {
  try {
    const response = await get(url); // Replace with your API endpoint
    return response as AxiosResponse<T>; // Assuming your API returns the expected type
  } catch (error) {
    console.error(error); // Handle request errors
    throw error; // Re-throw the error to be caught in the calling code
  }
};


export const postData = async <T>(url: string, data: object): Promise<AxiosResponse<T>> => {
  try {
    const response = await post(url, data); // Replace with your API endpoint
    return response as AxiosResponse<T>; // Assuming your API returns the expected type
  } catch (error) {
    console.error(error); // Handle request errors
    throw error; // Re-throw the error to be caught in the calling code
  }
};

export const updateData = async <T>(url: string, data: object): Promise<AxiosResponse<T>> => {
  try {
    const response = await put(url, data); // Replace with your API endpoint
    return response as AxiosResponse<T>; // Assuming your API returns the expected type
  } catch (error) {
    console.error(error); // Handle request errors
    throw error; // Re-throw the error to be caught in the calling code
  }
};

export const deleteData = async (url: string): Promise<void> => {
  try {
    const response = await del(url); // Replace with your API endpoint
  } catch (error) {
    console.error(error); // Handle request errors
    throw error; // Re-throw the error to be caught in the calling code
  }
};

