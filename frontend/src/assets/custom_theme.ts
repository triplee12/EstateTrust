import { extendTheme } from '@chakra-ui/react';

const customTheme = extendTheme({
  colors: {
    primary: {
      50: '#e6e1ff',
      100: '#c4b4ff',
      200: '#a682ff',
      300: '#8760ff',
      400: '#715aff',
      500: '#5c41ff',
      600: '#5237e6',
      700: '#482ecc',
      800: '#3d24b3',
      900: '#2e1d8a',
    },
    secondary: {
      50: '#e5ebff',
      100: '#c0ccff',
      200: '#95a3ff',
      300: '#6c80ff',
      400: '#5887ff',
      500: '#437fff',
      600: '#3a72e6',
      700: '#3155cc',
      800: '#2849b3',
      900: '#1c328a',
    },
    accent1: '#a682ff',
    accent2: '#f75c03',
    text: '#542344',
  },
  components: {
    // Define component styles here, if needed
  },
});

export default customTheme;
