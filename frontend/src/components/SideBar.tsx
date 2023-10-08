// import {useState} from 'react';
import { Box,
        Text,
        IconButton,
        VStack,
        Button,
        Drawer,
        DrawerBody,
        DrawerHeader,
        DrawerContent,
        DrawerOverlay,
        DrawerCloseButton,
        Modal,
        ModalOverlay,
        ModalContent,
        ModalHeader,
        ModalBody,
        ModalFooter,
        useDisclosure,
        useColorModeValue,
        ModalCloseButton,
     } from '@chakra-ui/react';
import { HamburgerIcon, InfoIcon } from '@chakra-ui/icons';
import { useNavigate } from 'react-router-dom';


const Sidebar = () => {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const { isOpen: isDrawerOpen, onOpen: onDrawerOpen, onClose: onDrawerClose } = useDisclosure();
    const navigate = useNavigate();
    const accountType = localStorage.getItem('account_type');
    const isTrustee: boolean = accountType === 'trustee';

    const handleAddAsset = (type: string) => {
        if (type === 'physical') {
            navigate('/add-physical-asset');
            onClose();
        }
        else if (type === 'monetary') {
            navigate('/add-monetary-asset');
            onClose();
        }
    };

    const handleCloseModal = () => {
        onClose();
    };

    const handleOpenModal = () => {
        onOpen();
    }

    // const handleDrawerCloseModal = () => {
    //     onDrawerClose();
    // };

    // const handleDrawerOpenModal = () => {
    //     onDrawerOpen();
    // }

  return (
    <>
    <Modal motionPreset="slideInBottom" isOpen={isOpen} onClose={handleCloseModal}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Select Asset Type</ModalHeader>
          <ModalCloseButton />
          <ModalBody p={5} >
            <Button onClick={() => handleAddAsset('physical')}
              margin={2}
            >
              Physical Asset
            </Button>
            <Button onClick={() => handleAddAsset('monetary')}
              margin={2}
            >
              Monetary Asset
            </Button>
          </ModalBody>
          <ModalFooter>
            {/* You can add additional footer content here */}
          </ModalFooter>
        </ModalContent>
      </Modal>

    <Box
        minW={{ base: '100%', md: '100%' }}
        maxW={{ base: '100%', md: '100%' }}
        maxH={{ base: '100%', md: '100%' }}
        bg={useColorModeValue('gray.200', 'gray.800')}
        p="4"
        display={{ base: 'none', md: 'block' }}
      >
        <VStack align="stretch" spacing={4} mt={4}>
          <Button onClick={() => navigate('/')} >
            Home
          </Button>
          <Button onClick={handleOpenModal} isDisabled={accountType === 'trustee'}>Add Asset</Button>
          <Button onClick={() => navigate('/add-trustee')}
          isDisabled={accountType === 'trustee'}>
            Add Trustee
          </Button>
          <Button onClick={() => navigate('/add-beneficiary')}
          isDisabled={accountType === 'trustee'}>
            Add Beneficiary
          </Button>

          {isTrustee && (<><InfoIcon color={'orange'}></InfoIcon><Text>You cannot make changes to this account</Text></>)}
        </VStack>
      </Box>

      <Box display={{ base: 'block', md: 'none' }}>
        <IconButton
          icon={<HamburgerIcon />}
          onClick={isOpen ? onDrawerClose : onDrawerOpen}
          aria-label="Open Menu"
          variant="outline"
          colorScheme="blue"
          mt="2"
        />
        <Drawer isOpen={isDrawerOpen} placement="left" onClose={onDrawerClose} size="xs">
          <DrawerOverlay />
          <DrawerContent>
            <DrawerCloseButton />
            <DrawerHeader>Menu</DrawerHeader>
            <DrawerBody>
              <VStack align="stretch" spacing={4}>
                <Button onClick={() => navigate('/')} >
                    Home
                </Button>
                <Button onClick={handleOpenModal} isDisabled={accountType === 'trustee'}>Add Asset</Button>
                <Button onClick={() => navigate('/add-trustee')} isDisabled={accountType === 'trustee'}>
                    Add Trustee
                </Button>
                <Button onClick={() => navigate('/add-beneficiary')} isDisabled={accountType === 'trustee'}>
                    Add Beneficiary
                </Button>
              </VStack>
            </DrawerBody>
          </DrawerContent>
        </Drawer>
      </Box>
    </>
  );
};

export default Sidebar;
