import { useState } from "react";
import "./App.css";
import {
  Box,
  Button,
  Stack,
  Typography,
  Paper,
  Autocomplete,
  TextField,
} from "@mui/material";
import TopNav from "./components/TopNav";
import axios from "axios";

function App() {
  const [keyword, setKeyword] = useState("");
  const [options, setOptions] = useState([
    "frontend-engineer",
    "backend-engineer",
    "software-engineer",
    "artificial-intelligence-engineer",
    "devops-engineer",
    "data-scientist",
  ]);
  const [companies, setCompanies] = useState([]);

  const handleScrape = async () => {
    if (!keyword) {
      alert("Please select or enter a keyword");
      return;
    }

    try {
      const { data } = await axios.post("http://127.0.0.1:8000/scrape", {
        keyword,
      });
      setCompanies(data.jobs);
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Failed to fetch company data.");
    }
  };

  return (
    <Box>
      <TopNav />
      <Stack width="70%" direction="row" margin="2rem auto" spacing={2}>
        <Autocomplete
          freeSolo
          fullWidth
          options={options}
          onInputChange={(event, newValue) => setKeyword(newValue)}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Search Companies"
              placeholder="Enter a keyword (e.g., Frontend-Developer, Backend-Developer, etc.)"
              variant="outlined"
            />
          )}
          onChange={(event, newValue) => {
            // if (newValue && !options.includes(newValue)) {
              // setOptions((prev) => [...prev, newValue]);
            // }
          }}
        />
        <Button
          variant="contained"
          sx={{ backgroundColor: "#ff622e" }}
          onClick={handleScrape}
        >
          <Typography variant="button">Search</Typography>
        </Button>
      </Stack>

      <Stack width="70%" margin="2rem auto" spacing={4}>
        {companies.length === 0 ? (
          <Typography variant="body1">
            No companies to display. Start your search above.
          </Typography>
        ) : (
          companies.map((company, index) => (
            <Paper key={index} elevation={2} sx={{ padding: 2 }}>
              <Stack direction="row" justifyContent="space-between">
                <Box>
                  <Typography variant="h5" color="#ff622e">{company.company}</Typography>
                  <Typography variant="h6">{company.title}</Typography>
                  <Typography variant="body1">
                    {company.additional_details}
                  </Typography>
                </Box>
                <img src={company.image_link} style={{width:"100px"}}/>
              </Stack>
            </Paper>
          ))
        )}
      </Stack>
    </Box>
  );
}

export default App;
