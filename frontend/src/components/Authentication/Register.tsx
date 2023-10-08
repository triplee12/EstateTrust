import { useState, useEffect } from 'react';
import {
  Flex,
  Box,
  HStack,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Select,
  Stack,
  Button,
  Heading,
  Text,
  useColorModeValue,
  Link,
  useToast,
  Spinner,
  FormErrorMessage,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import { useDispatch, useSelector } from 'react-redux';
import { registerAsync, RegistrationData } from '../../thunks/registerThunks'// Adjust the import path based on your project structure
import { registerAuth, clearError } from '../../slice/registerSlice';
import { useNavigate } from 'react-router-dom';


const SignupCard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const regState = useSelector(registerAuth);
  const [showPassword, setShowPassword ]= useState(false);
  const toast = useToast();

  const validationSchema = Yup.object().shape({
    first_name: Yup.string().required('First Name is required'),
    last_name: Yup.string(),
    middle_name: Yup.string(),
    username: Yup.string().required('Username is required'),
    email: Yup.string().email('Invalid email').required('Email is required'),
    phone_number: Yup.string().required('Phone number is required'),
    date_of_birth: Yup.date().required('Date of Birth is required'),
    gender: Yup.string().required('Gender is required'),
    password: Yup.string().required('Password is required'),
  });

  const handleSignup = async (values: RegistrationData) => {
    try {
      // Dispatch the registerAsync action and wait for it to complete
      await dispatch(registerAsync(values)).unwrap();

      setIsOpen(!isOpen);
      // If the registerAsync action completes successfully, redirect to the login page
      navigate('/login');
    } catch (error) {
      // If the registerAsync action fails, handle the error here
      console.error('Failed to register:', error);
    }
  };

  useEffect(() => {
    if (isOpen) {
      toast({
        title: 'Registration Successful',
        description: 'You have successfully registered.',
        status: 'success',
        duration: 5000, // Display the toast for 5 seconds
        isClosable: true,
      });
    }
  }, [isOpen, toast]);

  if (regState.error) {
      setTimeout(() => {
        dispatch(clearError());
      }, 10000);
  }

  return (
    <Flex
      minH={'100vh'}
      align={'center'}
      justify={'center'}
      bg={useColorModeValue('gray.50', 'gray.800')}
    >
      <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
        <Stack align={'center'}>
          <Heading fontSize={'4xl'} textAlign={'center'}>
            Sign up
          </Heading>
          <Text fontSize={'lg'} color={'gray.600'}>
            to enjoy all of our cool features ✌️
          </Text>
        </Stack>
        <Box
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}
        >
          <Formik
            initialValues={{
              first_name: '',
              last_name: '',
              middle_name: '',
              username: '',
              email: '',
              phone_number: '',
              date_of_birth: '',
              gender: '',
              password: '',
            }}
            validationSchema={validationSchema}
            onSubmit={handleSignup}
          >
           {(formik) => (
            <Form>
              <Stack spacing={4}>
                {regState.error && (
                    <Text color="#BF360C" fontSize="md" textAlign="center" mt={2}>
                      {regState.error}
                    </Text>
                  )}
                <HStack spacing={4}>
                  <Field name="first_name">
                    {({ field, meta }) => (
                      <FormControl id="first_name" isInvalid={meta.touched && meta.error}>
                        <FormLabel>First Name</FormLabel>
                        <Input {...field} type="text" />
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Field name="last_name">
                    {({ field, meta }) => (
                      <FormControl id="last_name" isInvalid={meta.touched && meta.error}>
                        <FormLabel>Last Name</FormLabel>
                        <Input {...field} type="text" />
                        <FormErrorMessage>{meta.error}</FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Field name="middle_name">
                    {({ field, meta }) => (
                      <FormControl id="middle_name" isInvalid={meta.touched && meta.error}>
                        <FormLabel>Middle Name</FormLabel>
                        <Input {...field} type="text" />
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                </HStack>

                <Field name="username">
                  {({ field, meta }) => (
                    <FormControl id="username" isInvalid={meta.touched && meta.error}>
                      <FormLabel>Username</FormLabel>
                      <Input {...field} type="text" />
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                    </FormControl>
                  )}
                </Field>

                <Field name="email">
                  {({ field, meta }) => (
                    <FormControl id="email" isInvalid={meta.touched && meta.error}>
                      <FormLabel>Email address</FormLabel>
                      <Input {...field} type="email" />
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                    </FormControl>
                  )}
                </Field>

                <Field name="phone_number">
                  {({ field, meta }) => (
                    <FormControl id="phone_number" isInvalid={meta.touched && meta.error}>
                      <FormLabel>Phone Number</FormLabel>
                      <Input {...field} type="tel" />
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                    </FormControl>
                  )}
                </Field>

                <Field name="date_of_birth">
                  {({ field, meta }) => (
                    <FormControl id="date_of_birth" isInvalid={meta.touched && meta.error}>
                      <FormLabel>Date of Birth</FormLabel>
                      <Input {...field} type="date" />
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                      </FormControl>
                  )}
                </Field>

                <Field name="gender">
                  {({ field, meta }) => (
                    <FormControl id="gender" isInvalid={meta.touched && meta.error}>
                      <FormLabel>Gender</FormLabel>
                      <Select {...field} placeholder="Select gender">
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                      </Select>
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                    </FormControl>
                  )}
                </Field>

                <Field name="password">
                  {({ field, meta }) => (
                    <FormControl id="password" isInvalid={meta.touched && meta.error}>
                      <FormLabel>Password</FormLabel>
                      <InputGroup>
                        <Input {...field} type={showPassword ? 'text' : 'password'} autoComplete='on' />
                        <InputRightElement h={'full'}>
                          <Button
                            variant={'ghost'}
                            onClick={() => setShowPassword((showPassword) => !showPassword)}
                          >
                            {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                          </Button>
                        </InputRightElement>
                      </InputGroup>
                      <FormErrorMessage>{meta.error}</FormErrorMessage>
                    </FormControl>
                  )}
                </Field>

                <Stack spacing={10} pt={2}>
                  <Button
                    type="submit"
                    size="lg"
                    bg={'blue.400'}
                    color={'white'}
                    isLoading={formik.isSubmitting}
                    _hover={{
                      bg: 'blue.500',
                    }}
                  >
                    {regState.status === 'loading' ? <Spinner /> : 'Sign up'}
                    
                  </Button>
                </Stack>

                <Stack pt={6}>
                  <Text align={'center'}>
                    Already a user?{' '}
                    <Link href="/login" color={'blue.400'}>
                      Login
                    </Link>
                  </Text>
                </Stack>
              </Stack>
            </Form>
            )}
          </Formik>
        </Box>
      </Stack>
    </Flex>
  );
};

export default SignupCard;
