import React from 'react';
import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Flex,
  Spacer,
} from '@chakra-ui/react';

const AddBeneficiary = () => {
  const handleAddBeneficiary = () => {
    // Implement logic to handle adding beneficiary
    console.log('Adding beneficiary...');
  };

  return (
    <Box p={8}>
      <Heading mb={4}>Add Beneficiary</Heading>
      <form>
        <FormControl id="name" mb={4}>
          <FormLabel>Name</FormLabel>
          <Input type="text" placeholder="Enter beneficiary's name" />
        </FormControl>

        <FormControl id="relationship" mb={4}>
          <FormLabel>Relationship</FormLabel>
          <Input type="text" placeholder="Enter relationship" />
        </FormControl>

        <Flex>
          <Spacer />
          <Button colorScheme="teal" onClick={handleAddBeneficiary}>
            Add Beneficiary
          </Button>
        </Flex>
      </form>
    </Box>
  );
};

export default AddBeneficiary;
