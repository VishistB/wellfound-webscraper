import React from "react";
// import {Stack} from '@mui/material'
// import Stack from "@mui/material/Stack";
import { Button, Typography, Stack } from "@mui/material";
import WLogo from "../assets/W_logo_alt.png";

export default function TopNav() {
  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="space-between"
      sx={{ height: "4rem", backgroundColor: "#2d3037", padding: "0.5rem" }}
    >
      {/* <Typography variant='h4' color='#ff622e'> WELLSCRAPER </Typography> */}
      <Stack direction="row" alignItems="center" justifyContent="center">
        <img src={WLogo} style={{width:"80px", margin:"0rem 2rem"}} />
      </Stack>
      <Typography
        variant="h4"
        color="#ff622e"
        fontWeight="bold"
        // fontFamily="Roboto Condensed"
        sx={{margin:"0 2rem"}}
      >
        WELLSCRAPER
      </Typography>
      {/* <Stack></Stack> */}
      {/* <Button color="error" variant="contained"><Typography variant="button" sx={{color:""}}>Logout</Typography></Button> */}
    </Stack>
  );
}
