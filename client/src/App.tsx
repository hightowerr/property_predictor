import React from 'react';
import { CssBaseline, Container, ThemeProvider, createTheme } from '@mui/material';
import PricePredictionForm from './components/PricePredictionForm';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <PricePredictionForm />
      </Container>
    </ThemeProvider>
  );
}

export default App;
