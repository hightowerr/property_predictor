import React from 'react';
import { 
  CssBaseline, 
  Container, 
  ThemeProvider, 
  createTheme,
  Box,
  Typography 
} from '@mui/material';
import PricePredictionForm from './components/PricePredictionForm';

// Create a theme instance
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          py: 4,
          backgroundColor: 'background.default'
        }}
      >
        <Container maxWidth="md">
          <Typography 
            variant="h3" 
            component="h1" 
            align="center" 
            gutterBottom
            sx={{ mb: 4 }}
          >
            Property Price Predictor
          </Typography>
          <PricePredictionForm />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;