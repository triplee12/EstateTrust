import React from 'react';
import { Box, VStack, Heading, FormControl, FormLabel,
        Input, Button, useToast,Select, FormHelperText } from '@chakra-ui/react';
import { useFormik } from 'formik';
import { useDispatch } from 'react-redux';
import { addMonetaryAsync } from '../thunks/monetaryThunk'; // Assuming you have a thunk for adding monetary assets
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { selectProfile } from '../slice/profileSlice';


const AddMonetary = () => {
  const dispatch = useDispatch();
  const toast = useToast();
  const navigate = useNavigate();
  const profile = useSelector(selectProfile);

  const formik = useFormik({
    initialValues: {
      acc_name: '',
      acc_number: '',
      amount: '',
      bank_name: '',
      will_to: '',
      note: '',
    },
    onSubmit: async (values) => {
      try {
        // console.log(values)
        // console.log(profile.data?.uuid_pk)
        // Dispatch the action to add monetary assets
        await dispatch(addMonetaryAsync({userData: values, grantorId: profile.data?.uuid_pk})).unwrap();

        // Reset form fields after successful submission
        formik.resetForm();

        toast({
          title: 'Monetary Asset Added',
          description: 'The monetary asset has been successfully added.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });

        navigate('/dashboard');
      } catch (error) {
        console.error('Error adding monetary asset:', error);

        toast({
          title: 'Error',
          description: 'An error occurred while adding the monetary asset.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    },
  });

  return (
    <Box p="4" m={20}>
      <Heading size="md" mb={4}>
        Add Monetary Asset
      </Heading>
      <form onSubmit={formik.handleSubmit}>
        <VStack spacing="4" align="stretch">
          <FormControl isRequired>
            <FormLabel>Account Name</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('acc_name')}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Account Number</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('acc_number')}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Amount</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('amount')}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Bank Name</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('bank_name')}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Beneficiary</FormLabel>
            <Select
              {...formik.getFieldProps('will_to')}
            >
              <option value="" disabled>Select Beneficiary</option>
              {profile.data?.beneficiaries.map((item) => (
                <option key={item.uuid_pk} value={item.uuid_pk}>{item.first_name}</option>
              ))}
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Note</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('note')}
            />
          </FormControl>

          <Button type="submit" colorScheme="teal"
            isLoading={formik.isSubmitting}
          >
            Add Asset
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default AddMonetary;
