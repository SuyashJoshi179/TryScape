'use client';

import React from 'react';
import { Box, Container, Typography, Grid, useTheme, useMediaQuery } from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import Button from '@mui/material/Button';

export default function HeroSection() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box
      id="home"
      sx={{
        bgcolor: 'background.default',
        pt: { xs: 8, md: 12 },
        pb: { xs: 8, md: 12 },
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4} alignItems="center">
          <Grid size={{ xs: 12, md: 6 }}>
            <Box>
              <Typography
                variant="h1"
                component="h1"
                gutterBottom
                sx={{
                  background: 'linear-gradient(45deg, #1976d2 30%, #9c27b0 90%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  mb: 3,
                }}
              >
                See Yourself in Any Outfit, Anywhere
              </Typography>
              <Typography
                variant="h6"
                color="text.secondary"
                paragraph
                sx={{ mb: 4, lineHeight: 1.8 }}
              >
                TryScape uses Azure-powered AI to generate photorealistic images of you wearing any outfit in any location. Try before you buy, visualize your style anywhere.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                <Button
                  variant="contained"
                  size="large"
                  endIcon={<ArrowForwardIcon />}
                  href="#get-started"
                  sx={{ py: 1.5, px: 4 }}
                >
                  Get Started
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  href="#how-it-works"
                  sx={{ py: 1.5, px: 4 }}
                >
                  Learn More
                </Button>
              </Box>
            </Box>
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <Box
              sx={{
                position: 'relative',
                height: { xs: 300, md: 400 },
                bgcolor: 'grey.100',
                borderRadius: 4,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              }}
            >
              <AutoAwesomeIcon sx={{ fontSize: { xs: 100, md: 150 }, color: 'white', opacity: 0.3 }} />
              <Typography
                variant="h4"
                sx={{
                  position: 'absolute',
                  color: 'white',
                  fontWeight: 600,
                  textAlign: 'center',
                  px: 2,
                }}
              >
                AI-Powered Visualization
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
