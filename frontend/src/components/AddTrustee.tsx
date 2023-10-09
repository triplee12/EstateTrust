import {useState} from 'react';
import { useFormik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import {
  Flex,
  Box,
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
  useToast,
  useColorModeValue,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import {addTrusteeAsync, Trustee} from '../thunks/trusteeThunk';
import { selectProfile } from '../slice/profileSlice';
import { useNavigate } from 'react-router-dom';
import {AppDispatch} from '../store';


const AddTrustee = () => {
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();
  const dispatch: AppDispatch = useDispatch();
  const profile = useSelector(selectProfile);

  const formik = useFormik({
    initialValues: {
      first_name: '',
      last_name: '',
      middle_name: '',
      username: '',
      email: '',
      phone_number: '',
      password: '',
      relation: '',
      note: '',
      added_by: "",
    },
    onSubmit: async (values: Trustee) => {
      try{
        if (profile.data?.uuid_pk)
        await dispatch(addTrusteeAsync({userData:values, grantorId: profile.data?.uuid_pk})).unwrap(); // Assuming you have an action like addTrusteeAsync
              // Reset form fields after successful submission
        formik.resetForm();

        toast({
          title: 'Trustee Added',
          description: 'Trustee has been successfully added.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });

        navigate('/dashboard');
      } catch (error) {
        console.error('Error adding trustee:', error);

        toast({
          title: 'Error',
          description: 'An error occurred while adding the trustee.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    },
  });

  const { handleSubmit, handleChange, handleBlur, values } = formik;

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
            Add Trustee
          </Heading>
          <Text fontSize={'lg'} color={'gray.600'}>
            Provide details to add a new trustee ✌️
          </Text>
        </Stack>
        <Box rounded={'lg'} bg={useColorModeValue('white', 'gray.700')} boxShadow={'lg'} p={8}>
          <form onSubmit={handleSubmit}>
            <Stack spacing={4}>
              <FormControl id="first_name" isRequired>
                <FormLabel>First Name</FormLabel>
                <Input
                  type="text"
                  name="first_name"
                  value={values.first_name}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>
              <FormControl id="last_name">
                <FormLabel>Last Name</FormLabel>
                <Input
                  type="text"
                  name="last_name"
                  value={values.last_name}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>

              <FormControl id="middle_name">
                <FormLabel>Middle Name</FormLabel>
                <Input
                  type="text"
                  name="middle_name"
                  value={values.middle_name}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>

              <FormControl id="username" isRequired>
                <FormLabel>Username</FormLabel>
                <Input
                  type="text"
                  name="username"
                  value={values.username}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>

              <FormControl id="email" isRequired>
                <FormLabel>Email address</FormLabel>
                <Input
                  type="email"
                  name="email"
                  value={values.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>

              <FormControl id="phone_number" isRequired>
                <FormLabel>Phone Number</FormLabel>
                <Input
                  type="tel"
                  name="phone_number"
                  value={values.phone_number}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>

              <FormControl id="password" isRequired>
                <FormLabel>Password</FormLabel>
                <InputGroup>
                  <Input
                    type="password"
                    name="password"
                    value={values.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  <InputRightElement h={'full'}>
                    <Button
                      variant={'ghost'}
                      onClick={() => setShowPassword((showPassword) => !showPassword)}>
                      {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                    </Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>
              <FormControl id="relation" isRequired>
                <FormLabel>Relation</FormLabel>
                <Select
                  placeholder="Select relation"
                  name="relation"
                  value={values.relation}
                  onChange={handleChange}
                  onBlur={handleBlur}
                >
                  <option value="brother">Brother</option>
                  <option value="friend">Friend</option>
                  <option value="lawyer">Lawyer</option>
                  <option value="sister">Sister</option>
                </Select>
              </FormControl>
              <FormControl id="note">
                <FormLabel>Note</FormLabel>
                <Input
                  type="text"
                  name="note"
                  value={values.note}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
              </FormControl>
              <Stack spacing={10} pt={2}>
                <Button
                  type="submit"
                  loadingText="Submitting"
                  size="lg"
                  bg={'blue.400'}
                  color={'white'}
                  isLoading={formik.isSubmitting}
                  _hover={{
                    bg: 'blue.500',
                  }}
                >
                  Add Trustee
                </Button>
              </Stack>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Flex>
  );
};

export default AddTrustee;
