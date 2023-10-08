import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

// Create an Axios instance with default configurations
const api: AxiosInstance = axios.create({
  baseURL: 'https://bba7-197-210-85-57.ngrok-free.app/api/v1', // Replace with your API base URL
  // timeout: 5000, // Set a timeout for requests (optional)
  // withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    // You can set default headers here (e.g., authorization token)
  },
});

// Axios request interceptors
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    try {
      const authToken = localStorage.getItem('authToken');
      if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
      }
      return config;
    } catch (error) {
      console.error('Error setting Authorization header:', error);
      return Promise.reject(error);
    }
  },
  (error) => {
    // Handle request errors
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response: AxiosResponse) => {
    const token = localStorage.getItem('authToken');

    if (!token) {
      // Check if the response has data
      if (response.data && response.data.access_token) {
        const authToken = response.data.access_token;
        // Set the authentication token in local storage
        localStorage.setItem('authToken', authToken);
      }
    }
    return response; // Return only the data
  },
  (error) => {
    // Handle response errors (e.g., unauthorized, not found, etc.)
    return Promise.reject(error);
  }
);


// Helper function for making GET requests
export const get = async <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    const response = await api.get<T>(url, config);
    return response;

};

// Helper function for making POST requests
export const post = async <T>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig
): Promise<AxiosResponse<T>> => {
    const response = await api.post<T>(url, data, config);
    return response;
};

// Helper function for making PUT requests
export const put = async <T>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig
): Promise<AxiosResponse<T>> => {
    const response = await api.put<T>(url, data, config);
    return response;
};

// Helper function for making DELETE requests
export const del = async <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    const response = await api.delete<T>(url, config);
    return response;
};

export const removeAuthToken = (): void => {
  localStorage.removeItem('authToken');
};

export const setAuthToken = (token: string): void => {
  localStorage.setItem('authToken', token);
};