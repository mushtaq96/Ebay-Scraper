import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

function App() {
  const [query, setQuery] = useState("");
  const [recentQueries, setRecentQueries] = useState([]);

  const handleSearch = () => {
    // send query to the server here
    fetch(`http://localhost:8000/query?q=${query}`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
    // update recent queries
    setRecentQueries((prevRecentQueries) => [
      query,
      ...prevRecentQueries.slice(0, 9),
    ]);
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
    >
      <h1>eBay Giveaway Finder</h1>
      <Box display="flex" alignItems="center">
        <TextField
          label="Enter Query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button
          variant="contained"
          style={{ marginLeft: 8 }}
          onClick={handleSearch}
        >
          Subscribe
        </Button>
      </Box>
      <Box>
        <h3>Recent Queries</h3>
        <ul>
          {recentQueries.map((recentQuery, index) => (
            <li key={index}>{recentQuery}</li>
          ))}
        </ul>
      </Box>
    </Box>
  );
}

export default App;
