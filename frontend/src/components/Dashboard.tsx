import React, { useState, useEffect } from 'react';
import {
  Tr,
  Th,
  Td,
  Box,
  Flex,
  Spacer,
  VStack,
  Heading,
  Text,
  HStack,
  Table,
  Thead,
  Tbody,
  Button,
  IconButton,
  Tooltip,
  useToast,
  useDisclosure,
  useBreakpointValue,
  useColorModeValue,
} from '@chakra-ui/react';
import { HamburgerIcon, DeleteIcon, ArrowUpIcon } from '@chakra-ui/icons';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { selectProfile } from '../slice/profileSlice';
import { selectAuth } from '../slice/authenticationSlice';
import { fetchProfileData } from '../thunks/profileThunk';
import { AddBeneficiaryApiResponse } from '../thunks/beneficiaryThunk';
import { deleteAssetsAsync } from '../thunks/assetsThunk';
import { deleteBeneficiaryAsync } from '../thunks/beneficiaryThunk';
import { deleteTrusteeAsync } from '../thunks/trusteeThunk';
import { deleteMonetaryAsync } from '../thunks/monetaryThunk';
import Sidebar from './SideBar';


const Dashboard = () => {
  const [assets, setAssets] = useState([]);
  const isDrawer = useBreakpointValue({ base: true, lg: false });
  const dispatch = useDispatch();
  const auth = useSelector(selectAuth);
  const profile = useSelector(selectProfile);

  const { isOpen, onOpen, onClose } = useDisclosure();
  const navigate = useNavigate();
  const toast = useToast();

  const account_type = localStorage.getItem('account_type');
  const isTrustee: boolean = account_type === 'trustee';

  const deleteAsset = async (deleteType: string, id: string) => {
    // Make API call to delete the asset with the given id
    try {
      // Your API call logic goes here
      if (deleteType === 'physical') {
        await dispatch(deleteAssetsAsync({grantor_id: profile.data?.uuid_pk, asset_id: id})).unwrap();
      }
      else if (deleteType === 'monetary') {
        await dispatch(deleteMonetaryAsync({grantor_id: profile.data?.uuid_pk, asset_id: id})).unwrap();
      }
      else if (deleteType === 'trustee') {
        await dispatch(deleteTrusteeAsync({grantor_id: profile.data?.uuid_pk, trustee_id: id})).unwrap();
      }
      else if (deleteType === 'beneficiary') {
        await dispatch(deleteBeneficiaryAsync({grantor_id: profile.data?.uuid_pk, bene_id: id})).unwrap();
      }

      toast({
        title: 'Deleted Successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

    } catch (error) {
      console.error('Error deleting asset:', error);

      toast({
        title: 'Error',
        description: 'Deletion was not successful.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  function findFirstNameById(id: string, objectList: AddBeneficiaryApiResponse[]) {
    const matchingObject = objectList.find(obj => obj.uuid_pk === id);

    if (matchingObject) {
      return matchingObject.first_name;
    } else {
      return null; // or throw new Error('Object not found');
    }
}


  useEffect(() =>{
    try {
      dispatch(fetchProfileData(auth.id)).unwrap();
    } catch (error) {
      console.log(error);
    }
  }, [auth.id, dispatch]);

  useEffect(() => {
    setAssets(profile?.data?.assets)
  }, [profile]);

  return (
    <>
    <Box flex="1" >
    <HStack m={4}>
      <Box w={'20%'} boxShadow={'lg'}
      rounded={'lg'}
      >
        <Sidebar />
      </Box>
      <VStack m={4} align="left" w="50%">
        <Box mb={8}
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}
          maxH="300px"  // Adjust the height as needed
          overflowY="auto"
        >
          <Heading size="md" mb={4}>
            Physical Assets
          </Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Asset Name</Th>
                <Th>Location</Th>
                <Th>Beneficiary</Th>
                {/* <Th>File</Th> */}
                <Th>Update</Th>
                <Th>Delete</Th>
              </Tr>
            </Thead>
            <Tbody>
              {assets.map((asset) => (
                <Tr key={asset.id}>
                  <Td>{asset.name}</Td>
                  <Td>{asset.location}</Td>
                  <Td>{findFirstNameById(asset.will_to, profile.data?.beneficiaries)}</Td>
                  {/* <Td>{asset.documents}</Td> */}
                  <Td>
                    <IconButton
                      icon={<ArrowUpIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset(asset.id)}
                      aria-label='Delete Asset'
                    />
                  </Td>
                  <Td>
                    <IconButton
                      icon={<DeleteIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset('physical', asset.uuid_pk)}
                      aria-label='Delete Asset'
                      isDisabled={isTrustee}
                    />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>

        <Box mb={8}
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}
          maxH="300px"  // Adjust the height as needed
          overflowY="auto"
        >
          <Heading size="md" mb={4}>
            Monetary Assets
          </Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Bank Name</Th>
                <Th>Amount</Th>
                <Th>Beneficiary</Th>
                <Th>Update</Th>
                <Th>Delete</Th>
              </Tr>
            </Thead>
            <Tbody>
              {profile.data?.monetaries.map((money) => (
                <Tr key={money.uuid_pk}>
                  <Td>{money.bank_name}</Td>
                  <Td>{money.amount}</Td>
                  <Td>{findFirstNameById(money.will_to, profile.data?.beneficiaries)}</Td>
                  <Td>
                    <IconButton
                      icon={<ArrowUpIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset(asset.id)}
                      aria-label='Delete Asset'
                    />
                  </Td>
                  <Td>
                    <IconButton
                      icon={<DeleteIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset('monetary', asset.id)}
                      aria-label='Delete Asset'
                      isDisabled={isTrustee}
                    />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </VStack>
      <VStack>

        <Box m={4}
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}
          maxH="300px"  // Adjust the height as needed
          overflowY="auto"
          >

          <Heading size="md" mb={4}>
            Trustees
          </Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>First Name</Th>
                <Th>Last Name</Th>
                <Th>Title</Th>
                <Th>Delete</Th>
              </Tr>
            </Thead>
            <Tbody >
              {profile.data?.executors.map((trustee) => (
                <Tr key={trustee.uuid_pk}>
                  <Td>{trustee.first_name}</Td>
                  <Td>{trustee.last_name}</Td>
                  <Td>{trustee.relation}</Td>
                  <Td>
                    <IconButton
                      icon={<DeleteIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset('trustee', trustee.uuid_pk)}
                      aria-label='Delete Asset'
                      isDisabled={isTrustee}
                    />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
        <Box m={4}
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}
          maxH="300px"  // Adjust the height as needed
          overflowY="auto"
          >

          <Heading size="md" mb={4}>
            Beneficiaries
          </Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>First Name</Th>
                <Th>Last Name</Th>
                <Th>Relation</Th>
                <Th>Delete</Th>
              </Tr>
            </Thead>
            <Tbody>
              {profile.data?.beneficiaries.map((item) => (
                <Tr key={item.uuid_pk}>
                  <Td>{item.first_name}</Td>
                  <Td>{item.last_name}</Td>
                  <Td>{item.relation}</Td>
                  {/* <Td>{item.file}</Td> */}
                  <Td>
                    <IconButton
                      icon={<DeleteIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset('trustee', item.uuid_pk)}
                      aria-label='Delete Asset'
                      isDisabled={isTrustee}
                    />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </VStack>
    </HStack>
      </Box>
    </>
  );
};

export default Dashboard;
