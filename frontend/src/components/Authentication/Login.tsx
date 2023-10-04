import React from 'react';
import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  Checkbox,
  Stack,
  Button,
  Heading,
  Link,
  Text,
  useColorModeValue,
  HStack,
} from '@chakra-ui/react';
import { Formik, Form, Field, ErrorMessage } from 'formik'; // Import Formik components
import * as Yup from 'yup'; // Import Yup for validation
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();

  // Validation schema using Yup
  const validationSchema = Yup.object().shape({
    username: Yup.string().required('Username is required'),
    password: Yup.string().required('Password is required'),
  });

  // Handle form submission
  const handleLogin = (values: object) => {
    // Perform login logic here (e.g., API call)
    console.log('Logging in with values:', values);

    // Redirect to the dashboard page on successful login
    navigate('/dashboard');
  };

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
            initialValues={{ username: '', password: '' }}
            validationSchema={validationSchema}
            onSubmit={handleLogin}
          >
            {(formik) => (
              <Form>
                <Stack spacing={4}>
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
                      style={{ color: 'red' }}
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
                      style={{ color: 'red' }}
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
                </Stack>
              </Form>
            )}
          </Formik>
        </Box>
      </Stack>
    </Flex>
  );
}
