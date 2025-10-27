'use client';

import React from 'react';
import { Box, Container, Typography, Grid, Link, IconButton } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

export default function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        bgcolor: 'grey.900',
        color: 'white',
        py: 6,
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
              TryScape
            </Typography>
            <Typography variant="body2" color="grey.400">
              AI-powered outfit visualization. See yourself in any outfit, anywhere.
            </Typography>
            <Box sx={{ mt: 2 }}>
              <IconButton color="inherit" aria-label="GitHub" size="small">
                <GitHubIcon />
              </IconButton>
              <IconButton color="inherit" aria-label="Twitter" size="small">
                <TwitterIcon />
              </IconButton>
              <IconButton color="inherit" aria-label="LinkedIn" size="small">
                <LinkedInIcon />
              </IconButton>
            </Box>
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Quick Links
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Link href="#home" color="grey.400" underline="hover">
                Home
              </Link>
              <Link href="#how-it-works" color="grey.400" underline="hover">
                How It Works
              </Link>
              <Link href="#get-started" color="grey.400" underline="hover">
                Get Started
              </Link>
            </Box>
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Support
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Link href="#" color="grey.400" underline="hover">
                Privacy Policy
              </Link>
              <Link href="#" color="grey.400" underline="hover">
                Terms of Service
              </Link>
              <Link href="#" color="grey.400" underline="hover">
                Contact Us
              </Link>
            </Box>
          </Grid>
        </Grid>
        <Box sx={{ mt: 4, pt: 4, borderTop: 1, borderColor: 'grey.800' }}>
          <Typography variant="body2" color="grey.500" align="center">
            © {new Date().getFullYear()} TryScape. All rights reserved. Powered by Azure AI.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}
