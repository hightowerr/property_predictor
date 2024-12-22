import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TextField, 
  Select, 
  MenuItem, 
  Button, 
  Grid, 
  Typography, 
  FormControl, 
  InputLabel,
  Paper
} from '@mui/material';

interface FormData {
  Year: number;
  District: string;
  property_type: string;
  County: string;
}

const PricePredictionForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    Year: new Date().getFullYear(),
    District: '',
    property_type: '',
    County: ''
  });
  
  const [propertyTypes, setPropertyTypes] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [counties, setCounties] = useState<string[]>([]);
  const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [propertyTypesRes, districtsRes] = await Promise.all([
          axios.get('http://localhost:5000/api/property-types'),
          axios.get('http://localhost:5000/api/districts')
        ]);

        setPropertyTypes(
          propertyTypesRes.data.property_types.map((pt: string) => pt.replace('property type_', ''))
        );
        setDistricts(
          districtsRes.data.districts.map((d: string) => d.replace('district_', ''))
        );
      } catch (err) {
        setError('Failed to load initial data');
        console.error(err);
      }
    };

    fetchInitialData();
  }, []);

  useEffect(() => {
    const fetchCounties = async () => {
      if (formData.District) {
        try {
          const response = await axios.get(`http://localhost:5000/api/counties?district=${formData.District}`);
          setCounties(
            response.data.counties
              .filter((c: string) => c.includes(`district_${formData.District}`))
              .map((c: string) => c.replace('district_', ''))
          );
        } catch (err) {
          setError('Failed to load counties');
          console.error(err);
        }
      }
    };

    fetchCounties();
  }, [formData.District]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setPredictedPrice(null);

    try {
      const response = await axios.get('http://localhost:5000/predict_home_price', { 
        params: formData 
      });

      setPredictedPrice(response.data.estimated_price);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Prediction failed');
      console.error(err);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        Home Price Predictor
      </Typography>
      
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Year"
              type="number"
              value={formData.Year}
              onChange={(e) => setFormData({
                ...formData, 
                Year: parseInt(e.target.value)
              })}
              inputProps={{ min: 2000, max: 2050 }}
            />
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>Property Type</InputLabel>
              <Select
                value={formData.property_type}
                label="Property Type"
                onChange={(e) => setFormData({
                  ...formData, 
                  property_type: e.target.value as string
                })}
              >
                {propertyTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>District</InputLabel>
              <Select
                value={formData.District}
                label="District"
                onChange={(e) => setFormData({
                  ...formData, 
                  District: e.target.value as string,
                  County: '' // Reset county when district changes
                })}
              >
                {districts.map((district) => (
                  <MenuItem key={district} value={district}>
                    {district}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth disabled={!formData.District}>
              <InputLabel>County</InputLabel>
              <Select
                value={formData.County}
                label="County"
                onChange={(e) => setFormData({
                  ...formData, 
                  County: e.target.value as string
                })}
              >
                {counties.map((county) => (
                  <MenuItem key={county} value={county}>
                    {county}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Button 
              fullWidth 
              variant="contained" 
              color="primary" 
              type="submit"
              disabled={!formData.District || !formData.property_type || !formData.County}
            >
              Predict Price
            </Button>
          </Grid>
        </Grid>
      </form>

      {error && (
        <Typography color="error" sx={{ mt: 2, textAlign: 'center' }}>
          {error}
        </Typography>
      )}

      {predictedPrice && (
        <Typography 
          variant="h5" 
          sx={{ 
            mt: 2, 
            textAlign: 'center', 
            color: 'primary.main' 
          }}
        >
          Estimated Price: £{predictedPrice.toLocaleString()}
        </Typography>
      )}
    </Paper>
  );
};

export default PricePredictionForm;
