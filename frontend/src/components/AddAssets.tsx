import React from 'react';
import { Box, VStack, Heading, FormControl, FormLabel, Input, Select, Button, useToast, FormHelperText, FormErrorMessage } from '@chakra-ui/react';
import { useFormik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { addAssetsAsync } from '../thunks/assetsThunk';
import { selectProfile } from '../slice/profileSlice';
import { useNavigate } from 'react-router-dom';
import { Asset } from '../thunks/assetsThunk';

const AddAssets = () => {
  const dispatch = useDispatch();
  const toast = useToast();
  const navigate = useNavigate();
  const profile = useSelector(selectProfile);

  const formik = useFormik({
    initialValues: {
      name: '',
      location: '',
      will_to: '',
      note: '',
      // documents: [],
    },
    onSubmit: async (values:Asset) => {
      try {
        // Dispatch the action to add assets
        await dispatch(addAssetsAsync({userData: values, grantor_id: profile.data?.uuid_pk})).unwrap();

        // Reset form fields after successful submission
        formik.resetForm();

        toast({
          title: 'Asset Added',
          description: 'The asset has been successfully added.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });

        navigate('/dashboard');
      } catch (error) {
        console.error('Error adding asset:', error);

        toast({
          title: 'Error',
          description: 'An error occurred while adding the asset.',
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
        Add Assets
      </Heading>
      <form onSubmit={formik.handleSubmit} encType='multipart/form-data'>
        <VStack spacing="4" align="stretch">
          <FormControl isRequired>
            <FormLabel>Asset Name</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('name')}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Location</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('location')}
            />
          </FormControl>


          <FormControl isRequired>
            <FormLabel>Note</FormLabel>
            <Input
              type="text"
              {...formik.getFieldProps('note')}
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

          {/* <FormControl
            id="documents"
            isInvalid={formik.errors.documents && formik.touched.documents}
            
          >
            <FormLabel>Files</FormLabel>
            <Input
              type="file"
              multiple
              onChange={(event) => {
                formik.setFieldValue(
                  'documents',
                  Array.from(event.target.files)
                );
              }}
              onBlur={formik.handleBlur}
            />
            <FormHelperText>Multiple files can be added.</FormHelperText>
            <FormErrorMessage>{formik.errors.documents}</FormErrorMessage>
          </FormControl> */}

          <Button type="submit" colorScheme="teal"
          isLoading={formik.isSubmitting}>
            Add Asset
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default AddAssets;
