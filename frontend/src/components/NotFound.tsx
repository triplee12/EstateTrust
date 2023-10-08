import React from 'react'
import NotFoundImg from '../assets/images/page-not-found-3385471.png'
import { Box, Container, Image } from '@chakra-ui/react'

function NotFound() {
  return (
    <>
        <Container maxW="container.xl" centerContent>
            <Box>
                <Image src={NotFoundImg} alt={'logo'} boxSize="100%" />
            </Box>
            <Box>NotFound</Box>
        </Container>
    </>
  )
}

export default NotFound