import React, { useState } from 'react';
import {
  Box,
  VStack,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Select,
  Button,
  useToast,
  FormHelperText,
} from '@chakra-ui/react';

// Sample data for beneficiaries
const beneficiariesList = ["Beneficiary 1", "Beneficiary 2", "Beneficiary 3"];

const AddAssets = () => {
  const [assetName, setAssetName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [yearAcquired, setYearAcquired] = useState('');
  const [beneficiary, setBeneficiary] = useState('');
  const [files, setFiles] = useState([]);

  const toast = useToast();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate form inputs
    if (!assetName || !quantity || !yearAcquired || !beneficiary || files.length === 0) {
      toast({
        title: 'Error',
        description: 'Please fill in all required fields.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    // Perform the necessary logic to add the asset (e.g., API call)
    // ...

    // Reset form fields after successful submission
    setAssetName('');
    setQuantity('');
    setYearAcquired('');
    setBeneficiary('');
    setFiles([]);

    toast({
      title: 'Asset Added',
      description: 'The asset has been successfully added.',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box p="4" m={20}>
      <Heading size="md" mb={4}>
        Add Assets
      </Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing="4" align="stretch">
          <FormControl isRequired>
            <FormLabel>Asset Name</FormLabel>
            <Input
              type="text"
              value={assetName}
              onChange={(e) => setAssetName(e.target.value)}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Quantity</FormLabel>
            <Input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Year Acquired</FormLabel>
            <Input
              type="number"
              value={yearAcquired}
              onChange={(e) => setYearAcquired(e.target.value)}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Beneficiary</FormLabel>
            <Select
              value={beneficiary}
              onChange={(e) => setBeneficiary(e.target.value)}
            >
              <option value="" disabled>Select Beneficiary</option>
              {beneficiariesList.map((name) => (
                <option key={name} value={name}>{name}</option>
              ))}
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Files</FormLabel>
            <Input
              type="file"
              multiple
              onChange={(e) => setFiles([...files, ...e.target.files])}
            />
            <FormHelperText>Multiple files can be added.</FormHelperText>
          </FormControl>

          <Button type="submit" colorScheme="teal">
            Add Asset
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default AddAssets;