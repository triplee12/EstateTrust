import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  Stack,
  Button,
  Heading,
  Link,
  Text,
  Select,
  useColorModeValue,
  HStack,
} from '@chakra-ui/react';
import { Formik, Form, Field, ErrorMessage } from 'formik'; // Import Formik components
import * as Yup from 'yup'; // Import Yup for validation
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { loginAsync, LoginData } from '../../thunks/authenticationThunk';
import { selectAuth, clearError } from '../../slice/authenticationSlice';
import { AppDispatch } from '../../store';




export default function Login() {
  const navigate = useNavigate();
  const dispatch: AppDispatch = useDispatch();
  const auth = useSelector(selectAuth);

  // Validation schema using Yup
  const validationSchema = Yup.object().shape({
    username: Yup.string().required('Username is required'),
    password: Yup.string().required('Password is required').min(8),
    account_type: Yup.string().required('Account type is required'),
  });

  // Handle form submission
  const handleLogin = async (values: LoginData) => {
    try {
      // Dispatch the loginAsync action and wait for it to complete
      await dispatch(loginAsync(values)).unwrap();

      localStorage.setItem('account_type', values.account_type);

      // If the loginAsync action completes successfully, redirect to the dashboard page
      navigate('/dashboard');
    } catch (error) {
      // If the loginAsync action fails, handle the error here
      console.error('Failed to log in:', error);
    }
  };

  if (auth.error) {
    setTimeout(() => {
      dispatch(clearError());
    }, 10000);
  }

  return (
    <Flex
      minH={'100vh'}
      align={'center'}
      justify={'center'}
      bg={useColorModeValue('gray.50', 'gray.800')}>
      <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
        <Stack align={'center'}>
          <Heading fontSize={'4xl'}>Sign in to your account</Heading>
        </Stack>
        <Box
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}>
          {/* Use Formik to handle form state */}
          <Formik
            initialValues={{ username: '', password: '', account_type: '',}}
            validationSchema={validationSchema}
            onSubmit={handleLogin}
          >
            {(formik) => (
              <Form>
                <Stack spacing={4}>
                  {auth.error && (
                    <Text color="#BF360C" fontSize="md" textAlign="center" mt={2}>
                      {auth.error}
                    </Text>
                  )}
                  <FormControl id="username">
                    <FormLabel>Username</FormLabel>
                    <Field
                      as={Input}
                      type="text"
                      name="username"
                      placeholder="Your username"
                    />
                    <ErrorMessage
                      name="username"
                      component="div"
                    />
                  </FormControl>
                  <FormControl id="account_type" isRequired>
                    <FormLabel>Account Type</FormLabel>
                    <Field as={Select} name="account_type" placeholder="Select account type">
                      <option value="" disabled>Select account type</option>
                      <option value="grantor">Grantor</option>
                      <option value="trustee">Trustee</option>
                    </Field>
                    <ErrorMessage
                      name="account_type"
                      component="div"
                    />
                  </FormControl>

                  <FormControl id="password">
                    <FormLabel>Password</FormLabel>
                    <Field
                      as={Input}
                      type="password"
                      name="password"
                      placeholder="Your password"
                    />
                    <ErrorMessage
                      name="password"
                      component="div"
                    />
                  </FormControl>
                  <Stack
                    direction={{ base: 'column', sm: 'row' }}
                    align={'start'}
                    justify={'space-between'}
                    spacing={4}
                  >
                    {/* <Checkbox>Remember me</Checkbox> */}

                    <HStack spacing={12}>
                      <Link color={'blue.400'} href="/register">
                        Sign Up
                      </Link>
                      <Link color={'blue.400'} href="/forgot-password">
                        Forgot password?
                      </Link>
                    </HStack>
                  </Stack>
                  <Button
                    type="submit"
                    bg={'blue.400'}
                    color={'white'}
                    isLoading={formik.isSubmitting}
                    _hover={{
                      bg: 'blue.500',
                    }}
                  >
                    Sign in
                  </Button>
                  {/* {auth.status === 'loading' && <Spinner />} */}
                </Stack>
              </Form>
            )}
          </Formik>
        </Box>
      </Stack>
    </Flex>
  );
}
