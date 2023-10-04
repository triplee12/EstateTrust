import React, { useState } from 'react';
import {
  Box,
  Flex,
  IconButton,
  Spacer,
  VStack,
  Heading,
  useBreakpointValue,
  Drawer,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  DrawerHeader,
  DrawerBody,
  DrawerFooter,
  SimpleGrid,
  Text,
  HStack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
} from '@chakra-ui/react';
import { HamburgerIcon, DeleteIcon } from '@chakra-ui/icons';
import { Link } from 'react-router-dom';

// Sample data for assets and beneficiaries
const sampleAssets = [
  { id: 1, name: "Asset 1", quantity: 10, beneficiaries: "Beneficiary 1, Beneficiary 2", file: "file.pdf" },
  { id: 2, name: "Asset 2", quantity: 5, beneficiaries: "Beneficiary 3, Beneficiary 4", file: "file.doc" },
  // Add more assets as needed
];

const Sidebar = () => {
  return (
    <Flex direction="column" h="100%" bg="gray.800" color="white" p="4" border={"1px"}>
      <Link to="/" > <Button marginY={1}>Home</Button></Link>
      <Link to="/add-assets"><Button marginY={1}>Add Assets</Button></Link>
      <Link to="/add-beneficiaries"><Button marginY={1}>Add Beneficiaries</Button></Link>
      <Link to="/add-assets"><Button marginY={1}>Set Counsel</Button></Link>
    </Flex>
  );
};

const Dashboard = () => {
  const [assets, setAssets] = useState(sampleAssets);
  const isDrawer = useBreakpointValue({ base: true, lg: false });
  const [isDrawerOpen, setIsDrawerOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setIsDrawerOpen(true);
  };

  const handleDrawerClose = () => {
    setIsDrawerOpen(false);
  };

  const deleteAsset = async (id: number) => {
    // Make API call to delete the asset with the given id
    try {
      // Your API call logic goes here

      // Assuming the API call is successful, update the state to reflect the deletion
      setAssets((prevAssets) => prevAssets.filter((asset) => asset.id !== id));
    } catch (error) {
      console.error('Error deleting asset:', error);
    }
  };

  return (
    <Flex m={4}>
      {/* Sidebar for Large Screens */}
      {!isDrawer && <Sidebar />}

      <Box flex="1" ml={!isDrawer ? '240px' : '0'}>
        {/* Menu Button for Small Screens */}
        {isDrawer && (
          <>
            <IconButton
              icon={<HamburgerIcon />}
              onClick={handleDrawerOpen}
              aria-label="Open Menu"
              variant="outline"
              colorScheme="white"
              m="4"
              display={{ lg: 'none' }}
            />
            <Drawer isOpen={isDrawerOpen} placement="right" onClose={handleDrawerClose}>
              <DrawerOverlay />
              <DrawerContent>
                <DrawerCloseButton />
                <DrawerHeader>Menu</DrawerHeader>
                <DrawerBody>
                  <Sidebar />
                </DrawerBody>
                <DrawerFooter>
                  {/* Additional Drawer Footer Content */}
                </DrawerFooter>
              </DrawerContent>
            </Drawer>
          </>
        )}

        <Box mb={8}>
          <Heading size="md" mb={4}>
            Assets
          </Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Asset Name</Th>
                <Th>Quantity</Th>
                <Th>Beneficiaries</Th>
                <Th>File</Th>
                <Th>Delete</Th>
              </Tr>
            </Thead>
            <Tbody>
              {assets.map((asset) => (
                <Tr key={asset.id}>
                  <Td>{asset.name}</Td>
                  <Td>{asset.quantity}</Td>
                  <Td>{asset.beneficiaries}</Td>
                  <Td>{asset.file}</Td>
                  <Td>
                    <IconButton
                      icon={<DeleteIcon />}
                      colorScheme="red"
                      variant="outline"
                      onClick={() => deleteAsset(asset.id)}
                      aria-label='Delete Asset'
                    />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </Box>
    </Flex>
  );
};

export default Dashboard;
