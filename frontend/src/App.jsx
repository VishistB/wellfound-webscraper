import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Paper from '@mui/material/Paper';
import {Autocomplete, Box, Stack, Typography} from '@mui/material'
import TopNav from './components/TopNav';


function App() {
  return (
    <Box>
      <TopNav/>
      <Stack width="70%" margin="2rem auto">
        
      </Stack>
      <Stack width="70%" margin="2rem auto">
        <Paper elevation={4} sx={{padding:2}}>
          <Typography variant='h5'>Company name</Typography>
          <Typography variant='h6'>Role</Typography>
          <Typography variant='body'>Details</Typography>
        </Paper>
      </Stack>
    </Box>
  )
}

export default App
