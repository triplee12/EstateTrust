import { Box, VStack, Heading, Button, useToast, Select, Input, FormControl, FormLabel, InputProps } from '@chakra-ui/react';
import { Formik, Field, Form, FieldInputProps, FormikHelpers } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { addBeneficiaryAsync } from '../thunks/beneficiaryThunk';
import { useNavigate } from 'react-router-dom';
import { selectProfile } from '../slice/profileSlice';
import { Beneficiary } from '../thunks/beneficiaryThunk';
import { AppDispatch } from '../store';

//@ts-ignore
interface CustomInputProps {
  field: FieldInputProps<any>;
  label: string;
}

const CustomInput: React.FC<CustomInputProps & InputProps> = ({ field, label, ...props }) => (
  <FormControl>
    <FormLabel>{label}</FormLabel>
    <Input {...field} {...props} />
  </FormControl>
);

const relationOptions = [
  'brother',
  'cousin',
  'daughter',
  'father',
  'friend',
  'grandchild',
  'husband',
  'inlaw',
  'mother',
  'nephew',
  'sister',
  'son',
  'stepson',
  'stepdaughter',
  'wife',
];

const AddBeneficiary = () => {
  const toast = useToast();
  const dispatch: AppDispatch = useDispatch();
  const navigate = useNavigate();
  const {data} = useSelector(selectProfile);

  const handleSubmit = async (values: Beneficiary, { resetForm }: FormikHelpers<Beneficiary>) => {
    try {
      if(data?.uuid_pk)
        // Dispatch the action to add the beneficiary
        await dispatch(addBeneficiaryAsync({userData: values, grantor_id: data.uuid_pk})).unwrap();
      else {
        throw new Error(`Profile not loaded`)
      }
      // Reset form fields after successful submission
      resetForm();

      toast({
        title: 'Beneficiary Added',
        description: 'The beneficiary has been successfully added.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

      // Move the navigation here
      navigate('/dashboard');
    } catch (error) {
      console.error('Error adding beneficiary:', error);

      toast({
        title: 'Error',
        description: 'An error occurred while adding the beneficiary.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p="4" m={20}>
      <Heading size="md" mb={4}>
        Add Beneficiary
      </Heading>
      <Formik
        initialValues={{ first_name: '', last_name: '', middle_name: '', relation: '' }}
        onSubmit={handleSubmit}
      >
        {(formik) => (
          <Form>
            <VStack spacing="4" align="stretch">
              <Field
                name="first_name"
                label="First Name"
                type="text"
                as={CustomInput}
              />

              <Field
                name="last_name"
                label="Last Name"
                type="text"
                as={CustomInput}
              />

              <Field
                name="middle_name"
                label="Middle Name"
                type="text"
                as={CustomInput}
              />

              <Field
                name="relation"
                label="Relation"
                as={Select}
              >
                <option value="" disabled>Select Relation</option>
                {relationOptions.map((relation) => (
                  <option key={relation} value={relation}>{relation}</option>
                ))}
              </Field>

              <Button type="submit" colorScheme="teal"
              isLoading={formik.isSubmitting}>
                Add Beneficiary
              </Button>
            </VStack>
          </Form>
        )}
      </Formik>
    </Box>
  );
};

export default AddBeneficiary;
