'use client';

import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Button,
  Paper,
  Stepper,
  Step,
  StepLabel,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const outfitOptions = [
  { id: 1, name: 'Casual Summer', color: '#FFE5B4' },
  { id: 2, name: 'Formal Business', color: '#2C3E50' },
  { id: 3, name: 'Evening Gown', color: '#8B4789' },
  { id: 4, name: 'Sports Attire', color: '#3498DB' },
];

const locationOptions = [
  { id: 1, name: 'Paris, Eiffel Tower', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
  { id: 2, name: 'New York, Times Square', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
  { id: 3, name: 'Tokyo, Shibuya', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
  { id: 4, name: 'Beach Sunset', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
];

const steps = ['Upload Photo', 'Select Outfit', 'Choose Location'];

export default function GetStarted() {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedOutfit, setSelectedOutfit] = useState<number | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<number | null>(null);
  const [photoUploaded, setPhotoUploaded] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handlePhotoUpload = () => {
    setPhotoUploaded(true);
  };

  const canProceed = () => {
    if (activeStep === 0) return photoUploaded;
    if (activeStep === 1) return selectedOutfit !== null;
    if (activeStep === 2) return selectedLocation !== null;
    return false;
  };

  return (
    <Box
      id="get-started"
      sx={{
        bgcolor: 'background.default',
        py: { xs: 8, md: 12 },
      }}
    >
      <Container maxWidth="lg">
        <Typography
          variant="h2"
          component="h2"
          align="center"
          gutterBottom
          sx={{ mb: 2 }}
        >
          Get Started
        </Typography>
        <Typography
          variant="h6"
          align="center"
          color="text.secondary"
          paragraph
          sx={{ mb: 6, maxWidth: 800, mx: 'auto' }}
        >
          Create your personalized visualization in three easy steps
        </Typography>

        <Paper elevation={2} sx={{ p: { xs: 3, md: 4 }, borderRadius: 3 }}>
          <Stepper activeStep={activeStep} sx={{ mb: 4 }} orientation={isMobile ? 'vertical' : 'horizontal'}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {activeStep === 0 && (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Paper
                sx={{
                  p: 6,
                  border: '2px dashed',
                  borderColor: photoUploaded ? 'success.main' : 'grey.300',
                  bgcolor: photoUploaded ? 'success.light' : 'grey.50',
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    bgcolor: 'grey.100',
                  },
                }}
                onClick={handlePhotoUpload}
              >
                {photoUploaded ? (
                  <>
                    <CheckCircleIcon sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
                    <Typography variant="h6" color="success.dark">
                      Photo Uploaded Successfully!
                    </Typography>
                  </>
                ) : (
                  <>
                    <CloudUploadIcon sx={{ fontSize: 80, color: 'grey.400', mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      Upload Your Photo
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Click to select a photo from your device
                    </Typography>
                  </>
                )}
              </Paper>
            </Box>
          )}

          {activeStep === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom align="center" sx={{ mb: 3 }}>
                Choose Your Outfit
              </Typography>
              <Grid container spacing={3}>
                {outfitOptions.map((outfit) => (
                  <Grid size={{ xs: 6, sm: 6, md: 3 }} key={outfit.id}>
                    <Card
                      sx={{
                        border: selectedOutfit === outfit.id ? 3 : 0,
                        borderColor: 'primary.main',
                        transition: 'all 0.3s',
                      }}
                    >
                      <CardActionArea onClick={() => setSelectedOutfit(outfit.id)}>
                        <Box
                          sx={{
                            height: 150,
                            bgcolor: outfit.color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            position: 'relative',
                          }}
                        >
                          {selectedOutfit === outfit.id && (
                            <CheckCircleIcon
                              sx={{
                                position: 'absolute',
                                top: 10,
                                right: 10,
                                fontSize: 30,
                                color: 'primary.main',
                              }}
                            />
                          )}
                        </Box>
                        <CardContent>
                          <Typography variant="body1" align="center" sx={{ fontWeight: 600 }}>
                            {outfit.name}
                          </Typography>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}

          {activeStep === 2 && (
            <Box>
              <Typography variant="h6" gutterBottom align="center" sx={{ mb: 3 }}>
                Select Your Location
              </Typography>
              <Grid container spacing={3}>
                {locationOptions.map((location) => (
                  <Grid size={{ xs: 12, sm: 6, md: 6 }} key={location.id}>
                    <Card
                      sx={{
                        border: selectedLocation === location.id ? 3 : 0,
                        borderColor: 'secondary.main',
                        transition: 'all 0.3s',
                      }}
                    >
                      <CardActionArea onClick={() => setSelectedLocation(location.id)}>
                        <Box
                          sx={{
                            height: 200,
                            background: location.gradient,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            position: 'relative',
                          }}
                        >
                          {selectedLocation === location.id && (
                            <CheckCircleIcon
                              sx={{
                                position: 'absolute',
                                top: 10,
                                right: 10,
                                fontSize: 30,
                                color: 'white',
                              }}
                            />
                          )}
                          <Typography variant="h5" sx={{ color: 'white', fontWeight: 600, textAlign: 'center' }}>
                            {location.name}
                          </Typography>
                        </Box>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}

          <Box sx={{ display: 'flex', flexDirection: 'row', pt: 4, gap: 2 }}>
            <Button
              color="inherit"
              disabled={activeStep === 0}
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Back
            </Button>
            <Box sx={{ flex: '1 1 auto' }} />
            {activeStep === steps.length - 1 ? (
              <Button
                variant="contained"
                onClick={() => alert('Generate Image! (This would trigger the Azure AI service)')}
                disabled={!canProceed()}
                size="large"
              >
                Generate Image
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!canProceed()}
              >
                Next
              </Button>
            )}
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}
