import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Alert,
  CircularProgress,
  InputAdornment
} from '@mui/material';

interface FormData {
  Year: string;
  District: string;
  property_type: string;
  County: string;
}

interface PredictionResponse {
  estimated_price: number;
  error?: string;
}

const PricePredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    Year: new Date().getFullYear().toString(),
    District: '',
    property_type: '',
    County: ''
  });

  const [propertyTypes, setPropertyTypes] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [counties, setCounties] = useState<string[]>([]);
  const [prediction, setPrediction] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [districtSearch, setDistrictSearch] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [propertyTypesRes, districtsRes, countiesRes] = await Promise.all([
          fetch(`${process.env.REACT_APP_API_URL}/api/property-types`),
          fetch(`${process.env.REACT_APP_API_URL}/api/districts`),
          fetch(`${process.env.REACT_APP_API_URL}/api/counties`)
        ]);

        const propertyTypesData = await propertyTypesRes.json();
        const districtsData = await districtsRes.json();
        const countiesData = await countiesRes.json();

        const processedPropertyTypes = propertyTypesData.property_types.map((type: string) => 
          type.replace('property type_', ''));
        
        const processedDistricts = districtsData.districts
          .map((district: string) => district.replace('district_', ''))
          .sort((a: string, b: string) => a.localeCompare(b));
        
        const processedCounties = countiesData.counties.map((county: string) => 
          county.replace('county_', ''));

        setPropertyTypes(processedPropertyTypes);
        setDistricts(processedDistricts);
        setCounties(processedCounties);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load form options. Please try again later.');
      }
    };

    fetchData();
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    if (name === 'districtSearch') {
      setDistrictSearch(value);
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
      setPrediction(null);
      setError(null);
    }
  };

  const handleSelectChange = (event: SelectChangeEvent) => {
    const { name, value } = event.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setPrediction(null);
    setError(null);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setPrediction(null);
    setError(null);

    const formBody = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      formBody.append(key, value);
    });

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/predict_home_price`, {
        method: 'POST',
        body: formBody
      });

      const data: PredictionResponse = await response.json();

      if (response.ok) {
        setPrediction(data.estimated_price);
      } else {
        setError(data.error || 'Failed to get prediction');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
      maximumFractionDigits: 0
    }).format(price);
  };

  const filteredDistricts = districts.filter(district =>
    district.toLowerCase().includes(districtSearch.toLowerCase())
  );

  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Property Price Predictor
      </Typography>
      <Typography variant="body1" sx={{ mb: 4 }}>
        Enter your property details below to get a price prediction
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {prediction !== null && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Estimated Property Price: {formatPrice(prediction)}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit} noValidate>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              required
              fullWidth
              name="Year"
              label="Year"
              type="number"
              value={formData.Year}
              onChange={handleInputChange}
              inputProps={{ min: 1900, max: 2100 }}
            />
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="property-type-label">Property Type</InputLabel>
              <Select
                labelId="property-type-label"
                name="property_type"
                value={formData.property_type}
                label="Property Type"
                onChange={handleSelectChange}
              >
                {propertyTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type.toUpperCase()}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="district-label">District</InputLabel>
              <Select
                labelId="district-label"
                name="District"
                value={formData.District}
                label="District"
                onChange={handleSelectChange}
                MenuProps={{
                  PaperProps: {
                    style: {
                      maxHeight: 300
                    }
                  }
                }}

                // startAdornment={
                //   <InputAdornment position="start">
                //     <TextField
                //       size="small"
                //       placeholder="Search districts..."
                //       name="districtSearch"
                //       value={districtSearch}
                //       onChange={handleInputChange}
                //       onClick={(e) => e.stopPropagation()}
                //       sx={{ m: 1, width: '90%' }}
                //     />
                //   </InputAdornment>
                // }
              >
                {filteredDistricts.map((district) => (
                  <MenuItem key={district} value={district}>
                    {district}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="county-label">County</InputLabel>
              <Select
                labelId="county-label"
                name="County"
                value={formData.County}
                label="County"
                onChange={handleSelectChange}
              >
                {counties.map((county) => (
                  <MenuItem key={county} value={county}>
                    {county.charAt(0).toUpperCase() + county.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              size="large"
              disabled={loading}
              sx={{ mt: 2 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Get Price Prediction'
              )}
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
};

export default PricePredictionForm;
