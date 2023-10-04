import { get, post, put, del } from './apiHelpers';

export const fetchData = async () => {
  try {
    const response = await get('/users'); // Replace with your API endpoint
    console.log(response); // Handle the response data
  } catch (error) {
    console.error(error); // Handle request errors
  }
};


export const postData = async () => {
  try {
    const response = await post('/users'); // Replace with your API endpoint
    console.log(response); // Handle the response data
  } catch (error) {
    console.error(error); // Handle request errors
  }
};

export const UpdateData = async () => {
  try {
    const response = await put('/users'); // Replace with your API endpoint
    console.log(response); // Handle the response data
  } catch (error) {
    console.error(error); // Handle request errors
  }
};

export const deleteData = async () => {
  try {
    const response = await del('/users'); // Replace with your API endpoint
    console.log(response); // Handle the response data
  } catch (error) {
    console.error(error); // Handle request errors
  }
};

