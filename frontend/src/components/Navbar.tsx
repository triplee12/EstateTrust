import React from 'react'
import {
  Box,
  Flex,
  Avatar,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  // useDisclosure,
  useColorModeValue,
  Stack,
  useColorMode,
  Center,
  Link,
  Image,
} from '@chakra-ui/react'
import { MoonIcon, SunIcon } from '@chakra-ui/icons'
import { useDispatch, useSelector } from 'react-redux'
import { selectAuth } from '../slice/authenticationSlice'
import { selectProfile } from '../slice/profileSlice'
import { logoutAsync } from '../thunks/authenticationThunk'
import { useNavigate } from 'react-router-dom'
import Logo from '../assets/images/house-lock.png'
import { AppDispatch } from '../store'
interface Props {
  isLoggedIn: boolean;
  children: React.ReactNode;
}

const NavLink = (props: Props) => {
  const { children, isLoggedIn } = props;

  return (
    <Box
      as="a"
      px={2}
      py={1}
      rounded={'md'}
      _hover={{
        textDecoration: 'none',
        bg: useColorModeValue('gray.200', 'gray.700'),
      }}
      href={isLoggedIn ? '#' : '/login'} // Link to login if not logged in
    >
      {children}
    </Box>
  );
}

export default function Nav() {
  const { colorMode, toggleColorMode } = useColorMode();
  // const { isOpen, onOpen, onClose } = useDisclosure();
  const dispatch: AppDispatch = useDispatch();
  const navigate = useNavigate();
  const auth = useSelector((selectAuth));
  const profile = useSelector((selectProfile));

  const handleLogout = async () => {
    try {
      // Dispatch the loginAsync action and wait for it to complete
      await dispatch(logoutAsync()).unwrap();
      localStorage.removeItem('account_type');

      // If the logout action completes successfully, redirect to the login page
      navigate('/login');
    } catch (error) {
      // If the loginAsync action fails, handle the error here
      console.error('Failed to log out:', error);
    }
  };


  return (
    <>
      <Box bg={useColorModeValue('gray.100', 'gray.900')} px={5}>
        <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
          <Box>
            <Link href={'/'}>
                <Image src={Logo} alt={'logo'} boxSize="30px" />
            </Link>
          </Box>

          <Flex alignItems={'center'}>
            <Stack direction={'row'} spacing={7}>
              <Button onClick={toggleColorMode}>
                {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
              </Button>

              {auth.authenticated ? (
                <Menu>
                  <MenuButton
                    as={Button}
                    rounded={'full'}
                    variant={'link'}
                    cursor={'pointer'}
                    minW={0}>
                    <Avatar
                      size={'sm'}
                      src={'https://avatars.dicebear.com/api/male/username.svg'}
                    />
                  </MenuButton>
                  <MenuList alignItems={'center'}>
                    <br />
                    <Center>
                      <Avatar
                        size={'2xl'}
                        src={'https://avatars.dicebear.com/api/male/username.svg'}
                      />
                    </Center>
                    <br />
                    <Center>
                      <p>{profile?.data?.username}</p>
                    </Center>
                    <br />
                    <MenuDivider />
                    <MenuItem>Account Settings</MenuItem>
                    <MenuItem
                    onClick={handleLogout}
                    >Logout</MenuItem>
                  </MenuList>
                </Menu>
              ) : (
                <NavLink isLoggedIn={auth.authenticated}>Login</NavLink>
              )}
            </Stack>
          </Flex>
        </Flex>
      </Box>
    </>
  );
}