'use client';

import React from 'react';
import { Box, Container, Typography, Grid, Card, CardContent } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CheckroomIcon from '@mui/icons-material/Checkroom';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

const steps = [
  {
    icon: <CloudUploadIcon sx={{ fontSize: 50, color: 'primary.main' }} />,
    title: 'Upload Your Photo',
    description: 'Start by uploading a clear photo of yourself. Our AI will analyze your features to create accurate visualizations.',
  },
  {
    icon: <CheckroomIcon sx={{ fontSize: 50, color: 'secondary.main' }} />,
    title: 'Choose Your Outfit',
    description: 'Select from our collection of outfits or upload your own. Mix and match to find your perfect style.',
  },
  {
    icon: <LocationOnIcon sx={{ fontSize: 50, color: 'primary.main' }} />,
    title: 'Pick a Location',
    description: 'Choose from iconic locations around the world or upload your dream destination background.',
  },
  {
    icon: <AutoAwesomeIcon sx={{ fontSize: 50, color: 'secondary.main' }} />,
    title: 'Generate Your Image',
    description: 'Our Azure-powered AI creates a photorealistic image of you in that outfit at that location.',
  },
];

export default function HowItWorks() {
  return (
    <Box
      id="how-it-works"
      sx={{
        bgcolor: 'background.paper',
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
          How It Works
        </Typography>
        <Typography
          variant="h6"
          align="center"
          color="text.secondary"
          paragraph
          sx={{ mb: 6, maxWidth: 800, mx: 'auto' }}
        >
          Transform your style visualization in four simple steps
        </Typography>
        <Grid container spacing={4}>
          {steps.map((step, index) => (
            <Grid size={{ xs: 12, sm: 6, md: 3 }} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.3s, box-shadow 0.3s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
                  },
                }}
              >
                <CardContent
                  sx={{
                    flexGrow: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textAlign: 'center',
                    p: 3,
                  }}
                >
                  <Box sx={{ mb: 2 }}>{step.icon}</Box>
                  <Typography
                    variant="h6"
                    component="h3"
                    gutterBottom
                    sx={{ fontWeight: 600 }}
                  >
                    {step.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {step.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
}
