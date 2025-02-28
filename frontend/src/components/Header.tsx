import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  Container
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import SoundIcon from '@mui/icons-material/GraphicEq';

const Header: React.FC = () => {
  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Container maxWidth="lg">
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <SoundIcon sx={{ mr: 1 }} />
            <Typography 
              variant="h6" 
              component={RouterLink} 
              to="/"
              sx={{ 
                textDecoration: 'none', 
                color: 'inherit',
                fontWeight: 'bold'
              }}
            >
              Word Sound Practice
            </Typography>
          </Box>
          <Button 
            color="inherit" 
            component={RouterLink} 
            to="/"
          >
            Home
          </Button>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header; 